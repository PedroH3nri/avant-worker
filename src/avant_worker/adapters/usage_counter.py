"""Contador no Redis do uso do painel: a rota de ping não toca no banco.

O contrato com o avant-api (a rota ``POST /api/v1/usage/ping`` soma; ``avant.default.flush_usage``
lê de hora em hora): o hash
``avant:usage:{dia}:{company_id}:{user_id}`` tem os campos ``sessions``, ``screens``,
``active_minutes`` e ``area:{área}``; o conjunto ``avant:usage:days:{dia}`` lista os pares
``{company_id}:{user_id}`` do dia. O worker lê os totais e regrava o dia inteiro no banco
(idempotente). Tudo vence em 3 dias. As marcas de sessão e de minuto ficam em
``avant:usage:mark:{nome}``.
"""

import uuid
from datetime import UTC, date, datetime
from typing import cast

import redis
from avant_core.usage.models import UsageIncrement, UserUsageDay

PREFIX = "avant:usage"
KEPT_SECONDS = 3 * 24 * 60 * 60
AREA = "area:"


def day_key(day: str, company_id: str, user_id: str) -> str:
    """A chave do hash dos totais da pessoa na Empresa no dia (ISO)."""
    return f"{PREFIX}:{day}:{company_id}:{user_id}"


def days_key(day: str) -> str:
    """A chave do conjunto das pessoas com uso no dia (ISO)."""
    return f"{PREFIX}:days:{day}"


class RedisUsageCounter:
    """O contador do Redis: a API marca e soma; o worker lê os totais do dia."""

    def __init__(self, client: redis.Redis) -> None:
        self._client = client

    @classmethod
    def from_url(cls, url: str) -> "RedisUsageCounter":
        """Conecta ao Redis pela URL."""
        return cls(redis.Redis.from_url(url, socket_timeout=1.0))

    def touch(self, name: str, seconds: int) -> bool:
        """Renova a marca por ``seconds``; ``True`` quando ela não existia."""
        previous = self._client.set(f"{PREFIX}:mark:{name}", "1", ex=seconds, get=True)
        return previous is None

    def add(self, increment: UsageIncrement) -> None:
        """Soma o incremento no hash do dia e põe a pessoa no conjunto do dia."""
        day = increment.day.isoformat()
        owner = f"{increment.company_id}:{increment.user_id}"
        key = day_key(day, str(increment.company_id), str(increment.user_id))
        pipe = self._client.pipeline(transaction=False)
        for field, amount in (
            ("sessions", increment.sessions),
            ("screens", increment.screens),
            ("active_minutes", increment.active_minutes),
        ):
            if amount:
                pipe.hincrby(key, field, amount)
        if increment.area:
            pipe.hincrby(key, f"{AREA}{increment.area}", 1)
        pipe.expire(key, KEPT_SECONDS)
        pipe.sadd(days_key(day), owner)
        pipe.expire(days_key(day), KEPT_SECONDS)
        pipe.execute()

    def totals(self, day: date) -> list[UserUsageDay]:
        """Os totais de cada pessoa e Empresa no dia, para gravar no banco."""
        now = datetime.now(UTC)
        found = []
        members = cast(set[bytes], self._client.smembers(days_key(day.isoformat())))
        for owner in sorted(members):
            company_id, user_id = text(owner).split(":")
            stored = cast(
                dict[bytes, bytes],
                self._client.hgetall(day_key(day.isoformat(), company_id, user_id)),
            )
            fields = {text(name): int(value) for name, value in stored.items()}
            found.append(usage_day_of(day, company_id, user_id, fields, now))
        return found


def text(value: bytes | str) -> str:
    """O valor do Redis como texto."""
    return value.decode() if isinstance(value, bytes) else value


def usage_day_of(
    day: date, company_id: str, user_id: str, fields: dict[str, int], now: datetime
) -> UserUsageDay:
    """O dia de uso a partir dos campos do hash."""
    return UserUsageDay(
        user_id=uuid.UUID(user_id),
        company_id=uuid.UUID(company_id),
        day=day,
        updated_at=now,
        sessions=fields.get("sessions", 0),
        screens=fields.get("screens", 0),
        active_minutes=fields.get("active_minutes", 0),
        areas={
            name.removeprefix(AREA): count
            for name, count in fields.items()
            if name.startswith(AREA)
        },
    )
