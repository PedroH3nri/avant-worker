"""Aplicação Celery. Rodar com:

celery -A avant_worker.app worker -Q default,mail,gam -l info
celery -A avant_worker.app beat -l info

Filas: ``default`` (limpeza e o resto), ``mail`` (e-mails) e ``gam`` (Google Ad Manager,
que tem cota própria). A fila sai do nome da tarefa: ``avant.<fila>.<nome>``.
"""

import logging
import os
from typing import Any

from celery import Celery, signals
from celery.schedules import crontab

from avant_worker.logs import configure_logging
from avant_worker.settings import BrokerSettings

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
            "avant_worker.tasks.gam.network_tasks",
            "avant_worker.tasks.gam.mcm_tasks",
            "avant_worker.tasks.metrics.gam_metrics_tasks",
            "avant_worker.tasks.metrics.page_view_tasks",
            "avant_worker.tasks.money.exchange_rate_tasks",
            "avant_worker.tasks.metrics.mcm_earnings_tasks",
            "avant_worker.tasks.commissions.commission_tasks",
        ],
    )
    app.conf.update(
        broker_url=broker_settings.celery_broker_url,
        result_backend=broker_settings.redis_url,
        result_expires=24 * 3600,
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
        task_default_queue="default",
        task_routes=(_route,),
        # Eventos para o celery-exporter (métricas no Prometheus).
        worker_send_task_events=True,
        task_send_sent_event=True,
        broker_connection_retry_on_startup=True,
        beat_schedule={
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
            "commissions-close": {
                "task": "avant.default.close_commissions",
                "schedule": crontab(day_of_month=15, hour=5, minute=0),
            },
        },
    )
    return app


app = create_app()


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
