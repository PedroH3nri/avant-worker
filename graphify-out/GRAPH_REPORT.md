# Graph Report - avant-worker  (2026-11-02)

## Corpus Check
- 62 files · ~33,531 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 798 nodes · 1543 edges · 44 communities (27 shown, 17 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 124 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `924bc893`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- adapters/__init__.py
- Settings
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
- network_tasks.py
- clean_code.py
- test_commission_tasks.py
- services.py
- session-start.sh
- avant-worker
- ExchangeRateSource
- gam_reports.py
- gam_metrics_tasks.py
- page_views.py
- page_view_tasks.py
- mcm_earnings_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- test_exchange_rates_tasks.py
- test_schedule_tasks.py
- gam_client.py
- uuid
- _HttpxResponse
- get_services
- FakeGamClient
- services
- RestGamClient
- FakeCredentials
- _HttpxAuthRequest
- purge_tasks.py
- .list_mcm_earnings
- _error
- ReportSource

## God Nodes (most connected - your core abstractions)
1. `Services` - 63 edges
2. `get_services()` - 42 edges
3. `company()` - 31 edges
4. `network()` - 23 edges
5. `RestGamClient` - 17 edges
6. `fake()` - 17 edges
7. `ReportKind` - 14 edges
8. `_route()` - 14 edges
9. `client()` - 14 edges
10. `Groone Avant: contexto do projeto` - 14 edges

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

## Communities (44 total, 17 thin omitted)

### Community 0 - "adapters/__init__.py"
Cohesion: 0.11
Nodes (4): channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates

### Community 1 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 2 - "app.py"
Cohesion: 0.10
Nodes (5): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "Services"
Cohesion: 0.07
Nodes (35): GamNotConfigured, Services, FakeEarnings, FakePageViews, FakeReports, test_alerts_fire_once_and_mail_the_list_once(), test_a_busy_lock_skips_the_run(), test_a_long_run_renews_the_lock() (+27 more)

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
Cohesion: 0.19
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 14 - "clean_code.py"
Cohesion: 0.05
Nodes (29): Como trabalhar nos repositórios, Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos (+21 more)

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.08
Nodes (18): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+10 more)

### Community 22 - "ExchangeRateSource"
Cohesion: 0.13
Nodes (3): EarningsSource, ExchangeRateSource, PageViewSource

### Community 23 - "gam_reports.py"
Cohesion: 0.07
Nodes (11): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), ReportKind, _soap_date(), SoapReportClient (+3 more)

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.12
Nodes (9): backfill_metrics(), _fan_out(), _network(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store(), sync_metrics() (+1 more)

### Community 27 - "mcm_earnings_tasks.py"
Cohesion: 0.21
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "test_exchange_rates_tasks.py"
Cohesion: 0.08
Nodes (8): closed_days_to_fetch(), sync_exchange_rates(), FakeExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 30 - "test_schedule_tasks.py"
Cohesion: 0.08
Nodes (9): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_report_preview_tasks_are_registered_on_the_default_queue() (+1 more)

### Community 32 - "uuid"
Cohesion: 0.07
Nodes (11): check_alerts(), notify_alerts(), schedule_alerts(), refresh_report_preview(), refresh_report_previews(), deliver_reports(), schedule_reports(), test_publish_without_redis_is_a_no_op() (+3 more)

### Community 34 - "get_services"
Cohesion: 0.27
Nodes (3): get_services(), discover_mcm(), sync_contracts()

### Community 36 - "services"
Cohesion: 0.50
Nodes (3): use_services(), engine(), services()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 396 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `adapters/__init__.py`, `Settings`, `get_services`, `uuid`, `services`, `RestGamClient`, `network_tasks.py`, `test_commission_tasks.py`, `services.py`, `gam_reports.py`, `gam_metrics_tasks.py`, `test_exchange_rates_tasks.py`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Are the 46 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 46 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `adapters/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `uuid`, `Settings`, `app.py`, `Services`, `commission_tasks.py`, `purge_tasks.py`, `network_tasks.py`, `services.py`, `gam_metrics_tasks.py`, `page_view_tasks.py`, `mcm_earnings_tasks.py`, `test_exchange_rates_tasks.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10317460317460317 - nodes in this community are weakly interconnected._