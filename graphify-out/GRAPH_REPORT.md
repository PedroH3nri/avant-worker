# Graph Report - avant-worker  (2026-11-05)

## Corpus Check
- 73 files · ~41,741 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1106 nodes · 2182 edges · 68 communities (45 shown, 23 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 165 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59e92cf2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- test_checklist_tasks.py
- mcm_earnings_tasks.py
- steps
- Avant: conexão com o GAM
- _soap_source
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- datetime
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- test_schedule_tasks.py
- clean_code.py
- test_commission_tasks.py
- Settings
- session-start.sh
- avant-worker
- ExchangeRateSource
- test_earnings_tasks.py
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
- conftest.py
- key_value_tasks.py
- tool_tasks.py
- RestGamClient
- updates
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- FakeSoapClient
- adapters/__init__.py
- app.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- page_view_tasks.py
- HttpPageFetcher
- RecordingMailer
- exchange_rate_tasks.py
- services.py
- _last
- test_gam_tool_tasks.py
- gam_reports.py
- _route
- uuid
- pytest
- test_key_value_tasks.py
- avant-worker
- .uow
- .list_child_publishers
- test_the_writer_lets_other_gam_errors_through
- source_files
- FakePageFetcher

## God Nodes (most connected - your core abstractions)
1. `Services` - 84 edges
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

## Communities (68 total, 23 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "test_checklist_tasks.py"
Cohesion: 0.09
Nodes (5): public_address(), _public_transport(), PublicOnlyBackend, refresh_levels(), test_public_addresses_are_allowed()

### Community 2 - "mcm_earnings_tasks.py"
Cohesion: 0.24
Nodes (3): months_to_fetch(), _shift(), sync_mcm_earnings()

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "_soap_source"
Cohesion: 0.10
Nodes (7): _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_report_with_only_the_header_is_an_empty_period(), test_a_report_without_the_csv_header_is_a_temporary_failure(), test_report_downloads_before_the_rows_are_read(), test_report_is_read_from_a_temporary_file_as_it_streams(), test_the_downloaded_file_closes_even_if_nobody_reads_it()

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
Nodes (12): avant-worker, Contexto, issues e skills, earnings(), FixedClock, seller_scenario(), test_a_busy_lock_skips_the_run(), test_closing_the_current_month_is_refused(), test_closing_warns_on_the_20th_when_the_month_is_still_open() (+4 more)

### Community 16 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "test_earnings_tasks.py"
Cohesion: 0.24
Nodes (3): _FixedClock, test_client_reads_mcm_earnings_money_in_micros(), test_months_backfill_then_previous_month_again()

### Community 24 - "get_services"
Cohesion: 0.11
Nodes (10): backfill_metrics(), _fan_out(), _network(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store() (+2 more)

### Community 26 - "Services"
Cohesion: 0.20
Nodes (5): Services, test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so(), staff(), test_run_tool_configures_the_network()

### Community 27 - "test_tasks.py"
Cohesion: 0.17
Nodes (3): purge_expired(), test_deployed_envs_need_redis_and_resend(), test_queue_comes_from_the_task_name()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "test_metrics_tasks.py"
Cohesion: 0.32
Nodes (13): test_open_checklists_checks_sites_that_earned_last_month(), company(), network(), test_a_busy_network_waits_and_tries_again(), test_connected_networks_reach_the_route(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history() (+5 more)

### Community 30 - "pytest"
Cohesion: 0.14
Nodes (13): client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 32 - "test_gam_tasks.py"
Cohesion: 0.28
Nodes (13): count(), fake(), inventory(), test_check_access_and_schedulers(), test_discover_mcm_creates_network_and_imports(), test_failed_check_stops_before_importing(), test_lock_skips_a_second_run(), test_permanent_error_during_import_is_recorded_not_retried() (+5 more)

### Community 34 - "conftest.py"
Cohesion: 0.14
Nodes (6): engine(), services(), FakeEarnings, FakeExchangeRates, FakePageViews, FakeReports

### Community 35 - "key_value_tasks.py"
Cohesion: 0.16
Nodes (5): get_services(), _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.20
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.12
Nodes (9): discover_mcm(), sync_contracts(), check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network() (+1 more)

### Community 45 - "adapters/__init__.py"
Cohesion: 0.15
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 46 - "app.py"
Cohesion: 0.11
Nodes (6): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "page_view_tasks.py"
Cohesion: 0.15
Nodes (5): channel(), publish(), schedule_page_views(), sync_page_views(), test_publish_without_redis_is_a_no_op()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.17
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 53 - "exchange_rate_tasks.py"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 56 - "test_gam_tool_tasks.py"
Cohesion: 0.22
Nodes (4): soap_writer(), test_tool_task_is_registered(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 57 - "gam_reports.py"
Cohesion: 0.05
Nodes (13): _ad_unit_path(), _classify(), _integer(), parse_report(), _read_rows(), report_query(), ReportKind, _soap_date() (+5 more)

### Community 58 - "_route"
Cohesion: 0.18
Nodes (10): _route(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue() (+2 more)

### Community 59 - "uuid"
Cohesion: 0.05
Nodes (16): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+8 more)

### Community 60 - "pytest"
Cohesion: 0.22
Nodes (4): test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 61 - "test_key_value_tasks.py"
Cohesion: 0.12
Nodes (4): FakeTrafficWriter, redis_services(), test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_buffered_values_become_gam_values_once()

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 63 - ".uow"
Cohesion: 0.24
Nodes (4): test_alerts_fire_once_and_mail_the_list_once(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), test_previews_are_refreshed_once_and_again_when_old(), test_due_reports_go_out_once()

### Community 65 - "test_the_writer_lets_other_gam_errors_through"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 546 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `datetime`, `test_commission_tasks.py`, `Settings`, `get_services`, `test_metrics_tasks.py`, `test_gam_tasks.py`, `conftest.py`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `adapters/__init__.py`, `GamNotConfigured`, `HttpPageFetcher`, `services.py`, `gam_reports.py`, `uuid`, `pytest`, `test_key_value_tasks.py`, `.uow`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 63 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 63 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0567287784679089 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `key_value_tasks.py`, `adapters/__init__.py`, `services.py`, `test_gam_tool_tasks.py`, `gam_reports.py`, `Services`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_checklist_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09259259259259259 - nodes in this community are weakly interconnected._