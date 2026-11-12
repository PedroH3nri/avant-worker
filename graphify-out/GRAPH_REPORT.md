# Graph Report - avant-worker  (2026-11-12)

## Corpus Check
- 88 files · ~52,329 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 1501 nodes · 3097 edges · 96 communities (57 shown, 39 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 289 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8fd9e9f2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- app.py
- enabled_site
- steps
- Avant: conexão com o GAM
- page_fetcher.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- adapters/__init__.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- clean_code.py
- pytest
- alert_tasks.py
- session-start.sh
- test_database_pool.py
- avant-worker
- Protocol
- datetime
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- conftest.py
- test_commission_tasks.py
- test_mail_tasks.py
- get_services
- _HttpxResponse
- conftest.py
- gam_client.py
- tool_tasks.py
- _last
- updates
- public_address
- MemoryWriter
- network_tasks.py
- price_rule_tasks.py
- _soap_source
- uuid
- logging
- gam_reports.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- test_exchange_rates_tasks.py
- HttpPageFetcher
- checklist_tasks.py
- ad_tag_tasks.py
- _check_on_start
- test_page_fetcher.py
- DeadlineStream
- parse_documents
- FakeSoapClient
- GeoLiteCountries
- reward_tasks.py
- test_ad_tag_tasks.py
- use_services
- network
- mcm_tasks.py
- _route
- pytest
- ._list
- ._first
- _ad_unit
- schedule_tasks.py
- GamTargetNetworkWithTimeZone
- services.py
- dripping_server
- ensure_page_view_partitions_task
- FakeRedis
- Avant: conexão com o GAM
- PageViewSource
- StuckLookup
- RecordingMailer
- test_tasks.py
- FakeTrafficWriter
- test_gam_tool_tasks.py
- purge_tasks.py
- key_value_tasks.py
- _fault
- redis_services
- _HttpxAuthRequest
- source_files
- _error
- redis_services
- .list_child_publishers
- _public_transport
- redis_services

## God Nodes (most connected - your core abstractions)
1. `Services` - 141 edges
2. `get_services()` - 65 edges
3. `company()` - 63 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `MemoryWriter` - 23 edges
7. `enabled_site()` - 20 edges
8. `Settings` - 19 edges
9. `fake()` - 19 edges
10. `_route()` - 18 edges

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

## Communities (96 total, 39 thin omitted)

### Community 2 - "enabled_site"
Cohesion: 0.08
Nodes (22): network(), CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call() (+14 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (38): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+30 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

### Community 5 - "page_fetcher.py"
Cohesion: 0.15
Nodes (3): _resolve(), test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports()

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.13
Nodes (13): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+5 more)

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
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 18 - "test_database_pool.py"
Cohesion: 0.19
Nodes (8): check_database_role(), _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_the_app_role_passes_the_start_check(), test_the_connection_carries_the_worker_name_and_timeouts(), test_the_default_pool_fits_the_connection_budget()

### Community 22 - "Protocol"
Cohesion: 0.12
Nodes (3): EarningsSource, ExchangeRateSource, ReportSource

### Community 23 - "datetime"
Cohesion: 0.13
Nodes (6): months_to_fetch(), _shift(), sync_mcm_earnings(), schedule_page_views(), sync_page_views(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.09
Nodes (14): _clear_queued(), _fan_out(), _mark_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), schedule_metrics() (+6 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "ad_tag_tasks.py"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "conftest.py"
Cohesion: 0.10
Nodes (5): engine(), services(), FakeEarnings, FakeExchangeRates, FakePageViews

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.05
Nodes (23): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+15 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.05
Nodes (13): MaskedRequest, MaskedTask, request_password_reset(), add_user(), count_resets(), RecordingMailer, test_a_retry_publishes_the_email_masked(), test_an_error_that_is_not_temporary_is_not_retried() (+5 more)

### Community 32 - "get_services"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 36 - "tool_tasks.py"
Cohesion: 0.16
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "public_address"
Cohesion: 0.19
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.11
Nodes (10): create_price_rules(), _currency_and_time_zone(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network(), _record_time_zone(), run_price_rules() (+2 more)

### Community 44 - "_soap_source"
Cohesion: 0.11
Nodes (17): FakeReports, reports(), row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue(), test_a_period_already_waiting_in_the_queue_is_not_queued_again() (+9 more)

### Community 45 - "uuid"
Cohesion: 0.12
Nodes (7): refresh_report_preview(), refresh_report_previews(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 46 - "logging"
Cohesion: 0.18
Nodes (4): _refuse_start(), configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 47 - "gam_reports.py"
Cohesion: 0.18
Nodes (7): _ad_unit_path(), _hour(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_parse_report_keeps_groone_try_rows()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "test_exchange_rates_tasks.py"
Cohesion: 0.17
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 54 - "_check_on_start"
Cohesion: 0.19
Nodes (5): _check_on_start(), _failure(), _logging(), _reset_after_fork(), reset_after_fork()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.15
Nodes (10): PublicOnlyBackend, FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect() (+2 more)

### Community 60 - "reward_tasks.py"
Cohesion: 0.10
Nodes (7): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task()

### Community 61 - "test_ad_tag_tasks.py"
Cohesion: 0.26
Nodes (4): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags()

### Community 62 - "use_services"
Cohesion: 0.29
Nodes (3): use_services(), FakeEngine, test_each_forked_child_gets_a_new_pool_without_closing_the_parent()

### Community 63 - "network"
Cohesion: 0.15
Nodes (28): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_stores_the_month_for_networks_in_avant(), backfills(), company(), count(), fake() (+20 more)

### Community 64 - "mcm_tasks.py"
Cohesion: 0.22
Nodes (3): Importação, discover_mcm(), sync_contracts()

### Community 66 - "_route"
Cohesion: 0.15
Nodes (12): _route(), test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_password_reset_task_is_registered_on_the_mail_queue(), test_page_view_tasks_are_registered_on_the_default_queue() (+4 more)

### Community 67 - "pytest"
Cohesion: 0.06
Nodes (18): Onde está o trabalho, ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today(), client(), record(), FakeCredentials (+10 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 71 - "schedule_tasks.py"
Cohesion: 0.20
Nodes (4): get_services(), backfill_metrics(), deliver_reports(), schedule_reports()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 75 - "ensure_page_view_partitions_task"
Cohesion: 0.33
Nodes (3): ensure_page_view_partitions_task(), flush_page_views(), test_partitions_are_created_once()

### Community 77 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 81 - "test_tasks.py"
Cohesion: 0.13
Nodes (8): check_settings(), _mailer(), Settings, test_an_empty_required_variable_does_not_start(), test_every_env_needs_redis_and_resend(), test_the_redis_url_needs_a_redis_scheme(), test_the_worker_does_not_start_without_redis_or_resend(), test_the_worker_mailer_is_always_resend()

### Community 82 - "FakeTrafficWriter"
Cohesion: 0.13
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 83 - "test_gam_tool_tasks.py"
Cohesion: 0.18
Nodes (5): soap_writer(), staff(), test_a_busy_network_waits_and_tries_again(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 85 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 87 - "_fault"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

### Community 98 - "redis_services"
Cohesion: 0.22
Nodes (4): redis_services(), _reward(), test_buffer_becomes_metrics_and_leads(), test_import_forgets_the_latest_reward_pages()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 721 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `network` to `SoapGamWriter`, `enabled_site`, `pytest`, `test_database_pool.py`, `gam_metrics_tasks.py`, `conftest.py`, `test_commission_tasks.py`, `test_mail_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `_soap_source`, `uuid`, `test_exchange_rates_tasks.py`, `HttpPageFetcher`, `ad_tag_tasks.py`, `GeoLiteCountries`, `reward_tasks.py`, `test_ad_tag_tasks.py`, `use_services`, `pytest`, `._list`, `schedule_tasks.py`, `services.py`, `dripping_server`, `ensure_page_view_partitions_task`, `test_tasks.py`, `FakeTrafficWriter`, `test_gam_tool_tasks.py`, `key_value_tasks.py`, `.gam`, `redis_services`, `redis_services`, `redis_services`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Are the 116 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 116 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `schedule_tasks.py` to `commission_tasks.py`, `datetime`, `gam_metrics_tasks.py`, `test_mail_tasks.py`, `get_services`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `uuid`, `test_exchange_rates_tasks.py`, `checklist_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `network`, `mcm_tasks.py`, `services.py`, `ensure_page_view_partitions_task`, `test_tasks.py`, `purge_tasks.py`, `key_value_tasks.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `enabled_site` be split into smaller, more focused modules?**
  _Cohesion score 0.08295625942684766 - nodes in this community are weakly interconnected._