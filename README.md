# avant-worker

Worker e agendador (Celery) do Groone Avant. As regras ficam no
[avant-core](https://github.com/PedroH3nri/avant-core), instalado por tag; aqui só há
as tarefas, que montam os adaptadores e chamam os casos de uso.

## Processos

| Processo | Comando | Faz |
| --- | --- | --- |
| worker | `celery -A avant_worker.app worker -Q default,mail,gam -l info` | roda as tarefas |
| scheduler | `celery -A avant_worker.app beat -l info` | publica as tarefas agendadas; um só por ambiente |

O agendador não fala com o banco: só precisa de `CELERY_BROKER_URL`.

## Filas e tarefas

A fila sai do nome da tarefa, `avant.<fila>.<nome>`:

- `default`: limpeza e o resto.
- `mail`: e-mails (por enquanto a API manda direto, depois do commit).
- `gam`: Google Ad Manager, que tem cota própria e não pode travar as outras filas.

| Tarefa | Quando | Faz |
| --- | --- | --- |
| `avant.default.purge_expired` | todo dia às 04:00 UTC | apaga sessões encerradas há mais de 30 dias e links de nova senha vencidos há mais de 7 |

## Como funciona

- **Entrega**: `task_acks_late` e `prefetch_multiplier=1`. A mensagem só sai da fila
  quando a tarefa termina; se o worker cair, outra instância roda de novo. Toda tarefa
  precisa ser idempotente.
- **RLS**: tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` só para
  limpeza e para varrer todas as Empresas.
- **Conexões**: cada processo filho monta o próprio pool na primeira tarefa.
- **Logs**: JSON em uma linha, com o stack trace quando uma tarefa falha.
- **Métricas**: o worker publica os eventos do Celery; o `celery-exporter` do
  avant-infra transforma em métricas do Prometheus.

## Variáveis

`DATABASE_URL` (papel `avant_app`), `CELERY_BROKER_URL`, `REDIS_URL` (resultados) e
`LOG_LEVEL`. Os nomes estão no `.env.example` do avant-infra.

## Desenvolvimento

```bash
uv sync
uv run ruff format . && uv run ruff check . && uv run mypy
export AVANT_TEST_MIGRATIONS_URL=postgresql+psycopg://avant_owner:SENHA@localhost:5432/avant_test
export AVANT_TEST_DATABASE_URL=postgresql+psycopg://avant_app:SENHA@localhost:5432/avant_test
uv run pytest
```

Os testes rodam as tarefas no próprio processo (`task_always_eager`), contra o Postgres.
A CI faz o mesmo e usa o secret `AVANT_CORE_ACCESS` (token só de leitura do avant-core).

## Imagem

```bash
docker build --secret id=github_token,env=GITHUB_TOKEN -t ghcr.io/pedroh3nri/avant-worker .
```
