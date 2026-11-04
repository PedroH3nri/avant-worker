# Graph Report - avant-worker  (2026-11-04)

## Corpus Check
- 69 files · ~38,596 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 989 nodes · 1941 edges · 71 communities (38 shown, 33 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 146 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e209efc2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- HttpPageFetcher
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
- purge_tasks.py
- clean_code.py
- test_commission_tasks.py
- FakeGamClient
- session-start.sh
- avant-worker
- ExchangeRateSource
- gam_reports.py
- gam_metrics_tasks.py
- test_gam_tasks.py
- test_schedule_tasks.py
- page_view_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- OpenExchangeRates
- app.py
- alert_tasks.py
- _HttpxResponse
- test_earnings_tasks.py
- test_exchange_rates_tasks.py
- services
- RestGamClient
- adapters/__init__.py
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- soap_writer
- test_metrics_tasks.py
- page_views.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- RecordingMailer
- SoapReportClient
- test_earnings_tasks.py
- test_checklist_tasks.py
- exchange_rates.py
- logs.py
- report_preview_tasks.py
- metrics/__init__.py
- schedule_tasks.py
- checklist_tasks.py
- source_files
- GamNotConfigured
- avant-worker
- test_gam_tool_tasks.py
- pytest
- _route
- uuid
- _failure
- FakePageFetcher
- FakeCredentials

## God Nodes (most connected - your core abstractions)
1. `Services` - 75 edges
2. `get_services()` - 47 edges
3. `company()` - 38 edges
4. `SoapGamWriter` - 33 edges
5. `network()` - 30 edges
6. `MemoryWriter` - 22 edges
7. `RestGamClient` - 17 edges
8. `fake()` - 17 edges
9. `_route()` - 16 edges
10. `publish()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Sites e ad units` --references--> `network()`  [INFERRED]
  docs/decisoes/06-endpoints-api.md → tests/test_gam_tasks.py
- `Como trabalhar nos repositórios` --references--> `main()`  [INFERRED]
  docs/contexto.md → scripts/clean_code.py
- `Ambientes, deploy e backup` --references--> `main()`  [INFERRED]
  docs/decisoes/02-arquitetura.md → scripts/clean_code.py
- `Pipeline` --references--> `main()`  [INFERRED]
  docs/decisoes/07-repositorios-e-plano.md → scripts/clean_code.py
- `Primeira semana (23/10 a 02/11)` --references--> `main()`  [INFERRED]
  docs/decisoes/07-repositorios-e-plano.md → scripts/clean_code.py

## Import Cycles
- None detected.

## Communities (71 total, 33 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 5 - "Services"
Cohesion: 0.18
Nodes (13): Services, test_alerts_fire_once_and_mail_the_list_once(), company(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), test_run_tool_configures_the_network(), reports(), test_backfill_runs_the_chunks_one_after_another(), test_backfill_splits_the_period_in_weekly_chunks() (+5 more)

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
Cohesion: 0.22
Nodes (11): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_network_and_admin_check(), handler(), test_network_failures_are_temporary() (+3 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 14 - "clean_code.py"
Cohesion: 0.18
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.11
Nodes (11): avant-worker, Contexto, issues e skills, test_open_checklists_checks_sites_that_earned_last_month(), earnings(), FixedClock, seller_scenario(), test_closing_the_current_month_is_refused(), test_closing_warns_on_the_20th_when_the_month_is_still_open() (+3 more)

### Community 16 - "FakeGamClient"
Cohesion: 0.09
Nodes (6): use_services(), engine(), services(), FakeEarnings, FakeExchangeRates, FakeGamClient

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "gam_reports.py"
Cohesion: 0.13
Nodes (6): _ad_unit_path(), _integer(), parse_report(), report_query(), ReportKind, _soap_date()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.10
Nodes (11): backfill_metrics(), _chunks_chain(), _fan_out(), _network(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess() (+3 more)

### Community 25 - "test_gam_tasks.py"
Cohesion: 0.33
Nodes (15): count(), fake(), inventory(), network(), test_check_access_and_schedulers(), test_discover_mcm_creates_network_and_imports(), test_failed_check_stops_before_importing(), test_lock_skips_a_second_run() (+7 more)

### Community 26 - "test_schedule_tasks.py"
Cohesion: 0.16
Nodes (3): test_alert_tasks_are_registered_on_their_queues(), test_report_preview_tasks_are_registered_on_the_default_queue(), test_schedule_tasks_are_registered_on_their_queues()

### Community 27 - "page_view_tasks.py"
Cohesion: 0.18
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "OpenExchangeRates"
Cohesion: 0.15
Nodes (3): OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today()

### Community 32 - "alert_tasks.py"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 35 - "test_exchange_rates_tasks.py"
Cohesion: 0.17
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 38 - "adapters/__init__.py"
Cohesion: 0.18
Nodes (4): channel(), publish(), schedule_page_views(), sync_page_views()

### Community 41 - "network_tasks.py"
Cohesion: 0.12
Nodes (11): Importação, get_services(), discover_mcm(), sync_contracts(), check_access(), _fan_out(), _flat(), schedule_imports() (+3 more)

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "soap_writer"
Cohesion: 0.15
Nodes (5): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 46 - "test_metrics_tasks.py"
Cohesion: 0.15
Nodes (6): FakePageViews, FakeReports, row(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_report_query_matches_unified_sync()

### Community 47 - "page_views.py"
Cohesion: 0.20
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 52 - "test_earnings_tasks.py"
Cohesion: 0.21
Nodes (3): _FixedClock, test_earnings_task_is_on_the_gam_queue(), test_sync_stores_the_month_for_networks_in_avant()

### Community 57 - "metrics/__init__.py"
Cohesion: 0.20
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 64 - "pytest"
Cohesion: 0.32
Nodes (3): test_a_busy_lock_skips_the_run(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so()

### Community 65 - "_route"
Cohesion: 0.25
Nodes (7): _route(), test_commission_tasks_are_registered_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_queue_comes_from_the_task_name()

### Community 66 - "uuid"
Cohesion: 0.33
Nodes (3): test_publish_without_redis_is_a_no_op(), test_deployed_envs_need_redis_and_resend(), test_purge_expired()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 489 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `HttpPageFetcher`, `Settings`, `test_commission_tasks.py`, `FakeGamClient`, `gam_metrics_tasks.py`, `test_gam_tasks.py`, `page_view_tasks.py`, `OpenExchangeRates`, `test_exchange_rates_tasks.py`, `RestGamClient`, `network_tasks.py`, `services.py`, `page_views.py`, `SoapReportClient`, `test_earnings_tasks.py`, `GamNotConfigured`, `test_gam_tool_tasks.py`, `pytest`, `uuid`, `.page_views`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `Services`, `adapters/__init__.py`, `soap_writer`, `services.py`, `GamNotConfigured`, `gam_client.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._