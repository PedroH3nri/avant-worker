"""Rewards: o buffer de eventos e contatos vira métricas e contatos; o cache sai depois da
importação."""

import json
import uuid
from datetime import timedelta

import pytest
from avant_core.gam.inventory.models import Site
from avant_core.rewards.enums import RewardLeadKind, RewardLeadPosition
from avant_core.rewards.models import Reward, RewardLeadFilter, RewardQuestion

from avant_worker.services import Services
from avant_worker.tasks.rewards import (
    flush_reward_events,
    forget_latest_reward_pages,
    purge_reward_batches_task,
)
from tests.test_gam_tasks import company, network

DAY = "2026-11-09"


@pytest.fixture
def redis_services(services: Services) -> Services:
    """Os serviços com Redis (as tarefas não fazem nada sem ele)."""
    if services.redis is None:
        pytest.skip("defina AVANT_TEST_REDIS_URL")
    return services


def _reward(services: Services, path: str = "receitas/bolo") -> tuple[Reward, RewardQuestion]:
    """Um site com um reward de uma pergunta que pede e-mail no fim."""
    owner = company(services, email=f"dono-{uuid.uuid4().hex[:6]}@blog.com")
    found = network(services, owner, code=uuid.uuid4().hex[:8])
    now = services.clock.now()
    domain = f"blog-{uuid.uuid4().hex[:6]}.com"
    site = Site(owner.id, domain, network_id=found.id, gam_site_id=uuid.uuid4().hex[:10])
    reward = Reward(
        company_id=owner.id,
        site_id=site.id,
        name="Bolo",
        page_path=path,
        title="Libere",
        description="",
        button_text="Ver",
        created_by=None,
        created_at=now,
        updated_at=now,
        icon_emoji="🎁",
        lead_kind=RewardLeadKind.EMAIL,
        lead_position=RewardLeadPosition.END,
        lead_title="E-mail",
        lead_button="Ok",
    )
    question = RewardQuestion(owner.id, reward.id, 1, "Qual?", ["a", "b", "c"])
    with services.uow(owner.id) as uow:
        uow.sites.add(site)
        uow.rewards.add(reward)
        uow.reward_questions.add(question)
        uow.commit()
    return reward, question


def test_buffer_becomes_metrics_and_leads(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    reward, question = _reward(services)
    rid, qid = str(reward.id), str(question.id)
    items = [
        {"type": "event", "day": DAY, "reward_id": rid, "kind": "open"},
        {
            "type": "event",
            "day": DAY,
            "reward_id": rid,
            "kind": "answer",
            "question_id": qid,
            "answer": 1,
        },
        {"type": "event", "day": DAY, "reward_id": rid, "kind": "voou"},
        {
            "type": "lead",
            "reward_id": rid,
            "name": "Ana",
            "contact": "ana@email.com",
            "language": "pt",
            "answers": [{"question_id": qid, "answer": 1}],
            "created_at": services.clock.now().isoformat(),
        },
    ]
    services.redis.rpush("avant:reward:buffer", *(json.dumps(item) for item in items), "{ruim")
    services.redis.rpush("avant:reward:processing:sobra", json.dumps(items[0]))
    totals = flush_reward_events()
    assert totals == {"events": 3, "leads": 1, "skipped": 2}
    assert not services.redis.exists("avant:reward:buffer")
    assert list(services.redis.scan_iter("avant:reward:processing:*")) == []
    with services.uow(reward.company_id) as uow:
        days = uow.reward_metrics.days(
            reward.id,
            services.clock.now().date() - timedelta(days=400),
            services.clock.now().date() + timedelta(days=400),
        )
        assert sum(day.opens for day in days) == 2
        leads = uow.reward_leads.list_for_reward(reward.id, RewardLeadFilter())
        assert [(lead.name, lead.answer_to(question.id)) for lead in leads] == [("Ana", 1)]
    assert flush_reward_events() == {"events": 0, "leads": 0, "skipped": 0}
    assert purge_reward_batches_task() == 0


def test_import_forgets_the_latest_reward_pages(redis_services: Services) -> None:
    services = redis_services
    assert services.redis is not None
    reward, _question = _reward(services, path="")
    with services.uow(reward.company_id) as uow:
        site = uow.sites.get(reward.site_id)
    assert site is not None and site.network_id is not None
    key = f"avant:reward:{site.domain}/"
    services.redis.set(key, "{}")
    assert forget_latest_reward_pages(services, site.network_id) == 1
    assert not services.redis.exists(key)
