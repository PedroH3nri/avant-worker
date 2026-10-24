# avant-worker

Worker e agendador (Celery) do Groone Avant. As regras ficam no
[avant-core](https://github.com/PedroH3nri/avant-core), instalado por tag; aqui só há
as tarefas, que montam os adaptadores e chamam os casos de uso.

## Processos

| Processo | Comando | Faz |
| --- | --- | --- |
| worker | `celery -A avant_worker.app worker -Q default,mail -l info` | limpeza e e-mails |
| worker-gam | `celery -A avant_worker.app worker -Q gam -c 2 -l info` | Google Ad Manager; o único com a chave da conta de serviço |
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
| `avant.gam.discover_mcm` | de hora em hora (minuto 5) | lê os child publishers da network da Groone: liga networks novas à Empresa do dono, guarda o MCM sem dono e desconecta o que foi encerrado |
| `avant.gam.sync_network(company_id, network_id, test=True)` | ao conectar, no "sincronizar agora" e depois da descoberta | teste de acesso, sites e ad units, nessa ordem |
| `avant.gam.schedule_tests` | todo dia às 03:00 UTC | uma `avant.gam.check_access` por network ativa |
| `avant.gam.schedule_imports` | de 6 em 6 horas (minuto 20) | uma `avant.gam.sync_network(test=False)` por network ativa |
| `avant.gam.sync_metrics(company_id, network_id, start, end)` | pelos agendadores abaixo | relatórios por ad unit e por key-value do período (SOAP, só leitura), gravados com upsert em `metrics.*`; avisa o painel com `metrics.updated` |
| `avant.gam.schedule_metrics` | de hora em hora (minuto 35) | ontem e hoje de cada network ativa |
| `avant.gam.schedule_reprocess` | todo dia às 04:40 UTC | os três dias antes de ontem (o GAM ajusta os números) |
| `avant.gam.backfill_metrics(company_id, network_id, days=90)` | quando a descoberta do MCM cria uma network | o histórico em lotes de 7 dias |

As métricas das networks do MCM Manage Inventory ficam na network da Groone e ainda não
entram aqui: terão uma tarefa própria, que lê um relatório só e distribui pelas Empresas.

A API enfileira `avant.gam.sync_network` pelo nome (`send_task`), sem importar este pacote.

## Como funciona

- **Entrega**: `task_acks_late` e `prefetch_multiplier=1`. A mensagem só sai da fila
  quando a tarefa termina; se o worker cair, outra instância roda de novo. Toda tarefa
  precisa ser idempotente.
- **RLS**: tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` só para
  limpeza e para varrer todas as Empresas.
- **Conexões**: cada processo filho monta o próprio pool na primeira tarefa.
- **GAM**: API REST do Ad Manager (v1), só leitura (escopo `admanager.readonly`), em
  `gam_client.py`. 401/403 e 404 são falhas permanentes da network (três seguidas viram
  erro e aviso ao dono); 429, 5xx e falha de rede voltam para a fila em 1, 2, 4 e 8 minutos
  sem mudar o estado. Uma trava no Redis por network impede duas importações ao mesmo tempo.
- **Avisos em tempo real**: depois de cada etapa de uma network, o worker publica
  `{"type": "network.updated", "data": {"network_id"}}` no canal Redis
  `avant:events:{company_id}`; a API repassa por SSE (`GET /api/v1/events`).
- **Logs**: JSON em uma linha, com o stack trace quando uma tarefa falha.
- **Métricas**: o worker publica os eventos do Celery; o `celery-exporter` do
  avant-infra transforma em métricas do Prometheus.

## Variáveis

| Variável | Para quê |
| --- | --- |
| `DATABASE_URL` | papel `avant_app` |
| `CELERY_BROKER_URL` | RabbitMQ |
| `REDIS_URL` | resultados e travas; obrigatório em staging e produção |
| `APP_BASE_URL`, `RESEND_API_KEY`, `MAIL_FROM` | avisos por e-mail (`RESEND_API_KEY` obrigatório em staging e produção) |
| `GAM_SERVICE_ACCOUNT_FILE` | caminho do JSON da chave da conta de serviço; só no worker-gam |
| `GAM_GROONE_NETWORK_CODE` | network da Groone (MCM) |
| `GAM_SOAP_VERSION` | opcional: versão da API SOAP dos relatórios (ex.: `v202608`); vazio usa a mais nova do `googleads` |
| `LOG_LEVEL` | padrão `INFO` |

Os nomes estão no `.env.example` do avant-infra; os valores, só nas VMs.

## Desenvolvimento

Para subir o Avant inteiro na máquina (banco, API, worker e painel), siga o [guia de desenvolvimento](https://github.com/PedroH3nri/avant-infra/blob/develop/docs/desenvolvimento.md) do avant-infra.

```bash
uv sync
uv run ruff format . && uv run ruff check . && uv run mypy
export AVANT_TEST_MIGRATIONS_URL=postgresql+psycopg://avant_owner:SENHA@localhost:5432/avant_test
export AVANT_TEST_DATABASE_URL=postgresql+psycopg://avant_app:SENHA@localhost:5432/avant_test
export AVANT_TEST_REDIS_URL=redis://localhost:6379/15   # opcional: teste da trava
uv run pytest
```

Os testes rodam as tarefas no próprio processo (`task_always_eager`), contra o Postgres,
com um GAM em memória (`tests/fake_gam.py`). O adaptador REST é testado com respostas
gravadas do formato da API (`tests/test_gam_client.py`).
A CI faz o mesmo e usa o secret `AVANT_CORE_ACCESS` (token só de leitura do avant-core).

## Imagem

```bash
docker build --secret id=github_token,env=GITHUB_TOKEN -t ghcr.io/pedroh3nri/avant-worker .
```
