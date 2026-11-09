# Graph Report - avant-worker  (2026-11-09)

## Corpus Check
- 76 files · ~43,305 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1164 nodes · 2286 edges · 85 communities (50 shown, 35 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 149 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `880b2eec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- Services
- mcm_earnings_tasks.py
- steps
- Avant: conexão com o GAM
- _soap_source
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- adapters/__init__.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- test_schedule_tasks.py
- clean_code.py
- test_commission_tasks.py
- test_tasks.py
- session-start.sh
- avant-worker
- .report
- test_earnings_tasks.py
- gam_metrics_tasks.py
- report_preview_tasks.py
- pytest
- test_time_limits.py
- Avant: grupos na Empresa e imagem da Empresa
- schedule_tasks.py
- test_gam_client.py
- gam_client.py
- _HttpxResponse
- FakeGamClient
- key_value_tasks.py
- tool_tasks.py
- RestGamClient
- updates
- _HttpxAuthRequest
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- fake_gam.py
- test_gam_tool_tasks.py
- parse_documents
- test_metrics_tasks.py
- parse_report
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- get_services
- test_checklist_tasks.py
- open_checklists
- app.py
- company
- test_reward_tasks.py
- ReportKind
- test_report_is_read_from_a_temporary_file_as_it_streams
- UUID
- reward_tasks.py
- test_key_value_tasks.py
- gam_writer.py
- test_page_views_tasks.py
- closed_days_to_fetch
- FakeCredentials
- purge_tasks.py
- .report
- SoapReportClient
- test_tasks.py
- report_query
- _classify
- source_files

## God Nodes (most connected - your core abstractions)
1. `Services` - 94 edges
2. `get_services()` - 53 edges
3. `company()` - 42 edges
4. `SoapGamWriter` - 35 edges
5. `network()` - 35 edges
6. `MemoryWriter` - 23 edges
7. `fake()` - 18 edges
8. `RestGamClient` - 17 edges
9. `_route()` - 16 edges
10. `ReportKind` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Sites e ad units` --references--> `network()`  [INFERRED]
  docs/decisoes/06-endpoints-api.md → tests/test_gam_tasks.py
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam/mcm_tasks.py
- `Como trabalhar nos repositórios` --references--> `main()`  [INFERRED]
  docs/contexto.md → scripts/clean_code.py
- `Ambientes, deploy e backup` --references--> `main()`  [INFERRED]
  docs/decisoes/02-arquitetura.md → scripts/clean_code.py
- `Pipeline` --references--> `main()`  [INFERRED]
  docs/decisoes/07-repositorios-e-plano.md → scripts/clean_code.py

## Import Cycles
- None detected.

## Communities (85 total, 35 thin omitted)

### Community 0 - "SoapGamWriter"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "Services"
Cohesion: 0.27
Nodes (15): Services, backfills(), count(), fake(), inventory(), test_check_access_and_schedulers(), test_check_access_imports_before_asking_for_the_history(), test_discover_mcm_activates_the_registered_network() (+7 more)

### Community 2 - "mcm_earnings_tasks.py"
Cohesion: 0.24
Nodes (3): months_to_fetch(), _shift(), sync_mcm_earnings()

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
Cohesion: 0.16
Nodes (8): _calculate(), calculate_recent_commissions(), calculate_today_commissions(), close_commissions(), previous_month(), _today(), transfer_clients(), _warn_if_late()

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "adapters/__init__.py"
Cohesion: 0.07
Nodes (9): channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates, _batch(), _event(), _flush(), _lead() (+1 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_schedule_tasks.py"
Cohesion: 0.06
Nodes (13): _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue() (+5 more)

### Community 14 - "clean_code.py"
Cohesion: 0.18
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "test_commission_tasks.py"
Cohesion: 0.06
Nodes (23): avant-worker, Contexto, issues e skills, avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem (+15 more)

### Community 16 - "test_tasks.py"
Cohesion: 0.15
Nodes (3): _mailer(), BrokerSettings, Settings

### Community 22 - ".report"
Cohesion: 0.13
Nodes (3): EarningsSource, ExchangeRateSource, PageViewSource

### Community 23 - "test_earnings_tasks.py"
Cohesion: 0.23
Nodes (4): FakeEarnings, _FixedClock, test_months_backfill_then_previous_month_again(), test_sync_stores_the_month_for_networks_in_avant()

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.12
Nodes (10): backfill_metrics(), _fan_out(), _network(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store() (+2 more)

### Community 26 - "pytest"
Cohesion: 0.29
Nodes (3): test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_without_key_does_nothing(), redis_services()

### Community 27 - "test_time_limits.py"
Cohesion: 0.22
Nodes (5): _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "test_gam_client.py"
Cohesion: 0.18
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 31 - "gam_client.py"
Cohesion: 0.14
Nodes (3): _error(), _message(), _revshare()

### Community 34 - "FakeGamClient"
Cohesion: 0.17
Nodes (4): use_services(), engine(), services(), FakeGamClient

### Community 35 - "key_value_tasks.py"
Cohesion: 0.17
Nodes (4): _key_ids(), process_key_values(), _process_network(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.11
Nodes (5): GamNotConfigured, _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "network_tasks.py"
Cohesion: 0.17
Nodes (8): check_access(), _fan_out(), _flat(), _last_import(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.18
Nodes (4): _delegation(), _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "test_gam_tool_tasks.py"
Cohesion: 0.10
Nodes (9): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists(), _fault(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create() (+1 more)

### Community 45 - "parse_documents"
Cohesion: 0.15
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 46 - "test_metrics_tasks.py"
Cohesion: 0.22
Nodes (10): FakeReports, network(), reports(), row(), test_a_failing_chunk_does_not_stop_the_rest_of_the_history(), test_backfill_splits_the_period_in_weekly_chunks(), test_locked_chunk_goes_back_to_the_queue(), test_schedules_cover_today_and_the_reprocess_window() (+2 more)

### Community 47 - "parse_report"
Cohesion: 0.14
Nodes (5): _ad_unit_path(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "get_services"
Cohesion: 0.15
Nodes (5): get_services(), discover_mcm(), sync_contracts(), schedule_page_views(), sync_page_views()

### Community 51 - "test_checklist_tasks.py"
Cohesion: 0.06
Nodes (9): HttpPageFetcher, public_address(), _public_transport(), PublicOnlyBackend, FakePageFetcher, test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text() (+1 more)

### Community 52 - "open_checklists"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "app.py"
Cohesion: 0.09
Nodes (6): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 55 - "company"
Cohesion: 0.18
Nodes (8): test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), company(), staff(), test_a_busy_network_waits_and_tries_again(), test_run_tool_configures_the_network(), test_previews_are_refreshed_once_and_again_when_old(), test_due_reports_go_out_once()

### Community 56 - "test_reward_tasks.py"
Cohesion: 0.18
Nodes (3): redis_services(), _reward(), test_import_forgets_the_latest_reward_pages()

### Community 59 - "UUID"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 60 - "reward_tasks.py"
Cohesion: 0.21
Nodes (4): flush_reward_events(), forget_latest_reward_pages(), purge_reward_batches_task(), test_buffer_becomes_metrics_and_leads()

### Community 61 - "test_key_value_tasks.py"
Cohesion: 0.14
Nodes (4): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_buffered_values_become_gam_values_once(), test_connected_networks_reach_the_route()

### Community 63 - "test_page_views_tasks.py"
Cohesion: 0.31
Nodes (4): FakePageViews, page_views(), test_schedule_uses_sao_paulo_dates_and_skips_without_mongo(), test_sync_page_views_stores_and_replaces_counts()

### Community 64 - "closed_days_to_fetch"
Cohesion: 0.25
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

### Community 77 - "test_tasks.py"
Cohesion: 0.33
Nodes (3): test_deployed_envs_need_redis_and_resend(), test_purge_expired(), test_queue_comes_from_the_task_name()

### Community 78 - "report_query"
Cohesion: 0.40
Nodes (3): report_query(), _soap_date(), test_report_query_matches_unified_sync()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 581 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `adapters/__init__.py`, `test_commission_tasks.py`, `test_tasks.py`, `test_earnings_tasks.py`, `gam_metrics_tasks.py`, `pytest`, `test_time_limits.py`, `FakeGamClient`, `key_value_tasks.py`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `fake_gam.py`, `parse_documents`, `test_metrics_tasks.py`, `get_services`, `test_checklist_tasks.py`, `app.py`, `services.py`, `company`, `test_reward_tasks.py`, `reward_tasks.py`, `test_key_value_tasks.py`, `test_page_views_tasks.py`, `SoapReportClient`, `test_tasks.py`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 50 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.0567287784679089 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `SoapGamWriter` to `Services`, `key_value_tasks.py`, `adapters/__init__.py`, `test_gam_tool_tasks.py`, `services.py`, `gam_writer.py`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SoapGamWriter` (e.g. with `Services` and `soap_writer()`) actually correct?**
  _`SoapGamWriter` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._