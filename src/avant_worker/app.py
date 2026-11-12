"""Aplicação Celery. Rodar com:

celery -A avant_worker.app worker -Q default,mail,gam -l info
celery -A avant_worker.app beat -l info

Filas: ``default`` (limpeza e o resto), ``mail`` (e-mails) e ``gam`` (Google Ad Manager,
que tem cota própria). A fila sai do nome da tarefa: ``avant.<fila>.<nome>``.
"""

import logging
import os
from typing import Any, NoReturn

from avant_core.db.app_role import UnsafeDatabaseRole, ensure_app_role_is_restricted
from avant_core.db.engine import new_engine
from celery import Celery, signals
from celery.schedules import crontab
from pydantic import ValidationError

from avant_worker.logs import configure_logging
from avant_worker.services import _mailer, reset_after_fork
from avant_worker.settings import BrokerSettings, InvalidVariable, Settings

QUEUES = ("default", "mail", "gam")


def _route(name: str, *args: Any, **kwargs: Any) -> dict[str, str]:
    """Escolhe a fila pelo nome da tarefa: avant.<fila>.<nome>; o resto vai para default."""
    parts = name.split(".")
    queue = parts[1] if len(parts) > 2 and parts[0] == "avant" else "default"
    return {"queue": queue if queue in QUEUES else "default"}


def create_app(settings: BrokerSettings | None = None) -> Celery:
    """Monta o Celery com as filas, a rota por nome e o agendamento do beat."""
    broker_settings = settings or BrokerSettings()
    app = Celery(
        "avant",
        include=[
            "avant_worker.tasks.maintenance.purge_tasks",
            "avant_worker.tasks.mail.password_reset_tasks",
            "avant_worker.tasks.gam.network_tasks",
            "avant_worker.tasks.gam.mcm_tasks",
            "avant_worker.tasks.gam.tool_tasks",
            "avant_worker.tasks.metrics.gam_metrics_tasks",
            "avant_worker.tasks.metrics.page_view_tasks",
            "avant_worker.tasks.money.exchange_rate_tasks",
            "avant_worker.tasks.metrics.mcm_earnings_tasks",
            "avant_worker.tasks.commissions.commission_tasks",
            "avant_worker.tasks.reports.report_preview_tasks",
            "avant_worker.tasks.alerts.alert_tasks",
            "avant_worker.tasks.schedules.schedule_tasks",
            "avant_worker.tasks.checklists.checklist_tasks",
            "avant_worker.tasks.rewards.reward_tasks",
            "avant_worker.tasks.ad_tags.ad_tag_tasks",
            "avant_worker.tasks.price_rules.price_rule_tasks",
        ],
    )
    app.conf.update(
        broker_url=broker_settings.celery_broker_url,
        result_backend=broker_settings.redis_url,
        result_expires=24 * 3600,
        # Ninguém lê o resultado das tarefas (a API só enfileira): não guarda no Redis, que fica
        # para travas, limites e eventos. O resultado com erro continua indo para os logs.
        task_ignore_result=True,
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        # Só confirma a mensagem depois de terminar: se o worker cair, a tarefa volta para
        # a fila. Por isso toda tarefa precisa ser idempotente.
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        worker_prefetch_multiplier=1,
        # O RabbitMQ devolve a mensagem que fica 30 minutos sem ack: toda tarefa termina antes.
        # As que têm trava mais curta definem limites próprios, sempre abaixo da trava.
        task_soft_time_limit=20 * 60,
        task_time_limit=25 * 60,
        # Reinicia o processo que passar de 500 MB (relatórios grandes do GAM).
        worker_max_memory_per_child=500_000,
        task_default_queue="default",
        task_routes=(_route,),
        # Eventos para o celery-exporter (métricas no Prometheus).
        worker_send_task_events=True,
        task_send_sent_event=True,
        broker_connection_retry_on_startup=True,
        beat_schedule={
            "key-values": {
                "task": "avant.gam.process_key_values",
                "schedule": 30.0,
                "options": {"expires": 25},
            },
            "key-value-networks": {
                "task": "avant.gam.refresh_key_value_networks",
                "schedule": 300.0,
            },
            "maintenance-purge": {
                "task": "avant.default.purge_expired",
                "schedule": crontab(hour=4, minute=0),
            },
            "gam-discover-mcm": {
                "task": "avant.gam.discover_mcm",
                "schedule": crontab(minute=5),
            },
            "gam-sync-contracts": {
                "task": "avant.gam.sync_contracts",
                "schedule": crontab(minute=10),
            },
            "gam-check-access": {
                "task": "avant.gam.schedule_tests",
                "schedule": crontab(hour=3, minute=0),
            },
            "exchange-rates-sync": {
                "task": "avant.default.sync_exchange_rates",
                "schedule": crontab(hour="*/6", minute=50),
            },
            "gam-sync-mcm-earnings": {
                "task": "avant.gam.sync_mcm_earnings",
                "schedule": crontab(day_of_month="15-20", hour=3, minute=10),
            },
            "page-views-sync": {
                "task": "avant.default.schedule_page_views",
                "schedule": crontab(minute=20),
            },
            "gam-sync-metrics": {
                "task": "avant.gam.schedule_metrics",
                "schedule": crontab(minute=35),
            },
            "scheduled-reports": {
                "task": "avant.default.schedule_reports",
                "schedule": crontab(minute=2),
            },
            "alerts-check": {
                "task": "avant.default.schedule_alerts",
                "schedule": crontab(minute=50),
            },
            "report-previews": {
                "task": "avant.default.refresh_report_previews",
                "schedule": crontab(minute=55),
            },
            "gam-reprocess-metrics": {
                "task": "avant.gam.schedule_reprocess",
                "schedule": crontab(hour=4, minute=40),
            },
            "gam-import-inventory": {
                "task": "avant.gam.schedule_imports",
                "schedule": crontab(hour="*/6", minute=20),
            },
            "commissions-today": {
                "task": "avant.default.calculate_today_commissions",
                "schedule": crontab(minute=45),
            },
            "commissions-recent": {
                "task": "avant.default.calculate_recent_commissions",
                "schedule": crontab(hour=3, minute=0),
            },
            "commissions-transfer": {
                "task": "avant.default.transfer_clients",
                "schedule": crontab(hour=3, minute=30),
            },
            "checklists-open": {
                "task": "avant.default.open_checklists",
                "schedule": crontab(hour=3, minute=15),
            },
            "commissions-close": {
                "task": "avant.default.close_commissions",
                "schedule": crontab(day_of_month="15-20", hour=5, minute=0),
            },
            "reward-events": {
                "task": "avant.default.flush_reward_events",
                "schedule": 60.0,
            },
            "page-views-flush": {
                "task": "avant.default.flush_page_views",
                "schedule": 60.0,
            },
            "page-view-partitions": {
                "task": "avant.default.ensure_page_view_partitions",
                "schedule": crontab(hour=2, minute=30),
            },
            "price-rule-hours": {
                "task": "avant.gam.schedule_price_rule_hours",
                "schedule": crontab(minute=55),
            },
            "price-rules-run": {
                "task": "avant.default.run_price_rules",
                "schedule": crontab(minute=58),
            },
            "price-rules-create": {
                "task": "avant.default.create_price_rules",
                "schedule": crontab(hour=7, minute=0),
            },
            "price-rule-partitions": {
                "task": "avant.default.maintain_price_rule_partitions",
                "schedule": crontab(hour=2, minute=35),
            },
            "reward-batches-purge": {
                "task": "avant.default.purge_reward_batches",
                "schedule": crontab(hour=4, minute=25),
            },
        },
    )
    return app


