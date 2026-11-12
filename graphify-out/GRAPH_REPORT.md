# Graph Report - avant-worker  (2026-11-12)

## Corpus Check
- 88 files · ~52,694 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 1514 nodes · 3122 edges · 102 communities (59 shown, 43 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 296 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `396c63e3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- app.py
- enabled_site
- steps
- ReportKind
- page_fetcher.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- publish
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- password_reset_tasks.py
- clean_code.py
- pytest
- FakeExchangeRates
- session-start.sh
- test_database_pool.py
- avant-worker
- Protocol
- mcm_earnings_tasks.py
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- services.py
- test_commission_tasks.py
- test_mail_tasks.py
- get_services
- _HttpxResponse
- conftest.py
- _FixedClock
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
- Settings
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
- test_gam_tool_tasks.py
- GeoLiteCountries
- reward_tasks.py
- _tag
- use_services
- network
- mcm_tasks.py
- test_schedule_tasks.py
- test_gam_client.py
- ._first
- _ad_unit
- schedule_tasks.py
- GamTargetNetworkWithTimeZone
- gam_reports.py
- dripping_server
- ensure_page_view_partitions_task
- FakeRedis
- Avant: conexão com o GAM
- OpenExchangeRates
- StuckLookup
- adapters/__init__.py
- pytest
- FakeTrafficWriter
- company
- purge_tasks.py
- key_value_tasks.py
- RestGamClient
- report_preview_tasks.py
- redis_services
- _HttpxAuthRequest
- source_files
- _error
- redis_services
- .list_child_publishers
- _batch
- _public_transport
- MaskedRequest
- RecordingMailer
- test_exchange_rates_tasks.py
- test_a_database_error_retries_without_the_email
- FakeCredentials
- _refuse_start

## God Nodes (most connected - your core abstractions)
1. `Services` - 142 edges
2. `get_services()` - 65 edges
3. `company()` - 63 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `MemoryWriter` - 23 edges
7. `Settings` - 22 edges
8. `enabled_site()` - 20 edges
9. `fake()` - 19 edges
10. `_route()` - 18 edges

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

## Communities (102 total, 43 thin omitted)

### Community 2 - "enabled_site"
Cohesion: 0.09
Nodes (20): CurrencyWriter, days_ago(), enabled_site(), hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too(), test_create_price_rules_keeps_the_count_when_a_cascade_fails() (+12 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (38): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+30 more)

### Community 4 - "ReportKind"
Cohesion: 0.09
Nodes (13): _ad_unit_path(), _hour(), _integer(), parse_report(), _read_rows(), report_query(), ReportKind, _soap_date() (+5 more)

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

### Community 10 - "publish"
Cohesion: 0.19
Nodes (4): channel(), publish(), schedule_page_views(), sync_page_views()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "password_reset_tasks.py"
Cohesion: 0.15
Nodes (3): request_password_reset(), TemporaryDatabaseError, test_the_email_never_reaches_the_celery_log_or_events()

### Community 14 - "clean_code.py"
Cohesion: 0.18
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 18 - "test_database_pool.py"
Cohesion: 0.18
Nodes (8): check_database_role(), _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_the_app_role_passes_the_start_check(), test_the_connection_carries_the_worker_name_and_timeouts(), test_the_default_pool_fits_the_connection_budget()

### Community 22 - "Protocol"
Cohesion: 0.10
Nodes (3): EarningsSource, ExchangeRateSource, PageViewSource

### Community 23 - "mcm_earnings_tasks.py"
Cohesion: 0.21
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.08
Nodes (15): backfill_metrics(), _clear_queued(), _fan_out(), _mark_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network() (+7 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "ad_tag_tasks.py"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "services.py"
Cohesion: 0.10
Nodes (3): FakeEarnings, FakePageViews, FakeReports

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.06
Nodes (22): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+14 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.18
Nodes (7): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here(), test_the_real_resend_mailer_failing_makes_the_task_try_again()

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
Nodes (9): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network(), _record_time_zone(), run_price_rules(), schedule_price_rule_hours() (+1 more)

### Community 44 - "_soap_source"
Cohesion: 0.11
Nodes (19): network(), test_connected_networks_reach_the_route(), reports(), row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue() (+11 more)

### Community 45 - "uuid"
Cohesion: 0.20
Nodes (6): test_purge_expired(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 46 - "logging"
Cohesion: 0.20
Nodes (3): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 47 - "Settings"
Cohesion: 0.22
Nodes (5): _mailer(), _redis_client(), Settings, test_the_redis_client_has_short_socket_timeouts(), test_the_worker_mailer_is_always_resend()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "test_exchange_rates_tasks.py"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "ad_tag_tasks.py"
Cohesion: 0.22
Nodes (3): forget_network_ad_tags(), _received_at(), test_import_forgets_the_network_tags()

### Community 54 - "_check_on_start"
Cohesion: 0.16
Nodes (6): _check_on_start(), check_settings(), _failure(), _logging(), _reset_after_fork(), reset_after_fork()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.15
Nodes (10): PublicOnlyBackend, FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect() (+2 more)

### Community 58 - "test_gam_tool_tasks.py"
Cohesion: 0.09
Nodes (9): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+1 more)

### Community 60 - "reward_tasks.py"
Cohesion: 0.12
Nodes (6): _flush(), flush_reward_events(), forget_latest_reward_pages(), purge_reward_batches_task(), redis_services(), test_buffer_becomes_metrics_and_leads()

### Community 62 - "use_services"
Cohesion: 0.22
Nodes (5): use_services(), engine(), services(), FakeEngine, test_each_forked_child_gets_a_new_pool_without_closing_the_parent()

### Community 63 - "network"
Cohesion: 0.20
Nodes (19): Services, test_sync_stores_the_month_for_networks_in_avant(), backfills(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history() (+11 more)

### Community 64 - "mcm_tasks.py"
Cohesion: 0.24
Nodes (3): get_services(), discover_mcm(), sync_contracts()

### Community 66 - "test_schedule_tasks.py"
Cohesion: 0.07
Nodes (13): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_password_reset_task_is_registered_on_the_mail_queue() (+5 more)

### Community 67 - "test_gam_client.py"
Cohesion: 0.18
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 75 - "ensure_page_view_partitions_task"
Cohesion: 0.28
Nodes (4): ensure_page_view_partitions_task(), flush_page_views(), test_buffer_becomes_page_views_and_health(), test_partitions_are_created_once()

### Community 77 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 81 - "pytest"
Cohesion: 0.29
Nodes (5): test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_required_variable_does_not_start(), test_the_redis_url_needs_a_redis_scheme(), test_the_worker_does_not_start_without_redis_or_resend(), test_the_worker_needs_redis_and_resend()

### Community 82 - "FakeTrafficWriter"
Cohesion: 0.13
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 83 - "company"
Cohesion: 0.13
Nodes (12): test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), company(), test_discover_mcm_activates_the_registered_network(), staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network(), test_sync_metrics_skips_manage_inventory_and_records_permanent_errors() (+4 more)

### Community 85 - "key_value_tasks.py"
Cohesion: 0.15
Nodes (5): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks(), _currency_and_time_zone()

### Community 94 - "_batch"
Cohesion: 0.22
Nodes (3): _batch(), _event(), _lead()

### Community 98 - "test_exchange_rates_tasks.py"
Cohesion: 0.22
Nodes (4): test_client_reads_rates_as_decimals_and_fails_clearly(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 726 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `network` to `SoapGamWriter`, `enabled_site`, `pytest`, `test_database_pool.py`, `gam_metrics_tasks.py`, `services.py`, `test_commission_tasks.py`, `test_mail_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `_soap_source`, `uuid`, `Settings`, `HttpPageFetcher`, `ad_tag_tasks.py`, `GeoLiteCountries`, `reward_tasks.py`, `_tag`, `use_services`, `mcm_tasks.py`, `gam_reports.py`, `dripping_server`, `ensure_page_view_partitions_task`, `OpenExchangeRates`, `adapters/__init__.py`, `FakeTrafficWriter`, `company`, `key_value_tasks.py`, `RestGamClient`, `redis_services`, `redis_services`, `test_exchange_rates_tasks.py`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Are the 117 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 117 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `mcm_tasks.py` to `commission_tasks.py`, `publish`, `password_reset_tasks.py`, `mcm_earnings_tasks.py`, `gam_metrics_tasks.py`, `services.py`, `get_services`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `Settings`, `test_exchange_rates_tasks.py`, `checklist_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `network`, `schedule_tasks.py`, `gam_reports.py`, `ensure_page_view_partitions_task`, `purge_tasks.py`, `key_value_tasks.py`, `report_preview_tasks.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `enabled_site` be split into smaller, more focused modules?**
  _Cohesion score 0.09191583610188261 - nodes in this community are weakly interconnected._