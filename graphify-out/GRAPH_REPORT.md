# Graph Report - avant-worker  (2026-11-05)

## Corpus Check
- 71 files · ~40,284 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 1059 nodes · 2080 edges · 50 communities (34 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 153 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fd2ae3fb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- test_checklist_tasks.py
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
- RecordingMailer
- clean_code.py
- Services
- typing
- session-start.sh
- avant-worker
- ExchangeRateSource
- _FixedClock
- gam_metrics_tasks.py
- FakeGamClient
- test_schedule_tasks.py
- FakeExchangeRates
- Avant: grupos na Empresa e imagem da Empresa
- test_exchange_rates_tasks.py
- test_gam_client.py
- gam_client.py
- _HttpxResponse
- RestGamClient
- updates
- FakeReports
- MemoryWriter
- get_services
- .list_mcm_earnings
- _error
- soap_writer
- services.py
- app.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- FakeCredentials
- gam_reports.py
- is_exempt
- uuid
- avant-worker

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

## Communities (50 total, 16 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 1 - "test_checklist_tasks.py"
Cohesion: 0.05
Nodes (10): HttpPageFetcher, public_address(), _public_transport(), PublicOnlyBackend, FakePageFetcher, test_checklist_tasks_are_registered(), test_fetcher_never_connects_to_internal_addresses_or_other_ports(), test_fetcher_refuses_internal_pages_and_redirects_to_them() (+2 more)

### Community 2 - "mcm_earnings_tasks.py"
Cohesion: 0.21
Nodes (4): months_to_fetch(), _shift(), sync_mcm_earnings(), test_months_backfill_then_previous_month_again()

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

### Community 10 - "adapters/__init__.py"
Cohesion: 0.06
Nodes (9): channel(), publish(), ExchangeRatesUnavailable, OpenExchangeRates, MongoPageViews, parse_documents(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_stores_closed_days_and_today() (+1 more)

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
Nodes (49): avant-worker, Contexto, issues e skills, Services, refresh_levels(), FakeReports, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), earnings() (+41 more)

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.11
Nodes (10): backfill_metrics(), _fan_out(), _network(), _network_busy(), _reads_groone_network(), schedule_metrics(), schedule_reprocess(), _store() (+2 more)

### Community 25 - "FakeGamClient"
Cohesion: 0.08
Nodes (7): _mailer(), use_services(), Settings, engine(), services(), FakeGamClient, FakePageViews

### Community 26 - "test_schedule_tasks.py"
Cohesion: 0.12
Nodes (9): _route(), test_alert_tasks_are_registered_on_their_queues(), test_commission_tasks_are_registered_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue(), test_report_preview_tasks_are_registered_on_the_default_queue() (+1 more)

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 29 - "test_exchange_rates_tasks.py"
Cohesion: 0.18
Nodes (5): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing()

### Community 30 - "test_gam_client.py"
Cohesion: 0.19
Nodes (12): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check(), handler() (+4 more)

### Community 31 - "gam_client.py"
Cohesion: 0.13
Nodes (3): _delegation(), _last(), _revshare()

### Community 38 - "updates"
Cohesion: 0.18
Nodes (10): imagens, patterns, interval, updates, directory, groups, package-ecosystem, schedule (+2 more)

### Community 41 - "get_services"
Cohesion: 0.05
Nodes (18): GamNotConfigured, get_services(), discover_mcm(), sync_contracts(), check_access(), _fan_out(), _flat(), schedule_imports() (+10 more)

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "soap_writer"
Cohesion: 0.15
Nodes (5): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 45 - "services.py"
Cohesion: 0.10
Nodes (4): FakeEarnings, test_earnings_task_is_on_the_gam_queue(), test_deployed_envs_need_redis_and_resend(), test_queue_comes_from_the_task_name()

### Community 46 - "app.py"
Cohesion: 0.09
Nodes (7): create_app(), _failure(), _logging(), configure_logging(), JsonFormatter, BrokerSettings, test_http_client_logs_do_not_carry_request_urls()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 57 - "gam_reports.py"
Cohesion: 0.05
Nodes (13): _ad_unit_path(), _classify(), _integer(), parse_report(), _read_rows(), report_query(), ReportKind, _soap_date() (+5 more)

### Community 59 - "uuid"
Cohesion: 0.06
Nodes (15): check_alerts(), notify_alerts(), schedule_alerts(), check_checklist(), _dispatch(), dispatch_checklists(), open_checklists(), refresh_report_preview() (+7 more)

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 522 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `test_checklist_tasks.py`, `RestGamClient`, `get_services`, `adapters/__init__.py`, `services.py`, `gam_metrics_tasks.py`, `gam_reports.py`, `uuid`, `test_exchange_rates_tasks.py`, `FakeGamClient`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 57 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05794556628621598 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `adapters/__init__.py`, `soap_writer`, `services.py`, `Services`, `gam_reports.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_checklist_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05357142857142857 - nodes in this community are weakly interconnected._