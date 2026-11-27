"""Segurança do site (M18, C2, decisão 23): soma os sinais que a ad tag viu por site e dia, acha o
conteúdo diferente conforme a origem e abre ou fecha a suspeita de cloaker com o aviso no sino.

Usa ``trusted_uow()`` (sem RLS): varre as páginas vistas de todas as Empresas. Idempotente:
regrava hoje e ontem, e uma suspeita aberta não avisa outra vez. A verificação ``security`` das
páginas roda na rotina diária da verificação de instalação.
"""

import logging

from avant_core.site_security.services import aggregate_site_integrity as aggregate

from avant_worker.app import app
from avant_worker.services import get_services

log = logging.getLogger("avant.worker.site_security")


@app.task(name="avant.default.aggregate_site_integrity")
def aggregate_site_integrity() -> dict[str, int]:
    """trusted_uow: grava os sinais por site e dia e confere a suspeita de cloaker."""
    services = get_services()
    run = aggregate(services.trusted_uow(), clock=services.clock)
    log.info(
        "sinais da ad tag somados",
        extra={"days": run.days, "opened": run.opened, "closed": run.closed},
    )
    return {"days": run.days, "opened": run.opened, "closed": run.closed}
