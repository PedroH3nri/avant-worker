# Graph Report - avant-worker  (2026-10-30)

## Corpus Check
- 53 files · ~31,393 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 719 nodes · 1360 edges · 38 communities (21 shown, 17 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 107 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `211942eb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- adapters/__init__.py
- fake_gam.py
- app.py
- steps
- Avant: conexão com o GAM
- Services
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- test_gam_client.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- FakeGamClient
- clean_code.py
- avant-worker
- services.py
- session-start.sh
- avant-worker
- ExchangeRateSource
- gam_reports.py
- gam_metrics_tasks.py
- _last
- get_services
- Settings
- Avant: grupos na Empresa e imagem da Empresa
- .list_child_publishers
- gam_client.py
- _HttpxResponse
- _HttpxAuthRequest
- RestGamClient
- .list_mcm_earnings
- _error
- datetime

## God Nodes (most connected - your core abstractions)
1. `Services` - 52 edges
2. `get_services()` - 32 edges
3. `company()` - 25 edges
4. `network()` - 23 edges
5. `RestGamClient` - 17 edges
6. `fake()` - 17 edges
7. `ReportKind` - 14 edges
8. `client()` - 14 edges
9. `Groone Avant: contexto do projeto` - 14 edges
10. `publish()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam/mcm_tasks.py
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

## Communities (38 total, 17 thin omitted)

### Community 0 - "adapters/__init__.py"
Cohesion: 0.07
Nodes (7): channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates, MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 2 - "app.py"
Cohesion: 0.07
Nodes (13): create_app(), _failure(), _logging(), _route(), configure_logging(), JsonFormatter, BrokerSettings, test_commission_tasks_are_registered_on_the_default_queue() (+5 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "Services"
Cohesion: 0.08
Nodes (33): avant-worker, Contexto, issues e skills, GamNotConfigured, Services, earnings(), seller_scenario(), test_the_daily_run_fills_every_open_day(), test_today_is_calculated_and_the_month_closes() (+25 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "test_gam_client.py"
Cohesion: 0.11
Nodes (16): test_client_reads_rates_as_decimals_and_fails_clearly(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing(), client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived() (+8 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 14 - "clean_code.py"
Cohesion: 0.06
Nodes (29): Como trabalhar nos repositórios, Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos (+21 more)

### Community 15 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 16 - "services.py"
Cohesion: 0.13
Nodes (6): use_services(), engine(), services(), FakeEarnings, FakePageViews, FakeReports

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "gam_reports.py"
Cohesion: 0.07
Nodes (10): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), _soap_date(), SoapReportClient, test_parse_ad_unit_report() (+2 more)

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.08
Nodes (13): ReportKind, backfill_metrics(), _fan_out(), _network(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store() (+5 more)

### Community 26 - "get_services"
Cohesion: 0.06
Nodes (16): get_services(), discover_mcm(), sync_contracts(), check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests() (+8 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 366 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `adapters/__init__.py`, `fake_gam.py`, `services.py`, `RestGamClient`, `test_gam_client.py`, `services.py`, `gam_reports.py`, `gam_metrics_tasks.py`, `get_services`, `Settings`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 37 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `adapters/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07422402159244265 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `RestGamClient` to `adapters/__init__.py`, `services.py`, `_HttpxAuthRequest`, `Services`, `.list_mcm_earnings`, `test_gam_client.py`, `_last`, `.list_child_publishers`, `gam_client.py`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0748663101604278 - nodes in this community are weakly interconnected._