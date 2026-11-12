# Graph Report - wt132-avant-worker  (2026-11-12)

## Corpus Check
- 88 files · ~53,311 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .toml 1, .lock 1)

## Summary
- 1543 nodes · 3184 edges · 94 communities (58 shown, 36 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 300 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e61baa45`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- app.py
- test_price_rule_tasks.py
- steps
- gam_reports.py
- page_fetcher.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- adapters/__init__.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- password_reset_tasks.py
- clean_code.py
- gam_writer.py
- metrics/__init__.py
- session-start.sh
- test_database_pool.py
- avant-worker
- .report
- months_to_fetch
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- services.py
- Services
- test_mail_tasks.py
- avant-worker
- _HttpxResponse
- FakeGamClient
- _FixedClock
- run_tool
- test_gam_tool_tasks.py
- updates
- public_address
- MemoryWriter
- network_tasks.py
- price_rule_tasks.py
- test_metrics_tasks.py
- test_checklist_tasks.py
- _fault
- Settings
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- logging
- HttpPageFetcher
- uuid
- _updated
- _check_on_start
- test_page_fetcher.py
- DeadlineStream
- MongoPageViews
- FakeSoapClient
- avant-worker
- reward_tasks.py
- redis_services
- company
- get_services
- test_schedule_tasks.py
- test_gam_client.py
- RestGamClient
- ._statement
- _ad_unit
- GamTargetNetworkWithTimeZone
- gam_client.py
- dripping_server
- FakeLock
- Avant: conexão com o GAM
- OpenExchangeRates
- StuckLookup
- pytest
- test_key_value_tasks.py
- .uow
- purge_tasks.py
- key_value_tasks.py
- FakeCountries
- _HttpxAuthRequest
- source_files
- _error
- _batch
- PublicOnlyBackend
- MaskedRequest
- RecordingMailer
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- FakeCredentials

## God Nodes (most connected - your core abstractions)
1. `Services` - 143 edges
2. `get_services()` - 65 edges
3. `company()` - 63 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `Settings` - 23 edges
7. `MemoryWriter` - 23 edges
8. `enabled_site()` - 20 edges
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

## Communities (94 total, 36 thin omitted)

### Community 1 - "app.py"
Cohesion: 0.12
Nodes (4): create_app(), _variable_names(), BrokerSettings, MissingVariable

### Community 2 - "test_price_rule_tasks.py"
Cohesion: 0.07
Nodes (21): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too() (+13 more)

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 4 - "gam_reports.py"
Cohesion: 0.06
Nodes (14): _ad_unit_path(), _hour(), _integer(), parse_report(), _read_rows(), report_query(), ReportKind, _soap_date() (+6 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "commission_tasks.py"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.14
Nodes (12): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Modelo de contas, O produto (+4 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

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
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 16 - "metrics/__init__.py"
Cohesion: 0.13
Nodes (7): backfill_metrics(), _fan_out(), _mark_queued(), schedule_metrics(), schedule_reprocess(), schedule_page_views(), sync_page_views()

### Community 18 - "test_database_pool.py"
Cohesion: 0.12
Nodes (11): check_database_role(), use_services(), FakeEngine, _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_each_forked_child_gets_a_new_pool_without_closing_the_parent() (+3 more)

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "months_to_fetch"
Cohesion: 0.25
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.12
Nodes (10): _clear_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store(), sync_metrics(), _sync_metrics() (+2 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "ad_tag_tasks.py"
Cohesion: 0.05
Nodes (15): GeoLiteCountries, CountryLookup, ensure_page_view_partitions_task(), _flush(), flush_page_views(), forget_network_ad_tags(), _hit(), _hits() (+7 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "services.py"
Cohesion: 0.08
Nodes (6): engine(), services(), FakeEarnings, FakeExchangeRates, FakePageViews, FakeReports

### Community 30 - "Services"
Cohesion: 0.08
Nodes (18): Services, refresh_levels(), test_open_checklists_checks_sites_that_earned_last_month(), earnings(), FixedClock, seller_scenario(), test_a_busy_lock_skips_the_run(), test_a_long_run_renews_the_lock() (+10 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.18
Nodes (7): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_password_reset_task_is_registered_on_the_mail_queue(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here()

### Community 32 - "avant-worker"
Cohesion: 0.17
Nodes (11): Infraestrutura e operação, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos (+3 more)

### Community 36 - "run_tool"
Cohesion: 0.22
Nodes (3): GamNotConfigured, run_tool(), _try_later()

### Community 37 - "test_gam_tool_tasks.py"
Cohesion: 0.24
Nodes (3): soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

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

### Community 44 - "test_metrics_tasks.py"
Cohesion: 0.10
Nodes (18): reports(), row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue(), test_a_period_already_waiting_in_the_queue_is_not_queued_again(), test_a_report_with_only_the_header_is_an_empty_period() (+10 more)

### Community 46 - "_fault"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

### Community 47 - "Settings"
Cohesion: 0.11
Nodes (8): check_settings(), _refuse_start(), _refuse_start_for(), _mailer(), _redis_client(), Settings, test_the_worker_starts_with_resend(), test_the_worker_starts_with_smtp()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "logging"
Cohesion: 0.10
Nodes (7): configure_logging(), JsonFormatter, closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_http_client_logs_do_not_carry_request_urls(), test_sync_without_key_does_nothing()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "uuid"
Cohesion: 0.05
Nodes (16): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+8 more)

### Community 54 - "_check_on_start"
Cohesion: 0.19
Nodes (5): _check_on_start(), _failure(), _logging(), _reset_after_fork(), reset_after_fork()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.17
Nodes (8): FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect(), test_slow_dns_counts_against_the_total_deadline()

### Community 57 - "MongoPageViews"
Cohesion: 0.20
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 60 - "reward_tasks.py"
Cohesion: 0.15
Nodes (5): _flush(), flush_reward_events(), forget_latest_reward_pages(), purge_reward_batches_task(), test_buffer_becomes_metrics_and_leads()

### Community 63 - "company"
Cohesion: 0.27
Nodes (22): test_sync_stores_the_month_for_networks_in_avant(), backfills(), company(), count(), fake(), inventory(), network(), test_check_access_and_schedulers() (+14 more)

### Community 64 - "get_services"
Cohesion: 0.21
Nodes (4): Importação, get_services(), discover_mcm(), sync_contracts()

### Community 66 - "test_schedule_tasks.py"
Cohesion: 0.06
Nodes (14): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue() (+6 more)

### Community 67 - "test_gam_client.py"
Cohesion: 0.19
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 73 - "gam_client.py"
Cohesion: 0.14
Nodes (3): _delegation(), _last(), _revshare()

### Community 74 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 77 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 78 - "OpenExchangeRates"
Cohesion: 0.12
Nodes (3): ExchangeRatesUnavailable, OpenExchangeRates, test_sync_stores_closed_days_and_today()

### Community 81 - "pytest"
Cohesion: 0.17
Nodes (12): test_client_reads_rates_as_decimals_and_fails_clearly(), clean_env(), _stopped_names(), test_a_broken_smtp_url_does_not_start_and_hides_the_password(), test_a_resend_key_with_only_spaces_does_not_start(), test_an_empty_variable_does_not_start(), test_an_unknown_transport_does_not_start(), test_each_transport_needs_its_own_configuration() (+4 more)

### Community 82 - "test_key_value_tasks.py"
Cohesion: 0.11
Nodes (6): FakeTrafficWriter, redis_services(), test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 83 - ".uow"
Cohesion: 0.18
Nodes (5): test_alerts_fire_once_and_mail_the_list_once(), test_previews_are_refreshed_once_and_again_when_old(), _reward(), test_import_forgets_the_latest_reward_pages(), test_due_reports_go_out_once()

### Community 85 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 94 - "_batch"
Cohesion: 0.22
Nodes (3): _batch(), _event(), _lead()

### Community 99 - "test_the_smtp_mailer_failing_for_now_makes_the_task_try_again"
Cohesion: 0.17
Nodes (3): test_a_database_error_retries_without_the_email(), test_a_retry_publishes_the_email_masked(), test_the_smtp_mailer_failing_for_now_makes_the_task_try_again()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 738 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `test_price_rule_tasks.py`, `gam_reports.py`, `metrics/__init__.py`, `test_database_pool.py`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `services.py`, `test_mail_tasks.py`, `avant-worker`, `network_tasks.py`, `price_rule_tasks.py`, `test_metrics_tasks.py`, `Settings`, `logging`, `HttpPageFetcher`, `uuid`, `_updated`, `MongoPageViews`, `reward_tasks.py`, `redis_services`, `company`, `get_services`, `RestGamClient`, `dripping_server`, `OpenExchangeRates`, `test_key_value_tasks.py`, `.uow`, `key_value_tasks.py`, `.gam`, `FakeCountries`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **Are the 118 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 118 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11594202898550725 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `app.py`, `run_tool`, `commission_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `password_reset_tasks.py`, `Settings`, `metrics/__init__.py`, `logging`, `uuid`, `key_value_tasks.py`, `purge_tasks.py`, `months_to_fetch`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `services.py`, `Services`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_price_rule_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07315233785822021 - nodes in this community are weakly interconnected._