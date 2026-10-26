# Graph Report - avant-worker  (2026-10-26)

## Corpus Check
- 43 files · ~28,827 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 653 nodes · 1197 edges · 40 communities (19 shown, 21 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 104 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0265c24`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- RestGamClient
- app.py
- steps
- Avant: conexão com o GAM
- test_gam_tasks.py
- Avant: models do MVP
- test_gam_client.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- test_gam_client.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- metrics.py
- clean_code.py
- avant-worker
- services.py
- session-start.sh
- avant-worker
- ExchangeRateSource
- test_metrics_tasks.py
- earnings.py
- FakeGamClient
- .list_mcm_earnings
- Settings
- FakeEarnings
- avant_worker/page_views.py
- gam_client.py
- FakeExchangeRates
- _HttpxResponse
- _last
- _HttpxAuthRequest
- _error
- FakePageViews
- services
- .list_child_publishers

## God Nodes (most connected - your core abstractions)
1. `Services` - 48 edges
2. `get_services()` - 26 edges
3. `company()` - 23 edges
4. `network()` - 21 edges
5. `ReportKind` - 18 edges
6. `fake()` - 17 edges
7. `RestGamClient` - 16 edges
8. `client()` - 14 edges
9. `Groone Avant: contexto do projeto` - 14 edges
10. `inventory()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam.py
- `Sites e ad units` --references--> `network()`  [INFERRED]
  docs/decisoes/06-endpoints-api.md → tests/test_gam_tasks.py
- `Como trabalhar nos repositórios` --references--> `main()`  [INFERRED]
  docs/contexto.md → scripts/clean_code.py
- `Ambientes, deploy e backup` --references--> `main()`  [INFERRED]
  docs/decisoes/02-arquitetura.md → scripts/clean_code.py
- `Pipeline` --references--> `main()`  [INFERRED]
  docs/decisoes/07-repositorios-e-plano.md → scripts/clean_code.py

## Import Cycles
- None detected.

## Communities (40 total, 21 thin omitted)

### Community 2 - "app.py"
Cohesion: 0.06
Nodes (14): create_app(), _failure(), _logging(), _route(), configure_logging(), JsonFormatter, BrokerSettings, purge_expired() (+6 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "test_gam_tasks.py"
Cohesion: 0.10
Nodes (30): avant-worker, Contexto, issues e skills, Como funciona, GamNotConfigured, Services, test_sync_stores_the_month_for_networks_in_avant(), company(), count() (+22 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "test_gam_client.py"
Cohesion: 0.07
Nodes (9): ExchangeRatesUnavailable, OpenExchangeRates, closed_days_to_fetch(), sync_exchange_rates(), _FixedClock, test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_sync_stores_closed_days_and_today() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "test_gam_client.py"
Cohesion: 0.14
Nodes (13): client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "metrics.py"
Cohesion: 0.05
Nodes (23): channel(), publish(), get_services(), check_access(), discover_mcm(), _fan_out(), _flat(), schedule_imports() (+15 more)

### Community 14 - "clean_code.py"
Cohesion: 0.06
Nodes (29): Como trabalhar nos repositórios, Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos (+21 more)

### Community 15 - "avant-worker"
Cohesion: 0.29
Nodes (6): avant-worker, Desenvolvimento, Filas e tarefas, Imagem, Processos, Variáveis

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "test_metrics_tasks.py"
Cohesion: 0.07
Nodes (11): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), ReportKind, _soap_date(), SoapReportClient (+3 more)

### Community 24 - "earnings.py"
Cohesion: 0.21
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 38 - "services"
Cohesion: 0.50
Nodes (3): use_services(), engine(), services()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 333 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `test_gam_tasks.py` to `RestGamClient`, `services`, `test_gam_client.py`, `metrics.py`, `services.py`, `test_metrics_tasks.py`, `Settings`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0595959595959596 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `RestGamClient` to `_last`, `_HttpxAuthRequest`, `test_gam_tasks.py`, `.list_child_publishers`, `test_gam_client.py`, `services.py`, `.list_mcm_earnings`, `gam_client.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._