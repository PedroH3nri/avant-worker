# Graph Report - avant-worker  (2026-11-27)

## Corpus Check
- 132 files · ~68,433 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 2111 nodes · 4231 edges · 146 communities (72 shown, 74 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 348 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f1b510c6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- company
- datetime
- steps
- gam_writer.py
- key_value_tasks.py
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
- google_ads_tasks.py
- avant-worker
- test_mail_tasks.py
- install_check_tasks.py
- gam_metrics_tasks.py
- portfolio_health_tasks.py
- .list_mcm_earnings
- get_services
- Avant: grupos na Empresa e imagem da Empresa
- services.py
- test_metrics_tasks.py
- ExchangeRateSource
- exchange_rates.py
- _HttpxResponse
- FakeGamClient
- test_hubspot_tasks.py
- ReportKind
- test_price_rule_tasks.py
- updates
- page_fetcher.py
- MemoryWriter
- network_tasks.py
- test_install_check_tasks.py
- price_rule_tasks.py
- test_facebook_tasks.py
- test_page_fetcher.py
- FakePageFetcher
- test_exchange_rates_tasks.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- nurture_tasks.py
- fake_gam.py
- test_key_value_tasks.py
- ad_tag_tasks.py
- FakeHubspot
- test_page_fetcher.py
- DeadlineStream
- gam_client.py
- metrics/__init__.py
- reward_tasks.py
- FakeFacebook
- test_reward_tasks.py
- test_database_pool.py
- Services
- datetime
- avant_core_metrics_models
- RestGamClient
- ._statement
- _ad_unit
- GamTargetNetworkWithTimeZone
- test_notification_tasks.py
- .fetch
- redis_services
- FakeLock
- Groone Avant: contexto do projeto
- Settings
- StuckLookup
- notification_tasks.py
- pytest
- FakeNurtureMailer
- Avant: conexão com o GAM
- purge_tasks.py
- FacebookNotConfigured
- checklist_tasks.py
- logging
- datetime
- InvalidVariable
- SoapReportClient
- _HttpxAuthRequest
- FakeGoogleAds
- _public_transport
- test_ad_tag_tasks.py
- UUID
- ReportKind
- report_preview_tasks.py
- avant-worker
- FakeSoapClient
- test_gam_tool_tasks.py
- alert_tasks.py
- test_report_is_read_from_a_temporary_file_as_it_streams
- _hit
- activation_tasks.py
- 20. CDN dos scripts do site (cdn.groone.com)
- MaskedRequest
- 19. Cliente e Empresa em dois cadastros
- .trusted_uow
- test_earnings_tasks.py
- RecordingMailer
- _route
- usage_counter.py
- GoogleAdsNotConfigured
- .uow
- adapters/__init__.py
- price_rules/__init__.py
- schedule_tasks.py
- test_nurture_tasks.py
- nps_tasks.py
- Protocol
- opportunity_tasks.py
- site_integrity_tasks.py
- app.py
- .page_fetcher
- flush_page_views
- sync_price_rule_hours
- _fault
- test_a_database_error_retries_without_the_email
- .report
- _flush
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- google_ads
- redis_services

## God Nodes (most connected - your core abstractions)
1. `Services` - 198 edges
2. `get_services()` - 114 edges
3. `company()` - 70 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `FakeGoogleAds` - 33 edges
7. `FakeFacebook` - 29 edges
8. `Settings` - 29 edges
9. `_route()` - 23 edges
10. `MemoryWriter` - 23 edges

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

## Communities (146 total, 74 thin omitted)

### Community 1 - "company"
Cohesion: 0.22
Nodes (20): FakePageViews, test_sync_stores_the_month_for_networks_in_avant(), backfills(), company(), count(), fake(), inventory(), test_check_access_and_schedulers() (+12 more)

### Community 2 - "datetime"
Cohesion: 0.22
Nodes (3): test_alert_tasks_are_registered_on_their_queues(), test_report_preview_tasks_are_registered_on_the_default_queue(), test_schedule_tasks_are_registered_on_their_queues()

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.16
Nodes (8): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late()

### Community 8 - "test_gam_client.py"
Cohesion: 0.14
Nodes (13): Onde está o trabalho, client(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "tool_tasks.py"
Cohesion: 0.20
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
Cohesion: 0.16
Nodes (9): _count(), _login(), _queued_job(), test_metrics_enforce_the_monthly_limit_and_rules_skip_accounts_without_site(), test_run_job_creates_once_syncs_the_login_and_tells_the_screen(), test_run_job_of_another_company_does_not_call_google(), test_run_job_with_the_lock_taken_tries_again_later(), test_structure_metrics_and_changes_fill_the_company() (+1 more)

### Community 18 - "google_ads_tasks.py"
Cohesion: 0.11
Nodes (13): get_services(), run_job(), notify(), run_rules(), schedule_changes(), schedule_metrics(), schedule_rules(), schedule_structure() (+5 more)

### Community 22 - "test_mail_tasks.py"
Cohesion: 0.18
Nodes (7): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here(), test_the_real_resend_mailer_failing_makes_the_task_try_again()

### Community 23 - "install_check_tasks.py"
Cohesion: 0.11
Nodes (6): check_install(), check_site_installs(), daily_install_checks(), _dispatch(), dispatch_install_checks(), _run()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.10
Nodes (11): _clear_queued(), _fan_out(), _mark_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store() (+3 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.18
Nodes (4): _delegation(), _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "get_services"
Cohesion: 0.10
Nodes (12): check_tokens(), email_alerts(), run_job(), notify(), run_rules(), schedule_insights(), schedule_rules(), schedule_structure() (+4 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "test_metrics_tasks.py"
Cohesion: 0.11
Nodes (21): FakeReports, network(), reports(), row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue() (+13 more)

### Community 32 - "exchange_rates.py"
Cohesion: 0.12
Nodes (3): ExchangeRatesUnavailable, OpenExchangeRates, test_sync_stores_closed_days_and_today()

### Community 35 - "test_hubspot_tasks.py"
Cohesion: 0.12
Nodes (8): _client(), test_followups_do_nothing_without_the_token(), test_monthly_sync_is_scheduled_daily(), test_monthly_sync_runs_right_after_the_routine(), test_network_error_becomes_one_task_on_the_client_contact(), test_requested_sync_runs_and_a_refused_token_fails_the_run(), test_sync_does_nothing_without_the_token(), test_sync_runs_the_routine_and_saves_links()

### Community 36 - "ReportKind"
Cohesion: 0.15
Nodes (4): _ad_unit_path(), _hour(), _integer(), parse_report()

### Community 37 - "test_price_rule_tasks.py"
Cohesion: 0.07
Nodes (22): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too() (+14 more)

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "page_fetcher.py"
Cohesion: 0.10
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), _resolve(), test_checklist_tasks_are_registered(), test_public_addresses_are_allowed()

### Community 41 - "network_tasks.py"
Cohesion: 0.11
Nodes (10): discover_mcm(), sync_contracts(), check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests() (+2 more)

### Community 42 - "test_install_check_tasks.py"
Cohesion: 0.11
Nodes (5): CountingFetcher, _seed(), test_check_install_saves_and_tells_the_screen(), test_daily_checks_fetch_each_page_once(), test_install_tasks_are_registered()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.21
Nodes (5): _forget_cascades(), _forget_floors(), run_price_rules(), _run_site_automatic(), _run_site_cascade()

### Community 44 - "test_facebook_tasks.py"
Cohesion: 0.13
Nodes (10): _count(), facebook(), _profile(), test_check_tokens_runs_without_profiles(), test_insights_enforce_the_monthly_limit_and_alerts_go_by_email(), test_rules_run_without_rules(), test_run_job_duplicates_once_and_tells_the_screen(), test_structure_then_insights_fill_the_company() (+2 more)

### Community 45 - "test_page_fetcher.py"
Cohesion: 0.22
Nodes (7): HttpPageFetcher, test_images_still_come_back_empty(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused(), test_scripts_are_read_for_the_security_check(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 47 - "test_exchange_rates_tasks.py"
Cohesion: 0.14
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.22
Nodes (8): Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11), Resumo, Serviços e ferramentas

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.14
Nodes (13): Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões (+5 more)

### Community 51 - "fake_gam.py"
Cohesion: 0.13
Nodes (4): engine(), services(), FakeEarnings, FakeExchangeRates

### Community 52 - "test_key_value_tasks.py"
Cohesion: 0.14
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 53 - "ad_tag_tasks.py"
Cohesion: 0.18
Nodes (3): forget_network_ad_tags(), _optional_text(), _received_at()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.15
Nodes (10): PublicOnlyBackend, test_fetcher_never_connects_to_internal_addresses_or_other_ports(), FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order() (+2 more)

### Community 57 - "gam_client.py"
Cohesion: 0.15
Nodes (3): _error(), _message(), _revshare()

### Community 59 - "metrics/__init__.py"
Cohesion: 0.15
Nodes (6): backfill_metrics(), schedule_metrics(), schedule_reprocess(), months_to_fetch(), _shift(), sync_mcm_earnings()

### Community 60 - "reward_tasks.py"
Cohesion: 0.11
Nodes (7): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task()

### Community 62 - "test_reward_tasks.py"
Cohesion: 0.20
Nodes (4): redis_services(), _reward(), test_buffer_becomes_metrics_and_leads(), test_import_forgets_the_latest_reward_pages()

### Community 63 - "test_database_pool.py"
Cohesion: 0.12
Nodes (11): check_database_role(), use_services(), FakeEngine, _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_each_forked_child_gets_a_new_pool_without_closing_the_parent() (+3 more)

### Community 64 - "Services"
Cohesion: 0.08
Nodes (8): GamNotConfigured, Services, _key_ids(), _process_network(), _currency_and_time_zone(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so(), test_connected_networks_reach_the_route()

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 73 - "test_notification_tasks.py"
Cohesion: 0.17
Nodes (3): test_purge_removes_only_notifications_older_than_30_days(), test_detractor_reaches_the_manager_once(), test_warn_task_is_scheduled_on_the_default_queue()

### Community 77 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Como trabalhar nos repositórios, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação (+6 more)

### Community 78 - "Settings"
Cohesion: 0.12
Nodes (8): check_settings(), _variable_names(), _mailer(), _redis_client(), Settings, test_the_redis_client_has_short_socket_timeouts(), test_the_worker_starts_with_resend(), test_the_worker_starts_with_smtp()

### Community 81 - "pytest"
Cohesion: 0.18
Nodes (14): clean_env(), _stopped_names(), test_a_broken_smtp_url_does_not_start_and_hides_the_password(), test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_integration_variable_turns_the_integration_off(), test_an_empty_resend_key_is_named_in_the_error(), test_an_empty_variable_does_not_start(), test_an_invalid_smtp_url_fails_in_the_settings_showing_only_the_name() (+6 more)

### Community 83 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 87 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 88 - "logging"
Cohesion: 0.17
Nodes (6): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls(), _record(), test_log_keeps_ordinary_messages(), test_log_masks_database_values_in_message_and_stack()

### Community 96 - "test_ad_tag_tasks.py"
Cohesion: 0.14
Nodes (9): _page(), redis_services(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags(), test_partitions_are_created_once(), test_opportunities_open_ads_txt_once(), test_integrity_signals_become_a_cloaker_alert() (+1 more)

### Community 97 - "UUID"
Cohesion: 0.22
Nodes (5): _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 98 - "ReportKind"
Cohesion: 0.22
Nodes (4): _read_rows(), report_query(), ReportKind, _soap_date()

### Community 100 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 102 - "test_gam_tool_tasks.py"
Cohesion: 0.24
Nodes (4): soap_writer(), test_tool_task_is_registered(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 103 - "alert_tasks.py"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 105 - "_hit"
Cohesion: 0.27
Nodes (3): CountryLookup, _hit(), _hits()

### Community 109 - "20. CDN dos scripts do site (cdn.groone.com)"
Cohesion: 0.40
Nodes (4): 20. CDN dos scripts do site (cdn.groone.com), Chamadas da API e nome dos scripts (Pedro, 23/11, 23h52), Como fica no ar (proposta para o avant-infra), O que ficou decidido

### Community 111 - "19. Cliente e Empresa em dois cadastros"
Cohesion: 0.40
Nodes (4): 19. Cliente e Empresa em dois cadastros, Migrations, O que ficou decidido, Painel

### Community 112 - ".trusted_uow"
Cohesion: 0.07
Nodes (19): avant-worker, Contexto, issues e skills, refresh_levels(), test_open_checklists_checks_sites_that_earned_last_month(), earnings(), FixedClock, seller_scenario(), test_a_busy_lock_skips_the_run() (+11 more)

### Community 115 - "_route"
Cohesion: 0.17
Nodes (9): _route(), test_gam_tasks_are_registered_on_the_gam_queue(), test_followups_go_to_the_hubspot_queue_every_15_minutes(), test_hubspot_tasks_go_to_their_queue(), test_password_reset_task_is_registered_on_the_mail_queue(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_price_rule_tasks_are_registered() (+1 more)

### Community 116 - "usage_counter.py"
Cohesion: 0.07
Nodes (9): day_key(), days_key(), RedisUsageCounter, text(), usage_day_of(), flush_usage(), purge_usage(), test_flush_writes_the_day_totals_once() (+1 more)

### Community 118 - ".uow"
Cohesion: 0.28
Nodes (3): test_alerts_fire_once_and_mail_the_list_once(), test_previews_are_refreshed_once_and_again_when_old(), test_due_reports_go_out_once()

### Community 119 - "adapters/__init__.py"
Cohesion: 0.16
Nodes (4): channel(), publish(), schedule_page_views(), sync_page_views()

### Community 120 - "price_rules/__init__.py"
Cohesion: 0.28
Nodes (3): create_price_rules(), maintain_price_rule_partitions(), schedule_price_rule_hours()

### Community 127 - "app.py"
Cohesion: 0.10
Nodes (9): _check_on_start(), create_app(), _failure(), _logging(), _refuse_start(), _refuse_start_for(), _reset_after_fork(), reset_after_fork() (+1 more)

### Community 131 - "sync_price_rule_hours"
Cohesion: 0.33
Nodes (3): _reads_groone_network(), _record_time_zone(), sync_price_rule_hours()

### Community 132 - "_fault"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1041 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **74 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `.page_fetcher`, `company`, `sync_price_rule_hours`, `key_value_tasks.py`, `_flush`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`, `tool_tasks.py`, `test_google_ads_tasks.py`, `google_ads`, `redis_services`, `google_ads_tasks.py`, `test_mail_tasks.py`, `install_check_tasks.py`, `gam_metrics_tasks.py`, `services.py`, `test_metrics_tasks.py`, `exchange_rates.py`, `test_hubspot_tasks.py`, `test_price_rule_tasks.py`, `network_tasks.py`, `test_install_check_tasks.py`, `price_rule_tasks.py`, `test_facebook_tasks.py`, `test_page_fetcher.py`, `test_exchange_rates_tasks.py`, `nurture_tasks.py`, `fake_gam.py`, `test_key_value_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `test_reward_tasks.py`, `test_database_pool.py`, `avant_core_metrics_models`, `RestGamClient`, `test_notification_tasks.py`, `Settings`, `FakeNurtureMailer`, `FacebookNotConfigured`, `datetime`, `SoapReportClient`, `test_ad_tag_tasks.py`, `UUID`, `.trusted_uow`, `usage_counter.py`, `GoogleAdsNotConfigured`, `.uow`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Are the 147 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 147 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.054878048780487805 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `google_ads_tasks.py` to `flush_page_views`, `sync_price_rule_hours`, `key_value_tasks.py`, `commission_tasks.py`, `tool_tasks.py`, `password_reset_tasks.py`, `install_check_tasks.py`, `gam_metrics_tasks.py`, `portfolio_health_tasks.py`, `get_services`, `services.py`, `network_tasks.py`, `price_rule_tasks.py`, `test_exchange_rates_tasks.py`, `nurture_tasks.py`, `ad_tag_tasks.py`, `metrics/__init__.py`, `reward_tasks.py`, `Services`, `datetime`, `Settings`, `notification_tasks.py`, `purge_tasks.py`, `checklist_tasks.py`, `report_preview_tasks.py`, `alert_tasks.py`, `activation_tasks.py`, `usage_counter.py`, `adapters/__init__.py`, `price_rules/__init__.py`, `schedule_tasks.py`, `nps_tasks.py`, `opportunity_tasks.py`, `site_integrity_tasks.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Avant: models do MVP` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._