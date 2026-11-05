# Graph Report - avant-worker  (2026-11-05)

## Corpus Check
- 73 files · ~41,584 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1104 nodes · 2176 edges · 67 communities (40 shown, 27 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 163 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `45397087`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- test_checklist_tasks.py
- test_earnings_tasks.py
- steps
- Avant: conexão com o GAM
- _soap_source
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- adapters/__init__.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- test_schedule_tasks.py
- clean_code.py
- test_commission_tasks.py
- Settings
- session-start.sh
- avant-worker
- ExchangeRateSource
- _FixedClock
- get_services
- FakeGamClient
- Services
- test_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- test_metrics_tasks.py
- pytest
- gam_client.py
- test_gam_tasks.py
- _HttpxResponse
- fake_gam.py
- key_value_tasks.py
- tool_tasks.py
- RestGamClient
- updates
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- test_gam_tool_tasks.py
- services.py
- app.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- schedule_tasks.py
- SoapReportClient
- mcm_tasks.py
- gam_writer.py
- services
- _last
- ReportKind
- gam_reports.py
- test_report_is_read_from_a_temporary_file_as_it_streams
- uuid
- FixedClock
- FakeTrafficWriter
- avant-worker
- report_query
- .list_child_publishers
- _classify
- source_files

## God Nodes (most connected - your core abstractions)
1. `Services` - 83 edges
2. `get_services()` - 50 edges
3. `company()` - 40 edges
4. `SoapGamWriter` - 35 edges
5. `network()` - 32 edges
6. `MemoryWriter` - 23 edges
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

## Communities (67 total, 27 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "test_checklist_tasks.py"
Cohesion: 0.05
Nodes (9): HttpPageFetcher, public_address(), _public_transport(), PublicOnlyBackend, FakePageFetcher, test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text() (+1 more)

### Community 2 - "test_earnings_tasks.py"
Cohesion: 0.12
Nodes (5): months_to_fetch(), _shift(), sync_mcm_earnings(), schedule_page_views(), sync_page_views()

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 5 - "_soap_source"
Cohesion: 0.23
Nodes (6): _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_report_with_only_the_header_is_an_empty_period(), test_a_report_without_the_csv_header_is_a_temporary_failure(), test_report_downloads_before_the_rows_are_read(), test_the_downloaded_file_closes_even_if_nobody_reads_it()

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

### Community 10 - "adapters/__init__.py"
Cohesion: 0.07
Nodes (7): channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates, parse_documents(), test_sync_stores_closed_days_and_today(), test_parse_documents_reads_the_data_counter()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_schedule_tasks.py"
Cohesion: 0.07
Nodes (12): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered() (+4 more)

### Community 14 - "clean_code.py"
Cohesion: 0.18
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.10
Nodes (14): avant-worker, Contexto, issues e skills, refresh_levels(), test_open_checklists_checks_sites_that_earned_last_month(), earnings(), seller_scenario(), test_a_busy_lock_skips_the_run(), test_closing_the_current_month_is_refused() (+6 more)

### Community 16 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 24 - "get_services"
Cohesion: 0.13
Nodes (10): get_services(), backfill_metrics(), _fan_out(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), sync_metrics() (+2 more)

### Community 26 - "Services"
Cohesion: 0.12
Nodes (8): Services, _network(), _store(), test_alerts_fire_once_and_mail_the_list_once(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so(), test_previews_are_refreshed_once_and_again_when_old(), test_due_reports_go_out_once()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "test_metrics_tasks.py"
Cohesion: 0.18
Nodes (11): network(), test_buffered_values_become_gam_values_once(), test_connected_networks_reach_the_route(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_backfill_splits_the_period_in_weekly_chunks(), test_locked_chunk_goes_back_to_the_queue() (+3 more)

### Community 30 - "pytest"
Cohesion: 0.07
Nodes (20): closed_days_to_fetch(), sync_exchange_rates(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing(), client(), record() (+12 more)

### Community 32 - "test_gam_tasks.py"
Cohesion: 0.36
Nodes (15): company(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_discover_mcm_creates_network_and_imports(), test_failed_check_stops_before_importing(), test_lock_skips_a_second_run() (+7 more)

### Community 34 - "fake_gam.py"
Cohesion: 0.14
Nodes (3): FakeExchangeRates, FakePageViews, FakeReports

### Community 35 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.20
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "test_gam_tool_tasks.py"
Cohesion: 0.10
Nodes (10): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+2 more)

### Community 46 - "app.py"
Cohesion: 0.11
Nodes (6): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 52 - "mcm_tasks.py"
Cohesion: 0.25
Nodes (3): Importação, discover_mcm(), sync_contracts()

### Community 54 - "services"
Cohesion: 0.25
Nodes (4): use_services(), engine(), services(), FakeEarnings

### Community 57 - "gam_reports.py"
Cohesion: 0.15
Nodes (5): _ad_unit_path(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria()

### Community 59 - "uuid"
Cohesion: 0.05
Nodes (17): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+9 more)

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 63 - "report_query"
Cohesion: 0.40
Nodes (3): report_query(), _soap_date(), test_report_query_matches_unified_sync()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 544 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `test_checklist_tasks.py`, `adapters/__init__.py`, `test_commission_tasks.py`, `Settings`, `get_services`, `test_metrics_tasks.py`, `pytest`, `test_gam_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `services.py`, `GamNotConfigured`, `SoapReportClient`, `services`, `uuid`, `FixedClock`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 62 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 62 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0567287784679089 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `key_value_tasks.py`, `adapters/__init__.py`, `test_gam_tool_tasks.py`, `services.py`, `gam_writer.py`, `Services`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_checklist_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0549645390070922 - nodes in this community are weakly interconnected._