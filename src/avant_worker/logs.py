"""Logs em JSON, uma linha por evento, para o Loki. Erros levam o stack trace."""

import json
import logging
import sys
import traceback
from datetime import UTC, datetime
from typing import Any

# Campos que o LogRecord sempre tem; o resto veio de extra= e entra no JSON.
_STANDARD = set(logging.makeLogRecord({}).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "msg": record.getMessage(),
        }
        data.update({k: v for k, v in record.__dict__.items() if k not in _STANDARD})
        if record.exc_info:
            data["stack"] = "".join(traceback.format_exception(*record.exc_info))
        return json.dumps(data, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
