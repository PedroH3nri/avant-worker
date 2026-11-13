# Graph Report - avant-worker  (2026-11-13)

## Corpus Check
- 89 files · ~53,652 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 1559 nodes · 3231 edges · 91 communities (53 shown, 38 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 309 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3be316a8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- InvalidVariable
- test_price_rule_tasks.py
- steps
- gam_reports.py
- page_fetcher.py
- Avant: models do MVP
- close_commissions
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- tool_tasks.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- password_reset_tasks.py
- clean_code.py
- checklist_tasks.py
- session-start.sh
- test_database_pool.py
- avant-worker
- .report
- metrics/__init__.py
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- fake_gam.py
- test_commission_tasks.py
- test_mail_tasks.py
- logging
- _HttpxResponse
- FakeGamClient
- exchange_rate_tasks.py
- backfill_metrics
- _check_on_start
- updates
- public_address
- MemoryWriter
- network_tasks.py
- parse_report
- price_rule_tasks.py
- network
- test_ad_tag_tasks.py
- .list_child_publishers
- Settings
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- test_gam_client.py
- HttpPageFetcher
- uuid
- _hit
- services.py
- test_page_fetcher.py
- DeadlineStream
- gam_client.py
- _last
- schedule_tasks.py
- reward_tasks.py
- GeoLiteCountries
- services
- company
- parse_documents
- test_schedule_tasks.py
- RestGamClient
- ._first
- _ad_unit
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- GamTargetNetworkWithTimeZone
- _error
- dripping_server
- _page
- FakeLock
- purge_expired
- clean_env
- StuckLookup
- pytest
- test_gam_tool_tasks.py
- Services
- get_services
- FakeCountries
- _HttpxAuthRequest
- source_files
- _public_transport
- MaskedRequest
- RecordingMailer
- test_a_database_error_retries_without_the_email

## God Nodes (most connected - your core abstractions)
1. `Services` - 146 edges
2. `get_services()` - 65 edges
3. `company()` - 64 edges
4. `network()` - 57 edges
5. `SoapGamWriter` - 36 edges
6. `Settings` - 25 edges
7. `MemoryWriter` - 23 edges
8. `enabled_site()` - 21 edges
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

## Communities (91 total, 38 thin omitted)

### Community 2 - "test_price_rule_tasks.py"
Cohesion: 0.07
Nodes (22): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too() (+14 more)

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 5 - "page_fetcher.py"
Cohesion: 0.15
Nodes (3): _resolve(), test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports()

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "close_commissions"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.14
Nodes (12): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Modelo de contas, O produto (+4 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "tool_tasks.py"
Cohesion: 0.11
Nodes (7): channel(), publish(), GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

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

### Community 16 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 18 - "test_database_pool.py"
Cohesion: 0.19
Nodes (8): check_database_role(), _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_the_app_role_passes_the_start_check(), test_the_connection_carries_the_worker_name_and_timeouts(), test_the_default_pool_fits_the_connection_budget()

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "metrics/__init__.py"
Cohesion: 0.14
Nodes (6): months_to_fetch(), _shift(), sync_mcm_earnings(), schedule_page_views(), sync_page_views(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.11
Nodes (11): ReportKind, _clear_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store(), sync_metrics() (+3 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "fake_gam.py"
Cohesion: 0.11
Nodes (6): FakeEarnings, FakeExchangeRates, FakePageViews, FakeReports, test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.06
Nodes (21): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+13 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.15
Nodes (10): Infraestrutura e operação, Variáveis, add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here() (+2 more)

### Community 32 - "logging"
Cohesion: 0.13
Nodes (8): _refuse_start(), _refuse_start_for(), configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls(), _record(), test_log_keeps_ordinary_messages(), test_log_masks_database_values_in_message_and_stack()

### Community 35 - "exchange_rate_tasks.py"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 36 - "backfill_metrics"
Cohesion: 0.18
Nodes (5): backfill_metrics(), _fan_out(), _mark_queued(), schedule_metrics(), schedule_reprocess()

### Community 37 - "_check_on_start"
Cohesion: 0.24
Nodes (4): _check_on_start(), _failure(), _logging(), _reset_after_fork()

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "public_address"
Cohesion: 0.19
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.07
Nodes (21): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+13 more)

### Community 42 - "parse_report"
Cohesion: 0.06
Nodes (14): _ad_unit_path(), _classify(), _hour(), _integer(), parse_report(), _read_rows(), report_query(), _soap_date() (+6 more)

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.08
Nodes (14): _key_ids(), _process_network(), create_price_rules(), _currency_and_time_zone(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network() (+6 more)

### Community 44 - "network"
Cohesion: 0.12
Nodes (20): network(), reports(), row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue(), test_a_period_already_waiting_in_the_queue_is_not_queued_again() (+12 more)

### Community 45 - "test_ad_tag_tasks.py"
Cohesion: 0.23
Nodes (4): ensure_page_view_partitions_task(), flush_page_views(), test_buffer_becomes_page_views_and_health(), test_partitions_are_created_once()

### Community 47 - "Settings"
Cohesion: 0.18
Nodes (7): check_settings(), _mailer(), _redis_client(), Settings, test_the_redis_client_has_short_socket_timeouts(), test_the_worker_starts_with_resend(), test_the_worker_starts_with_smtp()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "test_gam_client.py"
Cohesion: 0.06
Nodes (17): Onde está o trabalho, ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), client(), record(), FakeCredentials, ok() (+9 more)

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "uuid"
Cohesion: 0.12
Nodes (8): refresh_report_preview(), refresh_report_previews(), test_purge_expired(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 53 - "_hit"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 54 - "services.py"
Cohesion: 0.08
Nodes (3): create_app(), reset_after_fork(), BrokerSettings

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.15
Nodes (10): PublicOnlyBackend, FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect() (+2 more)

### Community 60 - "reward_tasks.py"
Cohesion: 0.08
Nodes (11): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task(), redis_services() (+3 more)

### Community 62 - "services"
Cohesion: 0.22
Nodes (5): use_services(), engine(), services(), FakeEngine, test_each_forked_child_gets_a_new_pool_without_closing_the_parent()

### Community 63 - "company"
Cohesion: 0.26
Nodes (18): backfills(), company(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network() (+10 more)

### Community 66 - "test_schedule_tasks.py"
Cohesion: 0.07
Nodes (13): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_password_reset_task_is_registered_on_the_mail_queue() (+5 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 81 - "pytest"
Cohesion: 0.25
Nodes (10): _stopped_names(), test_a_broken_smtp_url_does_not_start_and_hides_the_password(), test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_variable_does_not_start(), test_an_invalid_smtp_url_fails_in_the_settings_showing_only_the_name(), test_an_unknown_transport_does_not_start(), test_each_transport_needs_its_own_configuration(), test_the_redis_url_needs_a_redis_scheme() (+2 more)

### Community 82 - "test_gam_tool_tasks.py"
Cohesion: 0.05
Nodes (16): FakeSoapClient, FakeSoapService, soap_writer(), test_tool_task_is_registered(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), FakeTrafficWriter, _fault() (+8 more)

### Community 83 - "Services"
Cohesion: 0.11
Nodes (12): Services, _tag(), test_import_forgets_the_network_tags(), test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_stores_the_month_for_networks_in_avant(), staff(), test_a_busy_network_waits_and_tries_again() (+4 more)

### Community 84 - "get_services"
Cohesion: 0.25
Nodes (4): get_services(), check_alerts(), notify_alerts(), schedule_alerts()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 745 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `test_price_rule_tasks.py`, `gam_reports.py`, `tool_tasks.py`, `test_database_pool.py`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `fake_gam.py`, `test_commission_tasks.py`, `test_mail_tasks.py`, `backfill_metrics`, `network_tasks.py`, `parse_report`, `price_rule_tasks.py`, `network`, `test_ad_tag_tasks.py`, `Settings`, `test_gam_client.py`, `HttpPageFetcher`, `uuid`, `services.py`, `gam_client.py`, `reward_tasks.py`, `GeoLiteCountries`, `services`, `company`, `.gam`, `RestGamClient`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`, `dripping_server`, `_page`, `test_gam_tool_tasks.py`, `get_services`, `FakeCountries`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Are the 121 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 121 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `gam_reports.py`, `close_commissions`, `tool_tasks.py`, `password_reset_tasks.py`, `checklist_tasks.py`, `metrics/__init__.py`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `exchange_rate_tasks.py`, `backfill_metrics`, `network_tasks.py`, `price_rule_tasks.py`, `test_ad_tag_tasks.py`, `Settings`, `uuid`, `services.py`, `schedule_tasks.py`, `reward_tasks.py`, `purge_expired`, `Services`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_price_rule_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07197763801537387 - nodes in this community are weakly interconnected._