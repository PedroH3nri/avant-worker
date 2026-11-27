# Graph Report - avant-worker  (2026-11-27)

## Corpus Check
- 117 files · ~66,413 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 2070 nodes · 4083 edges · 176 communities (74 shown, 102 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 349 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d117dbd0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- Services
- steps
- gam_writer.py
- page_fetcher.py
- Avant: models do MVP
- commission_tasks.py
- test_gam_client.py
- Avant: endpoints da API do MVP
- tool_tasks.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- password_reset_tasks.py
- clean_code.py
- test_google_ads_tasks.py
- RecordingMailer
- session-start.sh
- get_services
- avant-worker
- .report
- test_earnings_tasks.py
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- facebook_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- company
- test_mail_tasks.py
- app.py
- _HttpxResponse
- FakeGamClient
- _hit
- ReportKind
- test_facebook_tasks.py
- updates
- public_address
- MemoryWriter
- network_tasks.py
- gam_reports.py
- price_rule_tasks.py
- company
- .totals
- services
- exchange_rate_tasks.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- datetime
- _flush
- _route
- ad_tag_tasks.py
- services.py
- test_page_fetcher.py
- DeadlineStream
- gam_client.py
- FakeExchangeRates
- reward_tasks.py
- FakeFacebook
- test_key_value_tasks.py
- test_database_pool.py
- Services
- _route
- collections_abc
- RestGamClient
- ._statement
- _ad_unit
- GamTargetNetworkWithTimeZone
- avant_core_company_models
- dripping_server
- checklist_tasks.py
- FakeLock
- Groone Avant: contexto do projeto
- Settings
- StuckLookup
- notification_tasks.py
- pytest
- soap_writer
- use_services
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- FacebookNotConfigured
- UUID
- logging
- ._create_values
- date
- InvalidVariable
- SoapReportClient
- _HttpxAuthRequest
- FakeGoogleAds
- _public_transport
- test_checklist_tasks.py
- RecordingMailer
- FakeCountries
- test_a_database_error_retries_without_the_email
- FakeCredentials
- fake_gam.py
- datetime
- alert_tasks.py
- test_report_is_read_from_a_temporary_file_as_it_streams
- sync_price_rule_hours
- GoogleAdsNotConfigured
- report_preview_tasks.py
- .exchange_code
- test_commission_tasks.py
- .keywords
- .trusted_uow
- GamNotConfigured
- UUID
- test_exchange_rates_tasks.py
- RedisUsageCounter
- GoogleAdsNotConfigured
- _run
- adapters/__init__.py
- google_ads
- schedule_tasks.py
- _error
- facebook
- _record
- app.py
- page_fetcher.py
- nurture_tasks.py
- _fault
- .report
- months_to_fetch
- test_install_check_tasks.py
- FakeCredentials
- warn_nps_detractors
- CountingFetcher
- test_a_database_error_retries_without_the_email
- .lock
- PageViewSource
- _FixedClock
- avant-worker
- .exchange_rates
- refresh_levels

## God Nodes (most connected - your core abstractions)
1. `Services` - 187 edges
2. `get_services()` - 104 edges
3. `company()` - 70 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 35 edges
6. `FakeGoogleAds` - 33 edges
7. `FakeFacebook` - 29 edges
8. `Settings` - 29 edges
9. `MemoryWriter` - 23 edges
10. `_route()` - 23 edges

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

## Communities (176 total, 102 thin omitted)

### Community 1 - "Services"
Cohesion: 0.12
Nodes (19): FakeEarnings, FakePageViews, test_sync_stores_the_month_for_networks_in_avant(), backfills(), count(), fake(), inventory(), test_check_access_and_schedulers() (+11 more)

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 5 - "page_fetcher.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "test_gam_client.py"
Cohesion: 0.16
Nodes (13): test_fetcher_sends_the_avant_user_agent_and_reads_only_text(), client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "tool_tasks.py"
Cohesion: 0.17
Nodes (4): _import(), run_tool(), _try_later(), _updated()

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

### Community 15 - "test_google_ads_tasks.py"
Cohesion: 0.12
Nodes (10): _count(), _login(), _queued_job(), test_metrics_enforce_the_monthly_limit_and_rules_skip_accounts_without_site(), test_run_job_creates_once_syncs_the_login_and_tells_the_screen(), test_run_job_of_another_company_does_not_call_google(), test_run_job_with_the_lock_taken_tries_again_later(), test_structure_metrics_and_changes_fill_the_company() (+2 more)

### Community 18 - "get_services"
Cohesion: 0.11
Nodes (13): get_services(), run_job(), notify(), run_rules(), schedule_changes(), schedule_metrics(), schedule_rules(), schedule_structure() (+5 more)

### Community 22 - ".report"
Cohesion: 0.17
Nodes (7): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here(), test_the_real_resend_mailer_failing_makes_the_task_try_again()

### Community 23 - "test_earnings_tasks.py"
Cohesion: 0.14
Nodes (5): check_install(), check_site_installs(), daily_install_checks(), _dispatch(), dispatch_install_checks()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.09
Nodes (14): backfill_metrics(), _clear_queued(), _fan_out(), _mark_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network() (+6 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "facebook_tasks.py"
Cohesion: 0.10
Nodes (12): check_tokens(), email_alerts(), run_job(), notify(), run_rules(), schedule_insights(), schedule_rules(), schedule_structure() (+4 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "company"
Cohesion: 0.11
Nodes (25): FakeReports, company(), network(), test_a_busy_network_waits_and_tries_again(), test_connected_networks_reach_the_route(), reports(), row(), _soap_source() (+17 more)

### Community 35 - "_hit"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 36 - "ReportKind"
Cohesion: 0.22
Nodes (4): _read_rows(), report_query(), ReportKind, _soap_date()

### Community 37 - "test_facebook_tasks.py"
Cohesion: 0.07
Nodes (21): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too() (+13 more)

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "public_address"
Cohesion: 0.15
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.13
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - "gam_reports.py"
Cohesion: 0.17
Nodes (4): _ad_unit_path(), _hour(), _integer(), parse_report()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.13
Nodes (8): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), run_price_rules(), _run_site_automatic(), _run_site_cascade(), schedule_price_rule_hours()

### Community 44 - "company"
Cohesion: 0.18
Nodes (9): _count(), _profile(), test_check_tokens_runs_without_profiles(), test_insights_enforce_the_monthly_limit_and_alerts_go_by_email(), test_rules_run_without_rules(), test_run_job_duplicates_once_and_tells_the_screen(), test_structure_then_insights_fill_the_company(), test_sync_profile_is_idempotent() (+1 more)

### Community 45 - ".totals"
Cohesion: 0.18
Nodes (3): day_key(), days_key(), usage_day_of()

### Community 46 - "services"
Cohesion: 0.22
Nodes (5): use_services(), engine(), services(), FakeEngine, test_each_forked_child_gets_a_new_pool_without_closing_the_parent()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.22
Nodes (8): Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11), Resumo, Serviços e ferramentas

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.14
Nodes (13): Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões (+5 more)

### Community 52 - "_route"
Cohesion: 0.17
Nodes (11): _route(), test_checklist_tasks_are_registered(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_password_reset_task_is_registered_on_the_mail_queue(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_price_rule_tasks_are_registered() (+3 more)

### Community 53 - "ad_tag_tasks.py"
Cohesion: 0.17
Nodes (4): ensure_page_view_partitions_task(), flush_page_views(), forget_network_ad_tags(), _received_at()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.17
Nodes (8): FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect(), test_slow_dns_counts_against_the_total_deadline()

### Community 57 - "gam_client.py"
Cohesion: 0.13
Nodes (3): _delegation(), _last(), _revshare()

### Community 60 - "reward_tasks.py"
Cohesion: 0.11
Nodes (7): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task()

### Community 62 - "test_key_value_tasks.py"
Cohesion: 0.13
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 63 - "test_database_pool.py"
Cohesion: 0.19
Nodes (8): check_database_role(), _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_the_app_role_passes_the_start_check(), test_the_connection_carries_the_worker_name_and_timeouts(), test_the_default_pool_fits_the_connection_budget()

### Community 64 - "Services"
Cohesion: 0.08
Nodes (11): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), staff(), test_run_tool_configures_the_network(), _seed(), test_daily_checks_fetch_each_page_once() (+3 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "dripping_server"
Cohesion: 0.18
Nodes (4): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 75 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 77 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Como trabalhar nos repositórios, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação (+6 more)

### Community 78 - "Settings"
Cohesion: 0.11
Nodes (9): check_settings(), _refuse_start(), _refuse_start_for(), _mailer(), _redis_client(), Settings, test_the_redis_client_has_short_socket_timeouts(), test_the_worker_starts_with_resend() (+1 more)

### Community 81 - "pytest"
Cohesion: 0.17
Nodes (14): clean_env(), _stopped_names(), test_a_broken_smtp_url_does_not_start_and_hides_the_password(), test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_integration_variable_turns_the_integration_off(), test_an_empty_resend_key_is_named_in_the_error(), test_an_empty_variable_does_not_start(), test_an_invalid_smtp_url_fails_in_the_settings_showing_only_the_name() (+6 more)

### Community 82 - "soap_writer"
Cohesion: 0.12
Nodes (3): FakeNurtureMailer, test_nurture_runs_every_hour_on_the_default_queue(), test_run_sends_each_email_once_and_reads_the_status()

### Community 83 - "use_services"
Cohesion: 0.13
Nodes (11): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+3 more)

### Community 87 - "UUID"
Cohesion: 0.21
Nodes (5): _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 88 - "logging"
Cohesion: 0.21
Nodes (3): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 95 - "_public_transport"
Cohesion: 0.22
Nodes (3): _public_transport(), PublicOnlyBackend, test_fetcher_never_connects_to_internal_addresses_or_other_ports()

### Community 96 - "test_checklist_tasks.py"
Cohesion: 0.10
Nodes (5): FakePageFetcher, redis_services(), _reward(), test_buffer_becomes_metrics_and_leads(), test_import_forgets_the_latest_reward_pages()

### Community 97 - "RecordingMailer"
Cohesion: 0.27
Nodes (5): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags(), test_partitions_are_created_once()

### Community 100 - "FakeCredentials"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 101 - "fake_gam.py"
Cohesion: 0.10
Nodes (10): _client(), test_followups_do_nothing_without_the_token(), test_followups_go_to_the_hubspot_queue_every_15_minutes(), test_hubspot_tasks_go_to_their_queue(), test_monthly_sync_is_scheduled_daily(), test_monthly_sync_runs_right_after_the_routine(), test_network_error_becomes_one_task_on_the_client_contact(), test_requested_sync_runs_and_a_refused_token_fails_the_run() (+2 more)

### Community 102 - "datetime"
Cohesion: 0.22
Nodes (4): soap_writer(), test_tool_task_is_registered(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 103 - "alert_tasks.py"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 107 - "GoogleAdsNotConfigured"
Cohesion: 0.25
Nodes (4): _currency_and_time_zone(), _reads_groone_network(), _record_time_zone(), sync_price_rule_hours()

### Community 109 - ".exchange_code"
Cohesion: 0.40
Nodes (4): 20. CDN dos scripts do site (cdn.groone.com), Chamadas da API e nome dos scripts (Pedro, 23/11, 23h52), Como fica no ar (proposta para o avant-infra), O que ficou decidido

### Community 110 - "test_commission_tasks.py"
Cohesion: 0.18
Nodes (4): FixedClock, test_a_busy_lock_skips_the_run(), test_closing_warns_on_the_20th_when_the_month_is_still_open(), test_commission_tasks_are_registered_on_the_default_queue()

### Community 111 - ".keywords"
Cohesion: 0.40
Nodes (4): 19. Cliente e Empresa em dois cadastros, Migrations, O que ficou decidido, Painel

### Community 112 - ".trusted_uow"
Cohesion: 0.19
Nodes (6): earnings(), seller_scenario(), test_closing_the_current_month_is_refused(), test_last_month_closes_after_its_earnings_arrive(), test_the_daily_run_fills_every_open_day(), test_today_is_calculated_and_the_month_closes()

### Community 114 - "UUID"
Cohesion: 0.31
Nodes (5): text(), test_purge_removes_only_notifications_older_than_30_days(), test_detractor_reaches_the_manager_once(), test_purge_expired(), test_flush_writes_the_day_totals_once()

### Community 115 - "test_exchange_rates_tasks.py"
Cohesion: 0.29
Nodes (3): test_client_reads_rates_as_decimals_and_fails_clearly(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 116 - "RedisUsageCounter"
Cohesion: 0.12
Nodes (4): RedisUsageCounter, flush_usage(), purge_usage(), test_usage_tasks_are_scheduled_on_the_default_queue()

### Community 119 - "adapters/__init__.py"
Cohesion: 0.16
Nodes (5): channel(), publish(), schedule_page_views(), sync_page_views(), test_check_install_saves_and_tells_the_screen()

### Community 125 - "_record"
Cohesion: 0.43
Nodes (3): _record(), test_log_keeps_ordinary_messages(), test_log_masks_database_values_in_message_and_stack()

### Community 127 - "app.py"
Cohesion: 0.10
Nodes (8): _check_on_start(), create_app(), _failure(), _logging(), _reset_after_fork(), _variable_names(), reset_after_fork(), BrokerSettings

### Community 132 - "_fault"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

### Community 135 - "months_to_fetch"
Cohesion: 0.27
Nodes (3): months_to_fetch(), _shift(), sync_mcm_earnings()

### Community 142 - "test_a_database_error_retries_without_the_email"
Cohesion: 0.29
Nodes (3): test_a_database_error_retries_without_the_email(), test_a_retry_publishes_the_email_masked(), capture()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1032 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **102 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `nurture_tasks.py`, `Services`, `page_fetcher.py`, `tool_tasks.py`, `.lock`, `test_google_ads_tasks.py`, `get_services`, `.report`, `test_earnings_tasks.py`, `gam_metrics_tasks.py`, `services.py`, `company`, `test_facebook_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `company`, `.exchange_rates`, `services`, `_flush`, `ad_tag_tasks.py`, `reward_tasks.py`, `test_key_value_tasks.py`, `test_database_pool.py`, `RestGamClient`, `Settings`, `soap_writer`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`, `FacebookNotConfigured`, `UUID`, `._create_values`, `test_checklist_tasks.py`, `RecordingMailer`, `FakeCountries`, `fake_gam.py`, `GoogleAdsNotConfigured`, `test_commission_tasks.py`, `.trusted_uow`, `GamNotConfigured`, `UUID`, `test_exchange_rates_tasks.py`, `GoogleAdsNotConfigured`, `_run`, `adapters/__init__.py`, `google_ads`, `facebook`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Are the 142 inferred relationships involving `Services` (e.g. with `RestGamClient` and `Settings`) actually correct?**
  _`Services` has 142 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `nurture_tasks.py`, `page_fetcher.py`, `commission_tasks.py`, `months_to_fetch`, `tool_tasks.py`, `warn_nps_detractors`, `password_reset_tasks.py`, `test_earnings_tasks.py`, `gam_metrics_tasks.py`, `facebook_tasks.py`, `services.py`, `network_tasks.py`, `price_rule_tasks.py`, `exchange_rate_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `Services`, `_route`, `checklist_tasks.py`, `Settings`, `notification_tasks.py`, `use_services`, `alert_tasks.py`, `sync_price_rule_hours`, `GoogleAdsNotConfigured`, `report_preview_tasks.py`, `RedisUsageCounter`, `adapters/__init__.py`, `schedule_tasks.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Services` be split into smaller, more focused modules?**
  _Cohesion score 0.11794871794871795 - nodes in this community are weakly interconnected._