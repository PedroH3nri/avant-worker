from sqlalchemy import text

from avant_worker.app import app
from avant_worker.services import Services
from avant_worker.tasks.portfolio_health import compute_portfolio_health


def test_portfolio_health_is_scheduled_daily_on_the_default_queue() -> None:
    """A nota de saúde roda todo dia às 05:30 UTC na fila default."""
    app.loader.import_default_modules()
    schedule = app.conf.beat_schedule["portfolio-health"]
    assert schedule["task"] == "avant.default.compute_portfolio_health"
    assert schedule["schedule"].hour == {5}
    assert schedule["schedule"].minute == {30}


def test_portfolio_health_run_is_idempotent(services: Services) -> None:
    """Rodar duas vezes no mesmo dia troca as notas do dia e não repete aviso."""
    first = compute_portfolio_health.delay().get()
    second = compute_portfolio_health.delay().get()
    assert first["scored"] == second["scored"]
    assert second["warned"] == 0
    with services.trusted_uow() as uow:
        rows = uow.session.execute(
            text("SELECT count(*) FROM client_health_scores WHERE day = :day"),
            {"day": services.clock.now().date()},
        ).scalar_one()
    assert rows == first["scored"]
