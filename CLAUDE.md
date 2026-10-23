# avant-worker

Worker e agendador (Celery) do Groone Avant. Leia o README antes de mudar algo.

- Regra de negócio fica no avant-core. Uma tarefa aqui só monta os adaptadores, chama um
  caso de uso e registra o resultado. Se faltar um caso de uso, ele entra no avant-core primeiro.
- Tarefa com `name="avant.<fila>.<nome>"`; a fila sai do nome (`task_routes` em `app.py`).
- Tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` (sem RLS) só para
  limpeza e para varrer todas as Empresas, sempre documentado na tarefa.
- Tarefas idempotentes: `acks_late` está ligado e uma tarefa pode rodar duas vezes.
- Antes de abrir PR: `uv run ruff format . && uv run ruff check . && uv run mypy && uv run pytest`.
- Nada de segredos no repositório. Mensagens e comentários em português.
- PRs vão para `develop`.
