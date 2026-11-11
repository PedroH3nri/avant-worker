# Graph Report - avant-worker  (2026-11-11)

## Corpus Check
- 83 files · ~48,180 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1312 nodes · 2715 edges · 81 communities (49 shown, 32 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 239 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0b486ce`
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
- test_schedule_tasks.py
- clean_code.py
- test_commission_tasks.py
- Settings
- session-start.sh
- avant-worker
- ExchangeRateSource
- months_to_fetch
- gam_metrics_tasks.py
- FakeGamClient
- test_price_rule_tasks.py
- test_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- test_metrics_tasks.py
- pytest
- _error
- ad_tag_tasks.py
- _HttpxResponse
- conftest.py
- key_value_tasks.py
- tool_tasks.py
- RestGamClient
- updates
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- price_rule_tasks.py
- test_gam_tool_tasks.py
- adapters/__init__.py
- adapters/__init__.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- mcm_tasks.py
- HttpPageFetcher
- RecordingMailer
- app.py
- conftest.py
- backfill_metrics
- is_exempt
- ReportKind
- _route
- uuid
- test_reward_tasks.py
- test_key_value_tasks.py
- network
- Services
- uuid
- gam_client.py
- SoapReportClient
- ._first
- _ad_unit
- gam_client.py
- GamTargetNetworkWithTimeZone
- _refused_values
- _last
- FakeExchangeRates
- FakeLock
- FakePageFetcher
- _FixedClock

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

## Communities (81 total, 32 thin omitted)

### Community 1 - "company"
Cohesion: 0.12
Nodes (13): _tag(), test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), company(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network() (+5 more)

### Community 2 - "enabled_site"
Cohesion: 0.10
Nodes (10): enabled_site(), FakeRedis, test_create_price_rules_creates_cascades_too(), test_create_price_rules_keeps_the_count_when_a_cascade_fails(), test_run_price_rules_forgets_and_counts_hashes_when_a_cascade_fails(), explode(), test_run_price_rules_forgets_cascade_cache_when_start_changed(), test_run_price_rules_keeps_cascade_cache_when_start_did_not_change() (+2 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

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
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_schedule_tasks.py"
Cohesion: 0.05
Nodes (15): _failure(), _logging(), _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue() (+7 more)

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), single_letter_names(), source_files()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.06
Nodes (21): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+13 more)

### Community 16 - "Settings"
Cohesion: 0.15
Nodes (4): create_app(), _mailer(), BrokerSettings, Settings

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "months_to_fetch"
Cohesion: 0.25
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.15
Nodes (7): _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later(), test_metrics_tasks_are_registered_on_the_gam_queue()

### Community 26 - "test_price_rule_tasks.py"
Cohesion: 0.15
Nodes (11): CurrencyWriter, days_ago(), hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_hourly_query_and_parse_keep_only_content_hash(), test_hours_rules_and_engine_run_in_the_network_currency(), test_sync_asks_gam_once_for_currency_and_time_zone() (+3 more)

### Community 27 - "test_tasks.py"
Cohesion: 0.13
Nodes (8): test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_a_busy_lock_skips_the_run(), redis_services(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "pytest"
Cohesion: 0.13
Nodes (13): client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 32 - "ad_tag_tasks.py"
Cohesion: 0.05
Nodes (16): GeoLiteCountries, CountryLookup, ensure_page_view_partitions_task(), _flush(), flush_page_views(), forget_network_ad_tags(), _hit(), _hits() (+8 more)

### Community 35 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.16
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.11
Nodes (10): create_price_rules(), _currency_and_time_zone(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network(), _record_time_zone(), run_price_rules() (+2 more)

### Community 44 - "test_gam_tool_tasks.py"
Cohesion: 0.09
Nodes (9): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+1 more)

### Community 45 - "adapters/__init__.py"
Cohesion: 0.09
Nodes (5): public_address(), MongoPageViews, parse_documents(), test_public_addresses_are_allowed(), test_parse_documents_reads_the_data_counter()

### Community 46 - "adapters/__init__.py"
Cohesion: 0.33
Nodes (3): channel(), publish(), test_publish_without_redis_is_a_no_op()

### Community 47 - "GamNotConfigured"
Cohesion: 0.18
Nodes (7): _ad_unit_path(), _hour(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_parse_report_keeps_groone_try_rows()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "mcm_tasks.py"
Cohesion: 0.15
Nodes (5): get_services(), discover_mcm(), sync_contracts(), schedule_page_views(), sync_page_views()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.09
Nodes (5): HttpPageFetcher, _public_transport(), PublicOnlyBackend, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "RecordingMailer"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "app.py"
Cohesion: 0.10
Nodes (7): configure_logging(), JsonFormatter, closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_http_client_logs_do_not_carry_request_urls(), test_sync_without_key_does_nothing()

### Community 54 - "conftest.py"
Cohesion: 0.09
Nodes (6): use_services(), engine(), services(), FakeEarnings, FakePageViews, FakeReports

### Community 55 - "backfill_metrics"
Cohesion: 0.20
Nodes (4): backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 57 - "ReportKind"
Cohesion: 0.20
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

### Community 59 - "uuid"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 60 - "test_reward_tasks.py"
Cohesion: 0.08
Nodes (9): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task(), redis_services() (+1 more)

### Community 61 - "test_key_value_tasks.py"
Cohesion: 0.20
Nodes (3): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_buffered_values_become_gam_values_once()

### Community 63 - "network"
Cohesion: 0.27
Nodes (18): backfills(), count(), fake(), inventory(), network(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network() (+10 more)

### Community 64 - "Services"
Cohesion: 0.15
Nodes (9): Services, test_sync_stores_the_month_for_networks_in_avant(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_backfill_splits_the_period_in_weekly_chunks(), test_locked_chunk_goes_back_to_the_queue(), test_schedules_cover_today_and_the_reprocess_window() (+1 more)

### Community 66 - "uuid"
Cohesion: 0.20
Nodes (4): purge_expired(), test_deployed_envs_need_redis_and_resend(), test_purge_expired(), test_queue_comes_from_the_task_name()

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 637 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `company`, `enabled_site`, `OpenExchangeRates`, `test_commission_tasks.py`, `Settings`, `gam_metrics_tasks.py`, `test_price_rule_tasks.py`, `test_tasks.py`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `price_rule_tasks.py`, `adapters/__init__.py`, `mcm_tasks.py`, `HttpPageFetcher`, `app.py`, `conftest.py`, `backfill_metrics`, `test_reward_tasks.py`, `test_key_value_tasks.py`, `network`, `uuid`, `SoapReportClient`, `FakeExchangeRates`, `.gam`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Are the 100 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 100 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `mcm_tasks.py` to `commission_tasks.py`, `Settings`, `months_to_fetch`, `gam_metrics_tasks.py`, `FakeGamClient`, `test_metrics_tasks.py`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `RecordingMailer`, `app.py`, `conftest.py`, `backfill_metrics`, `uuid`, `test_reward_tasks.py`, `Services`, `uuid`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `company` be split into smaller, more focused modules?**
  _Cohesion score 0.11956521739130435 - nodes in this community are weakly interconnected._