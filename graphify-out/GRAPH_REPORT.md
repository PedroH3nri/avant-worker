# Graph Report - avant-worker  (2026-11-11)

## Corpus Check
- 83 files · ~47,929 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1304 nodes · 2679 edges · 70 communities (49 shown, 21 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 232 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ed7925d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- Services
- page_view_tasks.py
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
- test_earnings_tasks.py
- gam_metrics_tasks.py
- FakeGamClient
- test_key_value_tasks.py
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
- FakeSoapClient
- adapters/__init__.py
- adapters/__init__.py
- GamNotConfigured
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- mcm_tasks.py
- HttpPageFetcher
- RecordingMailer
- logging
- conftest.py
- backfill_metrics
- is_exempt
- ReportKind
- _route
- uuid
- test_reward_tasks.py
- test_key_value_tasks.py
- services.py
- .list_child_publishers
- test_the_writer_lets_other_gam_errors_through
- uuid
- SoapReportClient
- gam_client.py
- test_gam_tool_tasks.py
- app.py

## God Nodes (most connected - your core abstractions)
1. `Services` - 122 edges
2. `get_services()` - 62 edges
3. `company()` - 56 edges
4. `network()` - 49 edges
5. `SoapGamWriter` - 35 edges
6. `MemoryWriter` - 23 edges
7. `fake()` - 19 edges
8. `RestGamClient` - 17 edges
9. `_route()` - 17 edges
10. `count()` - 17 edges

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

## Communities (70 total, 21 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.05
Nodes (6): _ad_unit(), GamTargetNetworkWithTimeZone, _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "Services"
Cohesion: 0.05
Nodes (56): Services, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), backfills(), company(), count(), fake(), inventory() (+48 more)

### Community 2 - "page_view_tasks.py"
Cohesion: 0.18
Nodes (3): sync_mcm_earnings(), schedule_page_views(), sync_page_views()

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
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "OpenExchangeRates"
Cohesion: 0.11
Nodes (4): ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_schedule_tasks.py"
Cohesion: 0.06
Nodes (14): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered() (+6 more)

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), single_letter_names(), source_files()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.08
Nodes (19): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+11 more)

### Community 16 - "Settings"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "test_earnings_tasks.py"
Cohesion: 0.15
Nodes (6): months_to_fetch(), _shift(), FakeEarnings, _FixedClock, test_months_backfill_then_previous_month_again(), test_sync_stores_the_month_for_networks_in_avant()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.18
Nodes (6): _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later()

### Community 26 - "test_key_value_tasks.py"
Cohesion: 0.16
Nodes (5): _fault(), redis_services(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through()

### Community 27 - "test_tasks.py"
Cohesion: 0.19
Nodes (6): test_a_busy_lock_skips_the_run(), _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "pytest"
Cohesion: 0.14
Nodes (13): test_client_reads_mcm_earnings_money_in_micros(), client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 32 - "ad_tag_tasks.py"
Cohesion: 0.05
Nodes (17): GeoLiteCountries, CountryLookup, ensure_page_view_partitions_task(), _flush(), flush_page_views(), forget_network_ad_tags(), _hit(), _hits() (+9 more)

### Community 35 - "key_value_tasks.py"
Cohesion: 0.24
Nodes (3): get_services(), process_key_values(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.08
Nodes (7): GamNotConfigured, _import(), run_tool(), _try_later(), _updated(), test_a_long_run_renews_the_lock(), test_renewing_a_lost_lock_says_so()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.16
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 43 - "price_rule_tasks.py"
Cohesion: 0.08
Nodes (12): _key_ids(), _process_network(), create_price_rules(), _currency_and_time_zone(), _forget_cascades(), _forget_floors(), maintain_price_rule_partitions(), _reads_groone_network() (+4 more)

### Community 45 - "adapters/__init__.py"
Cohesion: 0.20
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 46 - "adapters/__init__.py"
Cohesion: 0.31
Nodes (3): channel(), publish(), test_publish_without_redis_is_a_no_op()

### Community 47 - "GamNotConfigured"
Cohesion: 0.13
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
Cohesion: 0.05
Nodes (10): HttpPageFetcher, public_address(), _public_transport(), PublicOnlyBackend, FakePageFetcher, test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_fetcher_refuses_internal_pages_and_redirects_to_them() (+2 more)

### Community 52 - "RecordingMailer"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "logging"
Cohesion: 0.14
Nodes (4): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls(), test_sync_without_key_does_nothing()

### Community 54 - "conftest.py"
Cohesion: 0.12
Nodes (6): use_services(), engine(), services(), FakeExchangeRates, FakePageViews, FakeReports

### Community 55 - "backfill_metrics"
Cohesion: 0.22
Nodes (4): backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 57 - "ReportKind"
Cohesion: 0.20
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

### Community 59 - "uuid"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 60 - "test_reward_tasks.py"
Cohesion: 0.07
Nodes (9): _batch(), _event(), _flush(), flush_reward_events(), forget_latest_reward_pages(), _lead(), purge_reward_batches_task(), redis_services() (+1 more)

### Community 61 - "test_key_value_tasks.py"
Cohesion: 0.20
Nodes (3): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_buffered_values_become_gam_values_once()

### Community 64 - ".list_child_publishers"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 66 - "uuid"
Cohesion: 0.25
Nodes (3): purge_expired(), test_deployed_envs_need_redis_and_resend(), test_purge_expired()

### Community 77 - "test_gam_tool_tasks.py"
Cohesion: 0.24
Nodes (3): soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 83 - "app.py"
Cohesion: 0.18
Nodes (3): create_app(), _failure(), _logging()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 635 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `OpenExchangeRates`, `test_commission_tasks.py`, `Settings`, `test_earnings_tasks.py`, `gam_metrics_tasks.py`, `test_key_value_tasks.py`, `test_tasks.py`, `ad_tag_tasks.py`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `price_rule_tasks.py`, `adapters/__init__.py`, `HttpPageFetcher`, `logging`, `conftest.py`, `test_reward_tasks.py`, `test_key_value_tasks.py`, `services.py`, `uuid`, `SoapReportClient`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Are the 97 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 97 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05153153153153153 - nodes in this community are weakly interconnected._
- **Why does `get_services()` connect `key_value_tasks.py` to `Services`, `page_view_tasks.py`, `commission_tasks.py`, `Settings`, `test_earnings_tasks.py`, `gam_metrics_tasks.py`, `FakeGamClient`, `test_metrics_tasks.py`, `ad_tag_tasks.py`, `tool_tasks.py`, `network_tasks.py`, `price_rule_tasks.py`, `mcm_tasks.py`, `RecordingMailer`, `logging`, `backfill_metrics`, `uuid`, `test_reward_tasks.py`, `services.py`, `.list_child_publishers`, `uuid`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Services` be split into smaller, more focused modules?**
  _Cohesion score 0.05013530836063239 - nodes in this community are weakly interconnected._