app = create_app()


@signals.worker_init.connect
def _check_on_start(**_: Any) -> None:
    """Na subida do worker: sem uma variável obrigatória ou com papel do banco que ignora o RLS,
    ele não sobe."""
    check_database_role(check_settings())


@signals.worker_process_init.connect
def _reset_after_fork(**_: Any) -> None:
    """Em cada processo filho do prefork: pool novo, sem dividir conexão com o pai."""
    reset_after_fork()


def check_database_role(settings: Settings) -> None:
    """Recusa a subida se o papel do banco ignora o RLS ou se o banco não responde; levanta
    ``SystemExit`` sem a URL do banco, que tem a senha."""
    try:
        engine = new_engine(settings.database_url, settings.engine_settings())
    except ValueError as exc:
        _refuse_start(str(exc))
    try:
        ensure_app_role_is_restricted(engine)
    except UnsafeDatabaseRole as exc:
        _refuse_start(str(exc))
    except Exception as exc:
        _refuse_start(f"não foi possível conferir o papel do banco ({type(exc).__name__})")
    finally:
        engine.dispose()


def _refuse_start(reason: str) -> NoReturn:
    """Registra o motivo e encerra a subida do worker."""
    logging.getLogger("avant.worker").critical("worker não sobe", extra={"reason": reason})
    raise SystemExit(f"worker não sobe: {reason}")


def check_settings() -> Settings:
    """Confere a configuração do worker; levanta ``SystemExit`` com os nomes do que falta ou
    está errado, sem os valores (o erro do pydantic traz as outras variáveis, com segredos)."""
    try:
        settings = Settings()
    except ValidationError as exc:
        _refuse_start_for(_variable_names(exc))
    try:
        _mailer(settings)
    except ValueError as exc:
        _refuse_start(str(exc))
    return settings


def _variable_names(error: ValidationError) -> list[str]:
    """Os nomes das variáveis com problema: o campo, ou o nome que a checagem do transporte de
    e-mail levantou (``InvalidVariable``); nunca o valor."""
    names: set[str] = set()
    for item in error.errors():
        cause = item.get("ctx", {}).get("error")
        if item["loc"]:
            names.add(str(item["loc"][0]).upper())
        elif isinstance(cause, InvalidVariable):
            names.add(str(cause))
    return sorted(names)


def _refuse_start_for(names: list[str]) -> NoReturn:
    """Registra os nomes das variáveis que faltam e encerra a subida."""
    logging.getLogger("avant.worker").critical(
        "configuração do worker incompleta", extra={"variables": ", ".join(names)}
    )
    raise SystemExit(f"configuração do worker incompleta: {', '.join(names)}")


@signals.setup_logging.connect
def _logging(**_: Any) -> None:
    """Troca o log do Celery pelo log JSON."""
    # Sem este sinal, o Celery troca os handlers e os logs deixam de sair em JSON.
    configure_logging(os.environ.get("LOG_LEVEL", "INFO"))


@signals.task_failure.connect
def _failure(sender: Any = None, exception: BaseException | None = None, **_: Any) -> None:
    """Registra no log a tarefa que falhou, com o stack trace."""
    logging.getLogger("avant.worker").error(
        "tarefa falhou",
        exc_info=exception,
        extra={"task": getattr(sender, "name", None)},
    )
