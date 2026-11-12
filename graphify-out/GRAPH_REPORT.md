# Graph Report - wt-avant-worker-seguranca  (2026-11-11)

## Corpus Check
- 87 files · ~51,148 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .toml 1, .lock 1)

## Summary
- 1442 nodes · 2972 edges · 85 communities (47 shown, 38 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 275 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3fd05884`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- Services
- test_price_rule_tasks.py
- steps
- ReportKind
- page_fetcher.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- adapters/__init__.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- test_schedule_tasks.py
- clean_code.py
- SoapReportClient
- test_report_is_read_from_a_temporary_file_as_it_streams
- session-start.sh
- avant-worker
- .report
- months_to_fetch
- gam_metrics_tasks.py
- FakePageFetcher
- .list_mcm_earnings
- ad_tag_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- services.py
- test_commission_tasks.py
- test_mail_tasks.py
- BrokerSettings
- _HttpxResponse
- FakeGamClient
- _FixedClock
- tool_tasks.py
- _last
- updates
- public_address
- MemoryWriter
- network_tasks.py
- price_rule_tasks.py
- test_metrics_tasks.py
- get_services
- gam_reports.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- app.py
- uuid
- exchange_rate_tasks.py
- check_settings
- test_page_fetcher.py
- DeadlineStream
- RecordingMailer
- GeoLiteCountries
- reward_tasks.py
- test_ad_tag_tasks.py
- password_reset_tasks.py
- network
- _route
- gam_client.py
- ._statement
- _ad_unit
- GamTargetNetworkWithTimeZone
- gam_writer.py
- FakeLock
- sync_price_rule_hours
- collections_abc
- RecordingMailer
- test_tasks.py
- test_gam_tool_tasks.py
- RestGamClient
- FakeCountries
- _HttpxAuthRequest
- source_files
- _error
- .list_child_publishers
- FakeExchangeRates
- test_reward_tasks.py

## God Nodes (most connected - your core abstractions)
1. `Services` - 138 edges
2. `get_services()` - 65 edges
3. `company()` - 62 edges
4. `network()` - 55 edges
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

## Communities (85 total, 38 thin omitted)

### Community 1 - "Services"
Cohesion: 0.14
Nodes (18): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), test_sync_stores_the_month_for_networks_in_avant(), company(), test_discover_mcm_activates_the_registered_network(), test_sync_contracts_replaces_the_contract_when_the_revshare_changes(), staff() (+10 more)

### Community 2 - "test_price_rule_tasks.py"
Cohesion: 0.08
Nodes (21): CurrencyWriter, days_ago(), enabled_site(), FakeRedis, hour_row(), network_time_zone(), test_content_hash_and_groone_try_are_stored_in_the_same_call(), test_create_price_rules_creates_cascades_too() (+13 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (38): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, GITLEAKS_SHA256, GITLEAKS_VERSION, PGPASSWORD, POSTGRES_PASSWORD (+30 more)

### Community 4 - "ReportKind"
Cohesion: 0.20
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

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

### Community 10 - "adapters/__init__.py"
Cohesion: 0.05
Nodes (22): Onde está o trabalho, channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates, test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today() (+14 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "months_to_fetch"
Cohesion: 0.25
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.13
Nodes (8): _clear_queued(), _network(), _network_busy(), NetworkBusy, _reads_groone_network(), _store(), sync_metrics(), _try_later()

### Community 26 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 27 - "ad_tag_tasks.py"
Cohesion: 0.09
Nodes (9): CountryLookup, ensure_page_view_partitions_task(), _flush(), flush_page_views(), forget_network_ad_tags(), _hit(), _hits(), _optional_text() (+1 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "services.py"
Cohesion: 0.12
Nodes (3): use_services(), engine(), services()

### Community 30 - "test_commission_tasks.py"
Cohesion: 0.05
Nodes (22): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+14 more)

### Community 31 - "test_mail_tasks.py"
Cohesion: 0.23
Nodes (7): add_user(), count_resets(), test_password_reset_task_is_registered_on_the_mail_queue(), test_persistent_failure_stops_at_the_hourly_limit_without_sending(), test_task_ends_silently_when_the_account_does_not_exist(), test_task_retries_a_failed_sending_and_sends_only_one_email(), test_task_sends_the_reset_email_with_a_token_generated_here()

### Community 36 - "tool_tasks.py"
Cohesion: 0.16
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.12
Nodes (15): patterns, update-types, dependencias, imagens, dependency-name, patterns, interval, updates (+7 more)

### Community 39 - "public_address"
Cohesion: 0.20
Nodes (6): _embedded_ipv4(), public_address(), _public_ipv4(), test_public_addresses_are_allowed(), test_ipv6_addresses_with_a_public_ipv4_inside_are_allowed(), test_ipv6_addresses_with_an_internal_ipv4_inside_are_refused()

### Community 41 - "network_tasks.py"
Cohesion: 0.05
Nodes (24): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+16 more)

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.16
Nodes (6): create_price_rules(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), run_price_rules(), schedule_price_rule_hours()

### Community 44 - "test_metrics_tasks.py"
Cohesion: 0.12
Nodes (12): FakeReports, row(), _soap_source(), test_a_broken_report_file_is_a_temporary_failure(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_a_lost_lock_between_reports_sends_the_chunk_back_to_the_queue(), test_a_report_with_only_the_header_is_an_empty_period(), test_a_report_without_the_csv_header_is_a_temporary_failure() (+4 more)

### Community 46 - "get_services"
Cohesion: 0.14
Nodes (8): get_services(), backfill_metrics(), _fan_out(), _mark_queued(), schedule_metrics(), schedule_reprocess(), schedule_page_views(), sync_page_views()

### Community 47 - "gam_reports.py"
Cohesion: 0.13
Nodes (7): _ad_unit_path(), _hour(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria(), test_parse_report_keeps_groone_try_rows()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "app.py"
Cohesion: 0.19
Nodes (4): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls(), test_sync_without_key_does_nothing()

### Community 52 - "uuid"
Cohesion: 0.05
Nodes (16): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+8 more)

### Community 53 - "exchange_rate_tasks.py"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 54 - "check_settings"
Cohesion: 0.22
Nodes (4): _check_on_start(), check_settings(), _failure(), _logging()

### Community 55 - "test_page_fetcher.py"
Cohesion: 0.05
Nodes (19): HttpPageFetcher, _public_transport(), PublicOnlyBackend, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text(), dripping_server(), start(), FakeStream (+11 more)

### Community 60 - "reward_tasks.py"
Cohesion: 0.10
Nodes (7): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task()

### Community 61 - "test_ad_tag_tasks.py"
Cohesion: 0.27
Nodes (5): _page(), _tag(), test_buffer_becomes_page_views_and_health(), test_import_forgets_the_network_tags(), test_partitions_are_created_once()

### Community 63 - "network"
Cohesion: 0.28
Nodes (17): backfills(), count(), fake(), inventory(), network(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_failed_check_stops_before_importing() (+9 more)

### Community 66 - "_route"
Cohesion: 0.17
Nodes (11): _route(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue() (+3 more)

### Community 70 - "_ad_unit"
Cohesion: 0.22
Nodes (3): _ad_unit(), _line_item(), test_writer_payloads_follow_genius()

### Community 72 - "GamTargetNetworkWithTimeZone"
Cohesion: 0.20
Nodes (3): GamTargetNetworkWithTimeZone, _optional_text(), test_target_network_reads_a_missing_time_zone_as_empty()

### Community 77 - "sync_price_rule_hours"
Cohesion: 0.33
Nodes (3): _reads_groone_network(), _record_time_zone(), sync_price_rule_hours()

### Community 78 - "collections_abc"
Cohesion: 0.15
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 81 - "test_tasks.py"
Cohesion: 0.10
Nodes (7): _mailer(), Settings, purge_expired(), test_every_env_needs_redis_and_resend(), test_purge_expired(), test_queue_comes_from_the_task_name(), test_the_worker_mailer_is_always_resend()

### Community 82 - "test_gam_tool_tasks.py"
Cohesion: 0.06
Nodes (15): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), FakeTrafficWriter, _fault(), redis_services() (+7 more)

### Community 98 - "test_reward_tasks.py"
Cohesion: 0.22
Nodes (4): redis_services(), _reward(), test_buffer_becomes_metrics_and_leads(), test_import_forgets_the_latest_reward_pages()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 696 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `test_price_rule_tasks.py`, `adapters/__init__.py`, `SoapReportClient`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `services.py`, `test_commission_tasks.py`, `test_mail_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `test_metrics_tasks.py`, `get_services`, `app.py`, `uuid`, `test_page_fetcher.py`, `GeoLiteCountries`, `reward_tasks.py`, `test_ad_tag_tasks.py`, `network`, `sync_price_rule_hours`, `collections_abc`, `test_tasks.py`, `test_gam_tool_tasks.py`, `RestGamClient`, `FakeCountries`, `test_reward_tasks.py`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Are the 113 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 113 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Services` be split into smaller, more focused modules?**
  _Cohesion score 0.135632183908046 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `get_services` to `Services`, `tool_tasks.py`, `commission_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `sync_price_rule_hours`, `test_tasks.py`, `app.py`, `uuid`, `exchange_rate_tasks.py`, `months_to_fetch`, `gam_metrics_tasks.py`, `ad_tag_tasks.py`, `reward_tasks.py`, `services.py`, `password_reset_tasks.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_price_rule_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07529411764705882 - nodes in this community are weakly interconnected._