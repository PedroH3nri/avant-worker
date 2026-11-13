"""Logs em JSON, uma linha por evento, para o Loki. Erros levam o stack trace, com os valores
que o Postgres repete no erro trocados por *** (``scrub_database_error`` do core)."""

import json
import logging
import sys
import traceback
from datetime import UTC, datetime
from typing import Any

from avant_core.db.error_text import scrub_database_error

# Campos que o LogRecord sempre tem; o resto veio de extra= e entra no JSON.
_STANDARD = set(logging.makeLogRecord({}).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Converte o registro de log em uma linha JSON, com stack trace se houver; mensagem e stack
        passam pelo ``scrub_database_error``."""
        data: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "msg": scrub_database_error(record.getMessage()),
        }
        data.update({key: value for key, value in record.__dict__.items() if key not in _STANDARD})
        if record.exc_info:
            stack = "".join(traceback.format_exception(*record.exc_info))
            data["stack"] = scrub_database_error(stack)
        return json.dumps(data, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    """Manda todos os logs em JSON para a saída padrão; os clientes HTTP só a partir de WARNING,
    porque registram cada pedido com a URL completa."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
    for noisy in ("httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
