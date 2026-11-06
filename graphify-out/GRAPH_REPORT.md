# Graph Report - avant-worker  (2026-11-06)

## Corpus Check
- 73 files · ~42,197 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1126 nodes · 2197 edges · 81 communities (41 shown, 40 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8c1946f3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SoapGamWriter
- test_checklist_tasks.py
- metrics/__init__.py
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
- Services
- test_tasks.py
- session-start.sh
- avant-worker
- .report
- test_earnings_tasks.py
- gam_metrics_tasks.py
- report_preview_tasks.py
- test_key_value_tasks.py
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
- get_services
- .list_mcm_earnings
- _error
- soap_writer
- parse_documents
- parse_report
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- page_view_tasks.py
- HttpPageFetcher
- open_checklists
- logging
- services.py
- _last
- test_gam_tool_tasks.py
- ReportKind
- test_report_is_read_from_a_temporary_file_as_it_streams
- UUID
- PublicOnlyBackend
- test_key_value_tasks.py
- avant-worker
- _public_transport
- .list_child_publishers
- FakeCredentials
- is_exempt
- FakePageFetcher
- SoapReportClient

## God Nodes (most connected - your core abstractions)
1. `Services` - 87 edges
2. `get_services()` - 50 edges
3. `company()` - 40 edges
4. `SoapGamWriter` - 35 edges
5. `network()` - 33 edges
6. `MemoryWriter` - 23 edges
7. `fake()` - 18 edges
8. `RestGamClient` - 17 edges
9. `_route()` - 16 edges
10. `inventory()` - 15 edges

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

## Communities (81 total, 40 thin omitted)

### Community 0 - "SoapGamWriter"
Cohesion: 0.05
Nodes (6): _ad_unit(), _line_item(), _order_ref(), _refused_values(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 2 - "metrics/__init__.py"
Cohesion: 0.12
Nodes (8): backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess(), months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.13
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
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "adapters/__init__.py"
Cohesion: 0.12
Nodes (4): ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today()

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "test_schedule_tasks.py"
Cohesion: 0.05
Nodes (14): _failure(), _logging(), _route(), RecordingMailer, test_alert_tasks_are_registered_on_their_queues(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue() (+6 more)

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), single_letter_names(), source_files()

### Community 15 - "Services"
Cohesion: 0.06
Nodes (52): avant-worker, Contexto, issues e skills, Services, refresh_levels(), test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), earnings(), FixedClock (+44 more)

### Community 16 - "test_tasks.py"
Cohesion: 0.09
Nodes (6): _mailer(), BrokerSettings, Settings, purge_expired(), test_deployed_envs_need_redis_and_resend(), test_queue_comes_from_the_task_name()

### Community 22 - ".report"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.14
Nodes (7): _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later(), test_metrics_tasks_are_registered_on_the_gam_queue()

### Community 26 - "test_key_value_tasks.py"
Cohesion: 0.16
Nodes (7): test_a_busy_lock_skips_the_run(), _fault(), redis_services(), test_the_writer_drops_refused_values_and_sends_the_rest_again(), create(), test_the_writer_lets_other_gam_errors_through(), test_report_previews_stop_at_the_soft_limit()

### Community 27 - "test_time_limits.py"
Cohesion: 0.24
Nodes (4): _limits(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_tasks_finish_before_their_lock_expires()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 30 - "test_gam_client.py"
Cohesion: 0.16
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 34 - "FakeGamClient"
Cohesion: 0.09
Nodes (7): use_services(), engine(), services(), FakeEarnings, FakeExchangeRates, FakeGamClient, FakePageViews

### Community 35 - "key_value_tasks.py"
Cohesion: 0.22
Nodes (3): process_key_values(), _process_network(), refresh_key_value_networks()

### Community 36 - "tool_tasks.py"
Cohesion: 0.09
Nodes (6): GamNotConfigured, _key_ids(), _import(), run_tool(), _try_later(), _updated()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "get_services"
Cohesion: 0.14
Nodes (8): get_services(), check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 45 - "parse_documents"
Cohesion: 0.20
Nodes (3): MongoPageViews, parse_documents(), test_parse_documents_reads_the_data_counter()

### Community 47 - "parse_report"
Cohesion: 0.22
Nodes (5): _ad_unit_path(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "page_view_tasks.py"
Cohesion: 0.14
Nodes (4): channel(), publish(), schedule_page_views(), sync_page_views()

### Community 51 - "HttpPageFetcher"
Cohesion: 0.17
Nodes (3): HttpPageFetcher, test_fetcher_refuses_internal_pages_and_redirects_to_them(), test_fetcher_sends_the_avant_user_agent_and_reads_only_text()

### Community 52 - "open_checklists"
Cohesion: 0.25
Nodes (3): _dispatch(), dispatch_checklists(), open_checklists()

### Community 53 - "logging"
Cohesion: 0.12
Nodes (8): configure_logging(), JsonFormatter, _last_import(), closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_http_client_logs_do_not_carry_request_urls(), test_sync_without_key_does_nothing()

### Community 56 - "test_gam_tool_tasks.py"
Cohesion: 0.24
Nodes (3): soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 57 - "ReportKind"
Cohesion: 0.18
Nodes (5): _read_rows(), report_query(), ReportKind, _soap_date(), test_report_query_matches_unified_sync()

### Community 59 - "UUID"
Cohesion: 0.16
Nodes (4): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist()

### Community 61 - "test_key_value_tasks.py"
Cohesion: 0.20
Nodes (3): FakeTrafficWriter, test_a_gam_failure_puts_the_pairs_back_and_a_key_without_id_is_not_seen(), test_buffered_values_become_gam_values_once()

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 563 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `SoapGamWriter`, `FakeGamClient`, `key_value_tasks.py`, `SoapReportClient`, `RestGamClient`, `tool_tasks.py`, `get_services`, `adapters/__init__.py`, `parse_documents`, `test_tasks.py`, `HttpPageFetcher`, `logging`, `services.py`, `gam_metrics_tasks.py`, `test_key_value_tasks.py`, `test_time_limits.py`, `test_key_value_tasks.py`, `gam_client.py`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 50 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `SoapGamWriter` be split into smaller, more focused modules?**
  _Cohesion score 0.05220288781932617 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `SoapGamWriter` to `tool_tasks.py`, `Services`, `page_view_tasks.py`, `services.py`, `test_gam_tool_tasks.py`, `gam_client.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SoapGamWriter` (e.g. with `Services` and `soap_writer()`) actually correct?**
  _`SoapGamWriter` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `metrics/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11857707509881422 - nodes in this community are weakly interconnected._