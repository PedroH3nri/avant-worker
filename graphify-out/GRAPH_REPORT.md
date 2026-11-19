# Graph Report - avant-worker  (2026-11-18)

## Corpus Check
- 92 files · ~55,212 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 6, .toml 1, .lock 1)

## Summary
- 1629 nodes · 3360 edges · 98 communities (55 shown, 43 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 312 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `50f54ada`
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
- adapters/__init__.py
- session-start.sh
- test_database_pool.py
- avant-worker
- .report
- gam_metrics_tasks.py
- _store
- FakePageFetcher
- .list_mcm_earnings
- facebook_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- FakeEarnings
- test_commission_tasks.py
- test_mail_tasks.py
- app.py
- _HttpxResponse
- FakeGamClient
- test_exchange_rates_tasks.py
- get_services
- test_facebook_tasks.py
- updates
- public_address
- MemoryWriter
- network_tasks.py
- ReportKind
- price_rule_tasks.py
- company
- ensure_page_view_partitions_task
- _route
- key_value_tasks.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- test_gam_client.py
- HttpPageFetcher
- uuid
- ad_tag_tasks.py
- services.py
- test_page_fetcher.py
- DeadlineStream
- gam_client.py
- MonkeyPatch
- schedule_tasks.py
- reward_tasks.py
- FakeFacebook
- FakeTrafficWriter
- test_gam_tasks.py
- MongoPageViews
- RecordingMailer
- GamNotConfigured
- RestGamClient
- ._first
- _ad_unit
- test_the_smtp_mailer_failing_for_now_makes_the_task_try_again
- GamTargetNetworkWithTimeZone
- Avant: conexão com o GAM
- dripping_server
- avant-worker
- FakeLock
- purge_tasks.py
- SoapReportClient
- StuckLookup
- sync_price_rule_hours
- pytest
- soap_writer
- Services
- json
- FacebookNotConfigured
- test_report_is_read_from_a_temporary_file_as_it_streams
- FakeCountries
- report_query
- _FixedClock
- facebook
- redis_services
- _public_transport
- MaskedRequest
- RecordingMailer
- test_a_database_error_retries_without_the_email

## God Nodes (most connected - your core abstractions)
1. `Services` - 156 edges
2. `get_services()` - 71 edges
3. `company()` - 66 edges
4. `network()` - 56 edges
5. `SoapGamWriter` - 36 edges
6. `Settings` - 25 edges
7. `MemoryWriter` - 23 edges
8. `enabled_site()` - 21 edges
9. `_route()` - 19 edges
10. `fake()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam/mcm_tasks.py
- `test_a_busy_lock_skips_the_run()` --uses--> `Services`  [INFERRED]
  tests/test_commission_tasks.py → src/avant_worker/services.py
- `test_the_connection_carries_the_worker_name_and_timeouts()` --uses--> `Services`  [INFERRED]
  tests/test_database_pool.py → src/avant_worker/services.py
- `test_sync_without_key_does_nothing()` --uses--> `Services`  [INFERRED]
  tests/test_exchange_rates_tasks.py → src/avant_worker/services.py
- `test_check_tokens_runs_without_profiles()` --uses--> `Services`  [INFERRED]
  tests/test_facebook_tasks.py → src/avant_worker/services.py

## Import Cycles
- None detected.

## Communities (98 total, 43 thin omitted)

### Community 2 - "test_price_rule_tasks.py"
Cohesion: 0.07
Nodes (23): count(), CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call() (+15 more)

### Community 3 - "steps"
Cohesion: 0.05
Nodes (40): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+32 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "close_commissions"
Cohesion: 0.15
Nodes (9): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late() (+1 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Como trabalhar nos repositórios, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "tool_tasks.py"
Cohesion: 0.18
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "password_reset_tasks.py"
Cohesion: 0.14
Nodes (4): MaskedTask, request_password_reset(), TemporaryDatabaseError, test_the_email_never_reaches_the_celery_log_or_events()

### Community 14 - "clean_code.py"
Cohesion: 0.11
Nodes (10): check_file(), docstring_problems(), inline_comments(), is_exempt(), main(), single_letter_names(), source_files(), _record() (+2 more)

### Community 18 - "test_database_pool.py"
Cohesion: 0.10
Nodes (11): check_database_role(), use_services(), FakeEngine, _settings(), test_an_owner_role_does_not_start_and_the_password_stays_out(), test_an_unreachable_database_does_not_start(), test_default_engine_settings_are_valid_and_named(), test_each_forked_child_gets_a_new_pool_without_closing_the_parent() (+3 more)

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "gam_metrics_tasks.py"
Cohesion: 0.10
Nodes (6): schedule_reprocess(), months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again(), test_report_preview_tasks_are_registered_on_the_default_queue()

### Community 24 - "_store"
Cohesion: 0.08
Nodes (12): _clear_queued(), _fan_out(), _mark_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store() (+4 more)

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.18
Nodes (4): _delegation(), _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "facebook_tasks.py"
Cohesion: 0.16
Nodes (6): check_tokens(), schedule_insights(), schedule_structure(), sync_insights(), sync_profile(), test_tasks_go_to_the_facebook_queue_and_retry_on_unavailable()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.07
Nodes (18): avant-worker, Contexto, issues e skills, _flush(), refresh_levels(), test_open_checklists_checks_sites_that_earned_last_month(), earnings(), FixedClock, seller_scenario() (+10 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.15
Nodes (8): add_user(), count_resets(), test_an_error_that_is_not_temporary_is_not_retried(), test_password_reset_task_is_registered_on_the_mail_queue(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_sends_the_reset_email_with_a_token_generated_here(), test_the_real_resend_mailer_failing_makes_the_task_try_again()

### Community 32 - "app.py"
Cohesion: 0.09
Nodes (10): _check_on_start(), _failure(), _logging(), _refuse_start(), _refuse_start_for(), _reset_after_fork(), configure_logging(), JsonFormatter (+2 more)

### Community 35 - "test_exchange_rates_tasks.py"
Cohesion: 0.12
Nodes (8): closed_days_to_fetch(), sync_exchange_rates(), FakeExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 36 - "get_services"
Cohesion: 0.11
Nodes (8): Importação, get_services(), discover_mcm(), sync_contracts(), backfill_metrics(), schedule_metrics(), schedule_page_views(), sync_page_views()

### Community 37 - "test_facebook_tasks.py"
Cohesion: 0.16
Nodes (6): _count(), _profile(), test_check_tokens_runs_without_profiles(), test_structure_then_insights_fill_the_company(), test_sync_profile_is_idempotent(), test_unavailable_is_retried()

### Community 38 - "updates"
Cohesion: 0.11
Nodes (17): patterns, patterns, update-types, actions, dependencias, imagens, dependency-name, patterns (+9 more)

### Community 39 - "public_address"
Cohesion: 0.11
Nodes (7): GeoLiteCountries, _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - "ReportKind"
Cohesion: 0.13
Nodes (9): _ad_unit_path(), _hour(), _integer(), parse_report(), _read_rows(), ReportKind, test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria() (+1 more)

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.13
Nodes (8): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), run_price_rules(), _run_site_automatic(), _run_site_cascade(), schedule_price_rule_hours()

### Community 44 - "company"
Cohesion: 0.17
Nodes (29): backfills(), company(), fake(), inventory(), network(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_failed_check_stops_before_importing() (+21 more)

### Community 45 - "ensure_page_view_partitions_task"
Cohesion: 0.28
Nodes (4): ensure_page_view_partitions_task(), flush_page_views(), test_buffer_becomes_page_views_and_health(), test_partitions_are_created_once()

### Community 46 - "_route"
Cohesion: 0.12
Nodes (12): create_app(), _route(), BrokerSettings, test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered() (+4 more)

### Community 47 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.22
Nodes (8): Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11), Resumo, Serviços e ferramentas

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.14
Nodes (13): Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões (+5 more)

### Community 50 - "test_gam_client.py"
Cohesion: 0.14
Nodes (14): Onde está o trabalho, client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified() (+6 more)

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "uuid"
Cohesion: 0.06
Nodes (15): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+7 more)

### Community 53 - "ad_tag_tasks.py"
Cohesion: 0.12
Nodes (6): CountryLookup, forget_network_ad_tags(), _hit(), _hits(), _optional_text(), _received_at()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.15
Nodes (10): PublicOnlyBackend, FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect() (+2 more)

### Community 57 - "gam_client.py"
Cohesion: 0.14
Nodes (3): _error(), _message(), _revshare()

### Community 58 - "MonkeyPatch"
Cohesion: 0.19
Nodes (7): _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_report_with_only_the_header_is_an_empty_period(), test_a_report_without_the_csv_header_is_a_temporary_failure(), test_a_temporary_failure_that_will_be_retried_keeps_the_queue_mark(), test_report_downloads_before_the_rows_are_read(), test_the_downloaded_file_closes_even_if_nobody_reads_it()

### Community 60 - "reward_tasks.py"
Cohesion: 0.09
Nodes (8): _batch(), _event(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task(), redis_services(), test_buffer_becomes_metrics_and_leads()

### Community 62 - "FakeTrafficWriter"
Cohesion: 0.13
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 64 - "MongoPageViews"
Cohesion: 0.20
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 73 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 74 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 75 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 80 - "sync_price_rule_hours"
Cohesion: 0.25
Nodes (4): _currency_and_time_zone(), _reads_groone_network(), _record_time_zone(), sync_price_rule_hours()

### Community 81 - "pytest"
Cohesion: 0.12
Nodes (20): check_settings(), _mailer(), _redis_client(), Settings, engine(), services(), clean_env(), _stopped_names() (+12 more)

### Community 82 - "soap_writer"
Cohesion: 0.10
Nodes (9): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+1 more)

### Community 83 - "Services"
Cohesion: 0.09
Nodes (13): Services, _flush(), _tag(), test_import_forgets_the_network_tags(), test_alerts_fire_once_and_mail_the_list_once(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so(), test_discover_mcm_activates_the_registered_network() (+5 more)

### Community 89 - "report_query"
Cohesion: 0.40
Nodes (3): report_query(), _soap_date(), test_report_query_matches_unified_sync()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 788 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `test_price_rule_tasks.py`, `tool_tasks.py`, `adapters/__init__.py`, `test_database_pool.py`, `gam_metrics_tasks.py`, `_store`, `test_commission_tasks.py`, `test_mail_tasks.py`, `test_exchange_rates_tasks.py`, `get_services`, `test_facebook_tasks.py`, `public_address`, `network_tasks.py`, `price_rule_tasks.py`, `company`, `ensure_page_view_partitions_task`, `key_value_tasks.py`, `HttpPageFetcher`, `uuid`, `ad_tag_tasks.py`, `services.py`, `MonkeyPatch`, `reward_tasks.py`, `FakeTrafficWriter`, `MongoPageViews`, `GamNotConfigured`, `RestGamClient`, `test_the_smtp_mailer_failing_for_now_makes_the_task_try_again`, `dripping_server`, `SoapReportClient`, `sync_price_rule_hours`, `pytest`, `FacebookNotConfigured`, `FakeCountries`, `facebook`, `redis_services`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Are the 129 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 129 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `close_commissions`, `tool_tasks.py`, `password_reset_tasks.py`, `gam_metrics_tasks.py`, `_store`, `facebook_tasks.py`, `app.py`, `test_exchange_rates_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `ensure_page_view_partitions_task`, `key_value_tasks.py`, `uuid`, `ad_tag_tasks.py`, `services.py`, `schedule_tasks.py`, `reward_tasks.py`, `purge_tasks.py`, `sync_price_rule_hours`, `pytest`, `Services`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_price_rule_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07077922077922078 - nodes in this community are weakly interconnected._