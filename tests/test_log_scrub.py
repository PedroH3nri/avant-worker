import logging
import sys

from avant_worker.logs import JsonFormatter

DETAIL = "duplicate key\nDETAIL:  Key (email)=(ana@cliente.com) already exists."


def _record(message: str, *, with_error: bool) -> logging.LogRecord:
    """Um registro de erro com a mensagem e, se pedido, a exceção do banco em andamento."""
    exc_info = None
    if with_error:
        try:
            raise RuntimeError(DETAIL)
        except RuntimeError:
            exc_info = sys.exc_info()
    return logging.LogRecord("avant", logging.ERROR, __file__, 1, message, None, exc_info)


def test_log_masks_database_values_in_message_and_stack() -> None:
    line = JsonFormatter().format(_record(DETAIL, with_error=True))
    assert "ana@cliente.com" not in line
    assert "DETAIL: ***" in line


def test_log_keeps_ordinary_messages() -> None:
    line = JsonFormatter().format(_record("tarefa terminou", with_error=False))
    assert "tarefa terminou" in line
