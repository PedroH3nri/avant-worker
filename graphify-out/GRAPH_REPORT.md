# Graph Report - avant-worker  (2026-11-11)

## Corpus Check
- 87 files · ~50,735 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1414 nodes · 2908 edges · 97 communities (59 shown, 38 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 269 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b926b748`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- Services
- enabled_site
- steps
- Avant: conexão com o GAM
- _soap_source
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- OpenExchangeRates
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- test_gam_tool_tasks.py
- clean_code.py
- test_commission_tasks.py
- Settings
- session-start.sh
- avant-worker
- .report
- metrics/__init__.py
- gam_metrics_tasks.py
- test_checklist_tasks.py
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- conftest.py
- test_gam_client.py
- test_mail_tasks.py
- _hit
- _HttpxResponse
- conftest.py
- key_value_tasks.py
- tool_tasks.py
- RestGamClient
- updates
- public_address
- MemoryWriter
- network_tasks.py
- _FixedClock
- price_rule_tasks.py
- test_key_value_tasks.py
- services.py
- page_view_tasks.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- avant-worker
- HttpPageFetcher
- uuid
- test_exchange_rates_tasks.py
- test_price_rule_tasks.py
- test_page_fetcher.py
- DeadlineStream
- ReportKind
- _route
- GeoLiteCountries
- reward_tasks.py
- test_ad_tag_tasks.py
- password_reset_tasks.py
- network
- network
- test_gam_tool_tasks.py
- gam_client.py
- SoapReportClient
- ._first
- _ad_unit
- StuckLookup
- GamTargetNetworkWithTimeZone
- gam_writer.py
- get_services
- FixedClock
- FakeLock
- .trusted_uow
- test_page_views_tasks.py
- avant-worker
- RecordingMailer
- app.py
- FakeSoapClient
- dripping_server
- PublicOnlyBackend
- test_tasks.py
- test_sync_stores_the_month_for_networks_in_avant
- ensure_page_view_partitions_task
- redis_services
- _HttpxAuthRequest
- source_files
- _error
- _fault
- FakeCredentials
- refresh_levels
- redis_services

## God Nodes (most connected - your core abstractions)
1. `Services` - 133 edges
2. `get_services()` - 64 edges
3. `company()` - 59 edges
4. `network()` - 52 edges
5. `SoapGamWriter` - 36 edges
6. `MemoryWriter` - 23 edges
7. `enabled_site()` - 20 edges
8. `fake()` - 19 edges
9. `_route()` - 18 edges
10. `count()` - 18 edges

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

## Communities (97 total, 38 thin omitted)

### Community 1 - "Services"
Cohesion: 0.16
Nodes (13): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), company(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network() (+5 more)

### Community 2 - "enabled_site"
Cohesion: 0.10
Nodes (9): enabled_site(), FakeRedis, test_create_price_rules_creates_cascades_too(), test_create_price_rules_keeps_the_count_when_a_cascade_fails(), test_run_price_rules_forgets_and_counts_hashes_when_a_cascade_fails(), explode(), test_run_price_rules_forgets_cascade_cache_when_start_changed(), test_run_price_rules_keeps_cascade_cache_when_start_did_not_change() (+1 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.11
Nodes (11): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+3 more)

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
Cohesion: 0.13
Nodes (13): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+5 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "OpenExchangeRates"
Cohesion: 0.13
Nodes (3): ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_gam_tool_tasks.py"
Cohesion: 0.14
Nodes (8): _route(), test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_price_rule_tasks_are_registered(), test_report_preview_tasks_are_registered_on_the_default_queue(), test_schedule_tasks_are_registered_on_their_queues()

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.24
Nodes (3): test_a_busy_lock_skips_the_run(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so()

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "metrics/__init__.py"
Cohesion: 0.22
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.18
Nodes (6): _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later()

### Community 25 - "test_checklist_tasks.py"
Cohesion: 0.15
Nodes (4): FakePageFetcher, test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_public_addresses_are_allowed()

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "conftest.py"
Cohesion: 0.12
Nodes (7): use_services(), engine(), services(), FakeEarnings, FakePageViews, FakeReports, test_earnings_task_is_on_the_gam_queue()

### Community 30 - "test_gam_client.py"
Cohesion: 0.14
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.14
Nodes (7): add_user(), count_resets(), RecordingMailer, test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_retries_a_failed_sending_and_sends_only_one_email(), test_task_sends_the_reset_email_with_a_token_generated_here()

### Community 32 - "_hit"
Cohesion: 0.21
Nodes (4): CountryLookup, _hit(), _hits(), _optional_text()

### Community 35 - "key_value_tasks.py"
Cohesion: 0.15
Nodes (5): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks(), _currency_and_time_zone()

### Community 36 - "tool_tasks.py"
Cohesion: 0.16
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 39 - "public_address"
Cohesion: 0.15
Nodes (5): _embedded_ipv4(), public_address(), _public_ipv4(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.11
Nodes (9): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network(), _record_time_zone(), run_price_rules(), schedule_price_rule_hours() (+1 more)

### Community 44 - "test_key_value_tasks.py"
Cohesion: 0.14
Nodes (5): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_a_network_without_gam_access_backs_off_and_keeps_its_pairs(), test_buffered_values_become_gam_values_once(), test_the_lock_is_renewed_for_each_network_and_a_lost_lock_stops_the_run()

### Community 46 - "page_view_tasks.py"
Cohesion: 0.18
Nodes (5): channel(), publish(), schedule_page_views(), sync_page_views(), test_publish_without_redis_is_a_no_op()

### Community 47 - "GamNotConfigured"
Cohesion: 0.18
Nodes (7): _ad_unit_path(), _hour(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_parse_report_keeps_groone_try_rows()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "uuid"
Cohesion: 0.05
Nodes (16): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+8 more)

### Community 53 - "test_exchange_rates_tasks.py"
Cohesion: 0.13
Nodes (7): closed_days_to_fetch(), sync_exchange_rates(), FakeExchangeRates, test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 54 - "test_price_rule_tasks.py"
Cohesion: 0.13
Nodes (12): CurrencyWriter, days_ago(), hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_hourly_query_and_parse_keep_only_content_hash(), test_hours_rules_and_engine_run_in_the_network_currency(), test_sync_asks_gam_once_for_currency_and_time_zone() (+4 more)

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.17
Nodes (8): FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect(), test_slow_dns_counts_against_the_total_deadline()

### Community 56 - "DeadlineStream"
Cohesion: 0.11
Nodes (3): DeadlineStream, _resolve(), _time_left()

### Community 57 - "ReportKind"
Cohesion: 0.20
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

### Community 60 - "reward_tasks.py"
Cohesion: 0.08
Nodes (9): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task(), redis_services() (+1 more)

### Community 61 - "test_ad_tag_tasks.py"
Cohesion: 0.26
Nodes (4): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags()

### Community 63 - "network"
Cohesion: 0.22
Nodes (16): backfills(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network(), test_failed_check_stops_before_importing() (+8 more)

### Community 64 - "network"
Cohesion: 0.29
Nodes (9): network(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_backfill_splits_the_period_in_weekly_chunks(), test_locked_chunk_goes_back_to_the_queue(), test_schedules_cover_today_and_the_reprocess_window(), test_sync_metrics_skips_manage_inventory_and_records_permanent_errors() (+1 more)

### Community 66 - "test_gam_tool_tasks.py"
Cohesion: 0.22
Nodes (4): soap_writer(), test_tool_task_is_registered(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 74 - "get_services"
Cohesion: 0.23
Nodes (5): get_services(), backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 77 - ".trusted_uow"
Cohesion: 0.27
Nodes (6): earnings(), seller_scenario(), test_closing_the_current_month_is_refused(), test_last_month_closes_after_its_earnings_arrive(), test_the_daily_run_fills_every_open_day(), test_today_is_calculated_and_the_month_closes()

### Community 78 - "test_page_views_tasks.py"
Cohesion: 0.20
Nodes (3): parse_documents(), test_page_view_tasks_are_registered_on_the_default_queue(), test_parse_documents_reads_the_data_counter()

### Community 81 - "app.py"
Cohesion: 0.08
Nodes (7): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter, BrokerSettings, test_http_client_logs_do_not_carry_request_urls()

### Community 83 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 85 - "test_tasks.py"
Cohesion: 0.15
Nodes (4): purge_expired(), test_deployed_envs_need_redis_and_resend(), test_purge_expired(), test_queue_comes_from_the_task_name()

### Community 87 - "ensure_page_view_partitions_task"
Cohesion: 0.25
Nodes (4): ensure_page_view_partitions_task(), _flush(), flush_page_views(), test_partitions_are_created_once()

### Community 92 - "_fault"
Cohesion: 0.29
Nodes (4): _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 685 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `enabled_site`, `OpenExchangeRates`, `test_commission_tasks.py`, `Settings`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `conftest.py`, `test_mail_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `price_rule_tasks.py`, `test_key_value_tasks.py`, `services.py`, `HttpPageFetcher`, `uuid`, `test_exchange_rates_tasks.py`, `test_price_rule_tasks.py`, `GeoLiteCountries`, `reward_tasks.py`, `test_ad_tag_tasks.py`, `network`, `network`, `get_services`, `FixedClock`, `.trusted_uow`, `dripping_server`, `test_tasks.py`, `test_sync_stores_the_month_for_networks_in_avant`, `ensure_page_view_partitions_task`, `redis_services`, `redis_services`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 108 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `Services`, `Avant: conexão com o GAM`, `commission_tasks.py`, `Settings`, `metrics/__init__.py`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `services.py`, `page_view_tasks.py`, `uuid`, `test_exchange_rates_tasks.py`, `reward_tasks.py`, `password_reset_tasks.py`, `app.py`, `test_tasks.py`, `ensure_page_view_partitions_task`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `enabled_site` be split into smaller, more focused modules?**
  _Cohesion score 0.10153846153846154 - nodes in this community are weakly interconnected._