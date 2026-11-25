# Graph Report - avant-worker  (2026-11-25)

## Corpus Check
- 100 files · ~60,940 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 1826 nodes · 3673 edges · 148 communities (72 shown, 76 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 322 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec3c926c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- test_gam_tasks.py
- enabled_site
- steps
- gam_writer.py
- key_value_tasks.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- tool_tasks.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- password_reset_tasks.py
- clean_code.py
- Settings
- OpenExchangeRates
- session-start.sh
- get_services
- avant-worker
- .report
- install_check_tasks.py
- gam_metrics_tasks.py
- test_gam_tool_tasks.py
- .list_mcm_earnings
- facebook_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- test_commission_tasks.py
- test_mail_tasks.py
- _HttpxResponse
- FakeGamClient
- _hit
- ReportKind
- test_facebook_tasks.py
- updates
- page_fetcher.py
- MemoryWriter
- network_tasks.py
- gam_reports.py
- price_rule_tasks.py
- Services
- test_ad_tag_tasks.py
- _route
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- test_gam_client.py
- test_install_check_tasks.py
- uuid
- ad_tag_tasks.py
- mcm_tasks.py
- test_page_fetcher.py
- DeadlineStream
- gam_client.py
- schedule_tasks.py
- reward_tasks.py
- FakeFacebook
- test_key_value_tasks.py
- test_database_pool.py
- test_google_ads_tasks.py
- fake_gam.py
- collections_abc
- RestGamClient
- ._statement
- _ad_unit
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- GamTargetNetworkWithTimeZone
- exchange_rate_tasks.py
- HttpPageFetcher
- checklist_tasks.py
- FakeLock
- purge_expired
- InvalidVariable
- StuckLookup
- metrics/__init__.py
- pytest
- soap_writer
- services
- adapters/__init__.py
- FacebookNotConfigured
- alert_tasks.py
- FakeCountries
- ReportKind
- metrics/__init__.py
- logging
- SoapReportClient
- _HttpxAuthRequest
- FakeGoogleAds
- PublicOnlyBackend
- MaskedRequest
- RecordingMailer
- _FixedClock
- test_a_database_error_retries_without_the_email
- FakeCredentials
- test_page_fetcher.py
- GeoLiteCountries
- app.py
- MonkeyPatch
- _error
- GoogleAdsNotConfigured
- test_report_is_read_from_a_temporary_file_as_it_streams
- 20. CDN dos scripts do site (cdn.groone.com)
- typing
- 19. Cliente e Empresa em dois cadastros
- test_reward_tasks.py
- facebook
- forget_latest_reward_pages
- Avant: conexão com o GAM
- avant-worker
- price_rules/__init__.py
- sync_price_rule_hours
- _run
- google_ads
- FixedClock
- BrokerSettings
- .lock
- FakePageFetcher
- avant-worker
- _variable_names
- clean_env
- test_fetcher_never_connects_to_internal_addresses_or_other_ports

## God Nodes (most connected - your core abstractions)
1. `Services` - 172 edges
2. `get_services()` - 87 edges
3. `company()` - 70 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `FakeFacebook` - 29 edges
7. `Settings` - 25 edges
8. `MemoryWriter` - 23 edges
9. `enabled_site()` - 21 edges
10. `_route()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam/mcm_tasks.py
- `test_partitions_are_created_once()` --uses--> `Services`  [INFERRED]
  tests/test_ad_tag_tasks.py → src/avant_worker/services.py
- `test_a_busy_lock_skips_the_run()` --uses--> `Services`  [INFERRED]
  tests/test_commission_tasks.py → src/avant_worker/services.py
- `test_the_connection_carries_the_worker_name_and_timeouts()` --uses--> `Services`  [INFERRED]
  tests/test_database_pool.py → src/avant_worker/services.py
- `test_sync_without_key_does_nothing()` --uses--> `Services`  [INFERRED]
  tests/test_exchange_rates_tasks.py → src/avant_worker/services.py

## Import Cycles
- None detected.

## Communities (148 total, 76 thin omitted)

### Community 1 - "test_gam_tasks.py"
Cohesion: 0.13
Nodes (19): backfills(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network(), test_failed_check_stops_before_importing() (+11 more)

### Community 2 - "enabled_site"
Cohesion: 0.07
Nodes (18): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_create_price_rules_keeps_the_count_when_a_cascade_fails(), test_hourly_query_and_parse_keep_only_content_hash() (+10 more)

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 5 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.16
Nodes (8): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late()

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Como trabalhar nos repositórios, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "tool_tasks.py"
Cohesion: 0.16
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

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
Cohesion: 0.14
Nodes (7): check_file(), docstring_problems(), inline_comments(), is_exempt(), main(), single_letter_names(), source_files()

### Community 15 - "Settings"
Cohesion: 0.16
Nodes (8): check_settings(), _mailer(), _redis_client(), Settings, engine(), test_the_redis_client_has_short_socket_timeouts(), test_the_worker_starts_with_resend(), test_the_worker_starts_with_smtp()

### Community 18 - "get_services"
Cohesion: 0.15
Nodes (8): get_services(), schedule_changes(), schedule_metrics(), schedule_structure(), sync_changes(), sync_login(), sync_metrics(), test_tasks_go_to_the_google_ads_queue_and_retry_on_unavailable()

### Community 22 - ".report"
Cohesion: 0.13
Nodes (3): EarningsSource, ExchangeRateSource, PageViewSource

### Community 23 - "install_check_tasks.py"
Cohesion: 0.15
Nodes (5): check_install(), check_site_installs(), daily_install_checks(), _dispatch(), dispatch_install_checks()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.12
Nodes (9): _clear_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store(), sync_metrics(), _sync_metrics() (+1 more)

### Community 25 - "test_gam_tool_tasks.py"
Cohesion: 0.28
Nodes (3): staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network()

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.18
Nodes (4): _delegation(), _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "facebook_tasks.py"
Cohesion: 0.10
Nodes (12): check_tokens(), email_alerts(), run_job(), notify(), run_rules(), schedule_insights(), schedule_rules(), schedule_structure() (+4 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.13
Nodes (9): _flush(), refresh_levels(), earnings(), seller_scenario(), test_a_busy_lock_skips_the_run(), test_closing_the_current_month_is_refused(), test_last_month_closes_after_its_earnings_arrive(), test_the_daily_run_fills_every_open_day() (+1 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.17
Nodes (8): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_password_reset_task_is_registered_on_the_mail_queue(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here(), test_the_real_resend_mailer_failing_makes_the_task_try_again()

### Community 35 - "_hit"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 36 - "ReportKind"
Cohesion: 0.27
Nodes (3): _read_rows(), report_query(), _soap_date()

### Community 37 - "test_facebook_tasks.py"
Cohesion: 0.18
Nodes (9): _count(), _profile(), test_check_tokens_runs_without_profiles(), test_insights_enforce_the_monthly_limit_and_alerts_go_by_email(), test_rules_run_without_rules(), test_run_job_duplicates_once_and_tells_the_screen(), test_structure_then_insights_fill_the_company(), test_sync_profile_is_idempotent() (+1 more)

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "page_fetcher.py"
Cohesion: 0.20
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - "gam_reports.py"
Cohesion: 0.14
Nodes (4): _ad_unit_path(), _hour(), _integer(), parse_report()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.19
Nodes (5): _forget_cascades(), _forget_floors(), run_price_rules(), _run_site_automatic(), _run_site_cascade()

### Community 44 - "Services"
Cohesion: 0.18
Nodes (23): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_stores_the_month_for_networks_in_avant(), company(), network(), test_connected_networks_reach_the_route(), reports() (+15 more)

### Community 45 - "test_ad_tag_tasks.py"
Cohesion: 0.18
Nodes (5): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags(), test_partitions_are_created_once()

### Community 47 - "_route"
Cohesion: 0.06
Nodes (15): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue() (+7 more)

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.22
Nodes (8): Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11), Resumo, Serviços e ferramentas

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.14
Nodes (13): Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões (+5 more)

### Community 50 - "test_gam_client.py"
Cohesion: 0.17
Nodes (13): test_client_reads_rates_as_decimals_and_fails_clearly(), client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 51 - "test_install_check_tasks.py"
Cohesion: 0.13
Nodes (5): CountingFetcher, _seed(), test_check_install_saves_and_tells_the_screen(), test_daily_checks_fetch_each_page_once(), test_install_tasks_are_registered()

### Community 52 - "uuid"
Cohesion: 0.12
Nodes (8): refresh_report_preview(), refresh_report_previews(), test_purge_expired(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 53 - "ad_tag_tasks.py"
Cohesion: 0.16
Nodes (4): ensure_page_view_partitions_task(), flush_page_views(), forget_network_ad_tags(), _received_at()

### Community 54 - "mcm_tasks.py"
Cohesion: 0.22
Nodes (3): Importação, discover_mcm(), sync_contracts()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.21
Nodes (8): PublicOnlyBackend, FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect()

### Community 60 - "reward_tasks.py"
Cohesion: 0.19
Nodes (3): _batch(), _event(), _lead()

### Community 62 - "test_key_value_tasks.py"
Cohesion: 0.12
Nodes (6): FakeTrafficWriter, redis_services(), test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 63 - "test_database_pool.py"
Cohesion: 0.18
Nodes (8): check_database_role(), _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_the_app_role_passes_the_start_check(), test_the_connection_carries_the_worker_name_and_timeouts(), test_the_default_pool_fits_the_connection_budget()

### Community 64 - "test_google_ads_tasks.py"
Cohesion: 0.17
Nodes (4): _count(), _login(), test_structure_metrics_and_changes_fill_the_company(), test_unavailable_is_retried()

### Community 66 - "fake_gam.py"
Cohesion: 0.14
Nodes (5): services(), FakeEarnings, FakeExchangeRates, FakePageViews, FakeReports

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "HttpPageFetcher"
Cohesion: 0.18
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 75 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 80 - "metrics/__init__.py"
Cohesion: 0.29
Nodes (3): months_to_fetch(), _shift(), sync_mcm_earnings()

### Community 81 - "pytest"
Cohesion: 0.25
Nodes (10): _stopped_names(), test_a_broken_smtp_url_does_not_start_and_hides_the_password(), test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_variable_does_not_start(), test_an_invalid_smtp_url_fails_in_the_settings_showing_only_the_name(), test_an_unknown_transport_does_not_start(), test_each_transport_needs_its_own_configuration(), test_the_redis_url_needs_a_redis_scheme() (+2 more)

### Community 82 - "soap_writer"
Cohesion: 0.10
Nodes (9): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+1 more)

### Community 83 - "services"
Cohesion: 0.29
Nodes (3): use_services(), FakeEngine, test_each_forked_child_gets_a_new_pool_without_closing_the_parent()

### Community 84 - "adapters/__init__.py"
Cohesion: 0.17
Nodes (3): channel(), publish(), ExchangeRatesUnavailable

### Community 87 - "alert_tasks.py"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 90 - "metrics/__init__.py"
Cohesion: 0.13
Nodes (7): backfill_metrics(), _fan_out(), _mark_queued(), schedule_metrics(), schedule_reprocess(), schedule_page_views(), sync_page_views()

### Community 91 - "logging"
Cohesion: 0.11
Nodes (8): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing(), _record(), test_log_keeps_ordinary_messages(), test_log_masks_database_values_in_message_and_stack()

### Community 99 - "test_a_database_error_retries_without_the_email"
Cohesion: 0.29
Nodes (3): test_a_database_error_retries_without_the_email(), test_a_retry_publishes_the_email_masked(), capture()

### Community 101 - "test_page_fetcher.py"
Cohesion: 0.17
Nodes (5): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_dns_counts_against_the_total_deadline(), test_slow_headers_count_against_the_total_deadline()

### Community 103 - "app.py"
Cohesion: 0.11
Nodes (7): _check_on_start(), _failure(), _logging(), _refuse_start(), _refuse_start_for(), _reset_after_fork(), reset_after_fork()

### Community 104 - "MonkeyPatch"
Cohesion: 0.19
Nodes (7): _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_report_with_only_the_header_is_an_empty_period(), test_a_report_without_the_csv_header_is_a_temporary_failure(), test_a_temporary_failure_that_will_be_retried_keeps_the_queue_mark(), test_report_downloads_before_the_rows_are_read(), test_the_downloaded_file_closes_even_if_nobody_reads_it()

### Community 109 - "20. CDN dos scripts do site (cdn.groone.com)"
Cohesion: 0.40
Nodes (4): 20. CDN dos scripts do site (cdn.groone.com), Chamadas da API e nome dos scripts (Pedro, 23/11, 23h52), Como fica no ar (proposta para o avant-infra), O que ficou decidido

### Community 111 - "19. Cliente e Empresa em dois cadastros"
Cohesion: 0.40
Nodes (4): 19. Cliente e Empresa em dois cadastros, Migrations, O que ficou decidido, Painel

### Community 112 - "test_reward_tasks.py"
Cohesion: 0.18
Nodes (4): redis_services(), _reward(), test_buffer_becomes_metrics_and_leads(), test_import_forgets_the_latest_reward_pages()

### Community 115 - "forget_latest_reward_pages"
Cohesion: 0.22
Nodes (3): flush_reward_events(), forget_latest_reward_pages(), purge_reward_batches_task()

### Community 116 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 117 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 119 - "price_rules/__init__.py"
Cohesion: 0.28
Nodes (3): create_price_rules(), maintain_price_rule_partitions(), schedule_price_rule_hours()

### Community 120 - "sync_price_rule_hours"
Cohesion: 0.25
Nodes (4): _currency_and_time_zone(), _reads_groone_network(), _record_time_zone(), sync_price_rule_hours()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 902 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **76 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `.lock`, `test_gam_tasks.py`, `.uow`, `enabled_site`, `key_value_tasks.py`, `tool_tasks.py`, `Settings`, `OpenExchangeRates`, `get_services`, `install_check_tasks.py`, `gam_metrics_tasks.py`, `test_gam_tool_tasks.py`, `services.py`, `test_commission_tasks.py`, `test_mail_tasks.py`, `test_facebook_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `test_ad_tag_tasks.py`, `.gam`, `test_install_check_tasks.py`, `uuid`, `ad_tag_tasks.py`, `reward_tasks.py`, `test_key_value_tasks.py`, `test_database_pool.py`, `test_google_ads_tasks.py`, `fake_gam.py`, `collections_abc`, `RestGamClient`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`, `HttpPageFetcher`, `services`, `FacebookNotConfigured`, `FakeCountries`, `metrics/__init__.py`, `logging`, `SoapReportClient`, `test_page_fetcher.py`, `GeoLiteCountries`, `MonkeyPatch`, `GoogleAdsNotConfigured`, `test_reward_tasks.py`, `facebook`, `forget_latest_reward_pages`, `sync_price_rule_hours`, `_run`, `google_ads`, `FixedClock`?**
  _High betweenness centrality (0.222) - this node is a cross-community bridge._
- **Are the 138 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 138 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `gam_writer.py`, `key_value_tasks.py`, `commission_tasks.py`, `tool_tasks.py`, `password_reset_tasks.py`, `Settings`, `install_check_tasks.py`, `gam_metrics_tasks.py`, `facebook_tasks.py`, `services.py`, `network_tasks.py`, `price_rule_tasks.py`, `Services`, `uuid`, `ad_tag_tasks.py`, `mcm_tasks.py`, `schedule_tasks.py`, `reward_tasks.py`, `exchange_rate_tasks.py`, `checklist_tasks.py`, `purge_expired`, `metrics/__init__.py`, `adapters/__init__.py`, `alert_tasks.py`, `metrics/__init__.py`, `logging`, `app.py`, `forget_latest_reward_pages`, `price_rules/__init__.py`, `sync_price_rule_hours`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_gam_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13174603174603175 - nodes in this community are weakly interconnected._