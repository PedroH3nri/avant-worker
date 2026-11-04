# Graph Report - avant-worker  (2026-11-03)

## Corpus Check
- 69 files · ~38,220 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 978 nodes · 1914 edges · 51 communities (30 shown, 21 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 143 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4b70e70`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- test_checklist_tasks.py
- Settings
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
- get_services
- clean_code.py
- test_commission_tasks.py
- FakeExchangeRates
- session-start.sh
- avant-worker
- ExchangeRateSource
- adapters/__init__.py
- gam_metrics_tasks.py
- services
- PageViewSource
- page_view_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- fake_gam.py
- create_app
- gam_client.py
- uuid
- _HttpxResponse
- test_earnings_tasks.py
- services
- RestGamClient
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- test_gam_tool_tasks.py
- page_views.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- app.py
- metrics/__init__.py
- source_files

## God Nodes (most connected - your core abstractions)
1. `Services` - 73 edges
2. `get_services()` - 47 edges
3. `company()` - 36 edges
4. `SoapGamWriter` - 33 edges
5. `network()` - 28 edges
6. `MemoryWriter` - 22 edges
7. `RestGamClient` - 17 edges
8. `fake()` - 17 edges
9. `_route()` - 16 edges
10. `publish()` - 15 edges

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

## Communities (51 total, 21 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "test_checklist_tasks.py"
Cohesion: 0.07
Nodes (4): HttpPageFetcher, FakePageFetcher, test_checklist_tasks_are_registered(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 2 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "Services"
Cohesion: 0.05
Nodes (37): Services, FakeEarnings, FakePageViews, FakeReports, RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month() (+29 more)

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
Cohesion: 0.05
Nodes (22): ExchangeRatesUnavailable, OpenExchangeRates, closed_days_to_fetch(), sync_exchange_rates(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_stores_closed_days_and_today() (+14 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "get_services"
Cohesion: 0.12
Nodes (8): get_services(), discover_mcm(), sync_contracts(), purge_expired(), backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 14 - "clean_code.py"
Cohesion: 0.16
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.07
Nodes (21): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+13 more)

### Community 22 - "ExchangeRateSource"
Cohesion: 0.13
Nodes (3): EarningsSource, ExchangeRateSource, ReportSource

### Community 23 - "adapters/__init__.py"
Cohesion: 0.07
Nodes (11): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), ReportKind, _soap_date(), SoapReportClient (+3 more)

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.20
Nodes (5): _network(), _reads_groone_network(), _store(), sync_metrics(), test_metrics_tasks_are_registered_on_the_gam_queue()

### Community 25 - "services"
Cohesion: 0.50
Nodes (3): use_services(), engine(), services()

### Community 27 - "page_view_tasks.py"
Cohesion: 0.12
Nodes (7): channel(), publish(), GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 32 - "uuid"
Cohesion: 0.06
Nodes (12): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), open_checklists(), refresh_report_preview(), refresh_report_previews(), deliver_reports() (+4 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "test_gam_tool_tasks.py"
Cohesion: 0.07
Nodes (16): _failure(), _logging(), _route(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), FakeSoapClient, FakeSoapService (+8 more)

### Community 47 - "page_views.py"
Cohesion: 0.15
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 57 - "metrics/__init__.py"
Cohesion: 0.14
Nodes (6): months_to_fetch(), _shift(), sync_mcm_earnings(), schedule_page_views(), sync_page_views(), test_months_backfill_then_previous_month_again()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 485 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `test_checklist_tasks.py`, `Settings`, `uuid`, `RestGamClient`, `network_tasks.py`, `test_gam_client.py`, `get_services`, `services.py`, `page_views.py`, `test_commission_tasks.py`, `app.py`, `adapters/__init__.py`, `gam_metrics_tasks.py`, `services`, `page_view_tasks.py`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 53 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05794556628621598 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `Services`, `test_gam_tool_tasks.py`, `services.py`, `adapters/__init__.py`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_checklist_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07459677419354839 - nodes in this community are weakly interconnected._