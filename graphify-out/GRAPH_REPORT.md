# Graph Report - avant-worker  (2026-11-05)

## Corpus Check
- 70 files · ~39,840 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1031 nodes · 2033 edges · 62 communities (36 shown, 26 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 151 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aac10a30`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- test_checklist_tasks.py
- Settings
- steps
- Avant: conexão com o GAM
- mcm_earnings_tasks.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- test_gam_client.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- RecordingMailer
- clean_code.py
- Services
- typing
- session-start.sh
- avant-worker
- ExchangeRateSource
- fake_gam.py
- gam_metrics_tasks.py
- FakeGamClient
- test_schedule_tasks.py
- _route
- Avant: grupos na Empresa e imagem da Empresa
- test_exchange_rates_tasks.py
- .list_child_publishers
- gam_client.py
- _last
- _HttpxResponse
- alert_tasks.py
- report_preview_tasks.py
- tool_tasks.py
- RestGamClient
- adapters/__init__.py
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- soap_writer
- services.py
- logging
- page_views.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- get_services
- gam_reports.py
- gam/__init__.py
- schedule_tasks.py
- test_time_limits.py
- app.py
- uuid
- SoapReportClient
- is_exempt
- checklist_tasks.py
- avant-worker
- _failure

## God Nodes (most connected - your core abstractions)
1. `Services` - 77 edges
2. `get_services()` - 47 edges
3. `company()` - 38 edges
4. `SoapGamWriter` - 33 edges
5. `network()` - 30 edges
6. `MemoryWriter` - 22 edges
7. `RestGamClient` - 17 edges
8. `fake()` - 17 edges
9. `_route()` - 16 edges
10. `publish()` - 15 edges

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

## Communities (62 total, 26 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "test_checklist_tasks.py"
Cohesion: 0.05
Nodes (10): HttpPageFetcher, public_address(), _public_transport(), PublicOnlyBackend, FakePageFetcher, test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_fetcher_refuses_internal_pages_and_redirects_to_them() (+2 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "mcm_earnings_tasks.py"
Cohesion: 0.25
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

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

### Community 10 - "test_gam_client.py"
Cohesion: 0.06
Nodes (16): ExchangeRatesUnavailable, OpenExchangeRates, test_client_reads_rates_as_decimals_and_fails_clearly(), client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived() (+8 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 14 - "clean_code.py"
Cohesion: 0.17
Nodes (5): check_file(), docstring_problems(), inline_comments(), single_letter_names(), source_files()

### Community 15 - "Services"
Cohesion: 0.05
Nodes (47): avant-worker, Contexto, issues e skills, GamNotConfigured, Services, refresh_levels(), test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), earnings() (+39 more)

### Community 22 - "ExchangeRateSource"
Cohesion: 0.11
Nodes (3): EarningsSource, ExchangeRateSource, PageViewSource

### Community 23 - "fake_gam.py"
Cohesion: 0.11
Nodes (4): FakeEarnings, FakeExchangeRates, FakePageViews, FakeReports

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.14
Nodes (8): ReportKind, _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later(), test_metrics_tasks_are_registered_on_the_gam_queue()

### Community 25 - "FakeGamClient"
Cohesion: 0.17
Nodes (4): use_services(), engine(), services(), FakeGamClient

### Community 27 - "_route"
Cohesion: 0.20
Nodes (9): _route(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_page_view_tasks_are_registered_on_the_default_queue(), test_report_preview_tasks_are_registered_on_the_default_queue() (+1 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "test_exchange_rates_tasks.py"
Cohesion: 0.18
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_sync_stores_closed_days_and_today(), test_sync_without_key_does_nothing()

### Community 34 - "alert_tasks.py"
Cohesion: 0.24
Nodes (3): check_alerts(), notify_alerts(), schedule_alerts()

### Community 36 - "tool_tasks.py"
Cohesion: 0.20
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 41 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "soap_writer"
Cohesion: 0.13
Nodes (5): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 46 - "logging"
Cohesion: 0.21
Nodes (3): configure_logging(), JsonFormatter, test_http_client_logs_do_not_carry_request_urls()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 50 - "get_services"
Cohesion: 0.14
Nodes (6): get_services(), purge_expired(), backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 51 - "gam_reports.py"
Cohesion: 0.13
Nodes (5): _ad_unit_path(), _integer(), parse_report(), test_parse_ad_unit_report(), test_parse_key_value_report_skips_rows_without_criteria()

### Community 54 - "test_time_limits.py"
Cohesion: 0.24
Nodes (4): _limits(), test_every_task_has_limits_below_the_rabbitmq_ack_timeout(), test_report_previews_stop_at_the_soft_limit(), test_tasks_finish_before_their_lock_expires()

### Community 56 - "uuid"
Cohesion: 0.25
Nodes (5): test_publish_without_redis_is_a_no_op(), test_deployed_envs_need_redis_and_resend(), test_purge_expired(), test_queue_comes_from_the_task_name(), test_checklists_go_out_in_short_batches_without_a_rate_limit_bucket()

### Community 57 - "SoapReportClient"
Cohesion: 0.09
Nodes (6): _classify(), report_query(), _soap_date(), SoapReportClient, test_report_is_read_from_a_temporary_file_as_it_streams(), test_report_query_matches_unified_sync()

### Community 59 - "checklist_tasks.py"
Cohesion: 0.21
Nodes (4): check_checklist(), _dispatch(), dispatch_checklists(), open_checklists()

### Community 62 - "avant-worker"
Cohesion: 0.12
Nodes (10): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis (+2 more)

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 508 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `test_checklist_tasks.py`, `Settings`, `tool_tasks.py`, `RestGamClient`, `network_tasks.py`, `test_gam_client.py`, `services.py`, `get_services`, `test_time_limits.py`, `avant-worker`, `gam_metrics_tasks.py`, `SoapReportClient`, `uuid`, `test_exchange_rates_tasks.py`, `FakeGamClient`, `gam_client.py`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `soap_writer`, `services.py`, `Services`, `gam_reports.py`, `gam_client.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_checklist_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05357142857142857 - nodes in this community are weakly interconnected._