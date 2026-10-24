# avant-worker

Worker e agendador (Celery) do Groone Avant. Leia o README antes de mudar algo.

- Regra de negócio fica no avant-core. Uma tarefa aqui só monta os adaptadores, chama um
  caso de uso e registra o resultado. Se faltar um caso de uso, ele entra no avant-core primeiro.
- Tarefa com `name="avant.<fila>.<nome>"`; a fila sai do nome (`task_routes` em `app.py`).
- Tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` (sem RLS) só para
  limpeza e para varrer todas as Empresas, sempre documentado na tarefa.
- O GAM é só leitura: `gam_client.py` não ganha método que escreve sem revisão do Pedro.
- Tarefas idempotentes: `acks_late` está ligado e uma tarefa pode rodar duas vezes.
- Clean code obrigatório (skill `avant-clean-code`): nomes claros, nada de nome de uma letra,
  toda função com docstring de 1 ou 2 linhas sobre o que faz, nada de comentário ao lado do
  código. Conferido por `scripts/clean_code.py` no CI.
- Antes de abrir PR: `uv run ruff format . && uv run ruff check . && uv run mypy && uv run pytest && uv run python scripts/clean_code.py`.
- Nada de segredos no repositório. Mensagens e comentários em português.
- PRs vão para `develop`.

## Contexto, issues e skills

- Comece por `docs/contexto.md`: produto, decisões, estado dos cinco repositórios e onde está cada coisa. Decisões antigas em `docs/decisoes/`.
- Todo trabalho parte de uma issue com milestone neste repositório (`gh issue list --milestone ...`). Pedido sem issue vira issue antes.
- Skills em `docs/skills/` (índice em `docs/skills/README.md`); `.claude/skills` aponta para lá. Comece pela `avant-fluxo-de-trabalho`.
- Grafo do código em `graphify-out/` (comece pelo `GRAPH_REPORT.md`, ou `graphify query "..."`). Mudou código: `graphify update .` e commite o grafo no mesmo PR.
