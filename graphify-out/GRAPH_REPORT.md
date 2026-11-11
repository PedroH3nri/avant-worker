# Graph Report - avant-worker  (2026-11-11)

## Corpus Check
- 84 files · ~49,629 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1369 nodes · 2825 edges · 91 communities (56 shown, 35 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 255 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2671e0e0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- company
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
- ExchangeRateSource
- metrics/__init__.py
- gam_metrics_tasks.py
- page_fetcher.py
- test_price_rule_tasks.py
- uuid
- Avant: grupos na Empresa e imagem da Empresa
- test_metrics_tasks.py
- pytest
- _error
- ad_tag_tasks.py
- _HttpxResponse
- conftest.py
- key_value_tasks.py
- tool_tasks.py
- updates
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- price_rule_tasks.py
- test_gam_tool_tasks.py
- collections_abc
- adapters/__init__.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- mcm_tasks.py
- HttpPageFetcher
- RecordingMailer
- datetime
- test_page_fetcher.py
- DeadlineStream
- ReportKind
- _route
- uuid
- reward_tasks.py
- test_ad_tag_tasks.py
- app.py
- network
- network
- _route
- gam_client.py
- SoapReportClient
- ._first
- _ad_unit
- gam_client.py
- GamTargetNetworkWithTimeZone
- _refused_values
- _last
- fake_gam.py
- FakeLock
- FakePageFetcher
- RestGamClient
- _FixedClock
- RecordingMailer
- logging
- gam/__init__.py
- dripping_server
- PublicOnlyBackend
- purge_tasks.py
- adapters/__init__.py
- _failure
- report_query
- services
- source_files

## God Nodes (most connected - your core abstractions)
1. `Services` - 125 edges
2. `get_services()` - 62 edges
3. `company()` - 59 edges
4. `network()` - 52 edges
5. `SoapGamWriter` - 36 edges
6. `MemoryWriter` - 23 edges
7. `enabled_site()` - 20 edges
8. `fake()` - 19 edges
9. `count()` - 18 edges
10. `RestGamClient` - 17 edges

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

## Communities (91 total, 35 thin omitted)

### Community 1 - "company"
Cohesion: 0.12
Nodes (11): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_stores_the_month_for_networks_in_avant(), staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network(), test_previews_are_refreshed_once_and_again_when_old() (+3 more)

### Community 2 - "enabled_site"
Cohesion: 0.10
Nodes (10): enabled_site(), FakeRedis, test_create_price_rules_creates_cascades_too(), test_create_price_rules_keeps_the_count_when_a_cascade_fails(), test_run_price_rules_forgets_and_counts_hashes_when_a_cascade_fails(), explode(), test_run_price_rules_forgets_cascade_cache_when_start_changed(), test_run_price_rules_keeps_cascade_cache_when_start_did_not_change() (+2 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

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

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_gam_tool_tasks.py"
Cohesion: 0.14
Nodes (4): test_alert_tasks_are_registered_on_their_queues(), test_tool_task_is_registered(), test_report_preview_tasks_are_registered_on_the_default_queue(), test_schedule_tasks_are_registered_on_their_queues()

### Community 14 - "clean_code.py"
Cohesion: 0.18
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.06
Nodes (22): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+14 more)

### Community 16 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "metrics/__init__.py"
Cohesion: 0.15
Nodes (5): months_to_fetch(), _shift(), sync_mcm_earnings(), schedule_page_views(), sync_page_views()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.11
Nodes (10): backfill_metrics(), _fan_out(), _network(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store() (+2 more)

### Community 25 - "page_fetcher.py"
Cohesion: 0.11
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), _resolve(), test_checklist_tasks_are_registered(), test_public_addresses_are_allowed()

### Community 26 - "test_price_rule_tasks.py"
Cohesion: 0.14
Nodes (10): CurrencyWriter, days_ago(), hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_hours_rules_and_engine_run_in_the_network_currency(), test_sync_does_not_ask_gam_again_when_the_time_zone_is_empty(), test_sync_records_the_network_time_zone() (+2 more)

### Community 27 - "uuid"
Cohesion: 0.12
Nodes (7): refresh_report_preview(), refresh_report_previews(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "pytest"
Cohesion: 0.06
Nodes (21): Onde está o trabalho, flush_reward_events(), purge_reward_batches_task(), FakeCountries, redis_services(), test_client_reads_rates_as_decimals_and_fails_clearly(), client(), record() (+13 more)

### Community 32 - "ad_tag_tasks.py"
Cohesion: 0.07
Nodes (10): GeoLiteCountries, CountryLookup, ensure_page_view_partitions_task(), _flush(), flush_page_views(), forget_network_ad_tags(), _hit(), _hits() (+2 more)

### Community 35 - "key_value_tasks.py"
Cohesion: 0.15
Nodes (5): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks(), _currency_and_time_zone()

### Community 36 - "tool_tasks.py"
Cohesion: 0.14
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.19
Nodes (5): _flat(), _last_import(), sync_network(), _updated(), forget_latest_reward_pages()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.11
Nodes (9): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network(), _record_time_zone(), run_price_rules(), schedule_price_rule_hours() (+1 more)

### Community 44 - "test_gam_tool_tasks.py"
Cohesion: 0.06
Nodes (13): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), FakeTrafficWriter, _fault(), redis_services() (+5 more)

### Community 45 - "collections_abc"
Cohesion: 0.15
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 46 - "adapters/__init__.py"
Cohesion: 0.31
Nodes (3): channel(), publish(), test_publish_without_redis_is_a_no_op()

### Community 47 - "GamNotConfigured"
Cohesion: 0.14
Nodes (7): _ad_unit_path(), _hour(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_parse_report_keeps_groone_try_rows()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "mcm_tasks.py"
Cohesion: 0.22
Nodes (3): Importação, discover_mcm(), sync_contracts()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.21
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "RecordingMailer"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "datetime"
Cohesion: 0.16
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.14
Nodes (10): FakeStream, _resolves_to(), test_backend_never_connects_when_any_address_is_internal(), fake_connect(), test_backend_raises_the_last_error_when_no_address_answers(), test_backend_tries_each_checked_address_in_order(), fake_connect(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed() (+2 more)

### Community 59 - "uuid"
Cohesion: 0.23
Nodes (4): get_services(), check_alerts(), notify_alerts(), schedule_alerts()

### Community 60 - "reward_tasks.py"
Cohesion: 0.17
Nodes (4): _batch(), _event(), _flush(), _lead()

### Community 61 - "test_ad_tag_tasks.py"
Cohesion: 0.22
Nodes (5): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags(), test_partitions_are_created_once()

### Community 63 - "network"
Cohesion: 0.28
Nodes (18): backfills(), company(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network() (+10 more)

### Community 64 - "network"
Cohesion: 0.27
Nodes (11): FakeReports, network(), test_connected_networks_reach_the_route(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_backfill_splits_the_period_in_weekly_chunks(), test_locked_chunk_goes_back_to_the_queue() (+3 more)

### Community 66 - "_route"
Cohesion: 0.15
Nodes (9): _route(), test_commission_tasks_are_registered_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_price_rule_tasks_are_registered(), test_deployed_envs_need_redis_and_resend(), test_purge_expired() (+1 more)

### Community 70 - "_ad_unit"
Cohesion: 0.18
Nodes (4): _ad_unit(), _line_item(), _optional_text(), test_writer_payloads_follow_genius()

### Community 75 - "fake_gam.py"
Cohesion: 0.14
Nodes (3): FakeEarnings, FakeExchangeRates, FakePageViews

### Community 79 - "_FixedClock"
Cohesion: 0.28
Nodes (3): _FixedClock, test_earnings_task_is_on_the_gam_queue(), test_months_backfill_then_previous_month_again()

### Community 81 - "logging"
Cohesion: 0.21
Nodes (3): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 82 - "gam/__init__.py"
Cohesion: 0.25
Nodes (4): check_access(), _fan_out(), schedule_imports(), schedule_tests()

### Community 83 - "dripping_server"
Cohesion: 0.27
Nodes (4): dripping_server(), start(), test_slow_body_stops_at_the_total_deadline_with_what_arrived(), test_slow_headers_count_against_the_total_deadline()

### Community 84 - "PublicOnlyBackend"
Cohesion: 0.22
Nodes (3): _public_transport(), PublicOnlyBackend, test_fetcher_never_connects_to_internal_addresses_or_other_ports()

### Community 88 - "report_query"
Cohesion: 0.33
Nodes (4): report_query(), _soap_date(), test_report_query_matches_unified_sync(), test_hourly_query_and_parse_keep_only_content_hash()

### Community 89 - "services"
Cohesion: 0.50
Nodes (3): use_services(), engine(), services()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 662 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `company` to `SoapGamWriter`, `enabled_site`, `OpenExchangeRates`, `test_commission_tasks.py`, `Settings`, `gam_metrics_tasks.py`, `test_price_rule_tasks.py`, `uuid`, `pytest`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `test_gam_tool_tasks.py`, `collections_abc`, `HttpPageFetcher`, `datetime`, `services.py`, `uuid`, `reward_tasks.py`, `test_ad_tag_tasks.py`, `network`, `network`, `_route`, `SoapReportClient`, `RestGamClient`, `dripping_server`, `services`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Are the 100 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 100 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `uuid` to `company`, `commission_tasks.py`, `Settings`, `metrics/__init__.py`, `gam_metrics_tasks.py`, `uuid`, `test_metrics_tasks.py`, `pytest`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `mcm_tasks.py`, `RecordingMailer`, `datetime`, `services.py`, `reward_tasks.py`, `app.py`, `gam/__init__.py`, `purge_tasks.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `company` be split into smaller, more focused modules?**
  _Cohesion score 0.11956521739130435 - nodes in this community are weakly interconnected._