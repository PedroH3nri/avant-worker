# Graph Report - avant-worker  (2026-11-04)

## Corpus Check
- 69 files · ~38,582 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 986 nodes · 1935 edges · 63 communities (32 shown, 31 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 146 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `480745ff`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_exchange_rates_tasks.py
- HttpPageFetcher
- Settings
- steps
- Avant: conexão com o GAM
- metrics/__init__.py
- Avant: models do MVP
- commission_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- test_gam_client.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- purge_tasks.py
- clean_code.py
- Services
- FakeGamClient
- session-start.sh
- avant-worker
- ExchangeRateSource
- gam_reports.py
- gam_metrics_tasks.py
- conftest.py
- test_schedule_tasks.py
- page_view_tasks.py
- Avant: grupos na Empresa e imagem da Empresa
- OpenExchangeRates
- app.py
- gam_client.py
- alert_tasks.py
- _HttpxResponse
- test_earnings_tasks.py
- mcm_tasks.py
- services
- RestGamClient
- page_view_tasks.py
- FakeReports
- MemoryWriter
- network_tasks.py
- .list_mcm_earnings
- _error
- soap_writer
- services.py
- fake_gam.py
- page_views.py
- Avant: repositório e plano do MVP
- Arquitetura do MVP do Avant
- RecordingMailer
- FakeReports
- .exchange_rates
- logs.py
- report_preview_tasks.py
- metrics/__init__.py
- schedule_tasks.py
- checklist_tasks.py
- source_files
- avant-worker
- _route
- FakePageFetcher

## God Nodes (most connected - your core abstractions)
1. `Services` - 75 edges
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

## Communities (63 total, 31 thin omitted)

### Community 0 - "test_exchange_rates_tasks.py"
Cohesion: 0.06
Nodes (5): _ad_unit(), _line_item(), _order_ref(), SoapGamWriter, test_writer_payloads_follow_genius()

### Community 2 - "Settings"
Cohesion: 0.24
Nodes (3): get_services(), _mailer(), Settings

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 5 - "metrics/__init__.py"
Cohesion: 0.11
Nodes (7): backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess(), sync_mcm_earnings(), schedule_page_views(), sync_page_views()

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
Cohesion: 0.08
Nodes (19): closed_days_to_fetch(), sync_exchange_rates(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_closed_days_backfill_then_only_what_is_missing(), test_exchange_rates_task_is_on_the_default_queue(), test_sync_without_key_does_nothing(), client(), record() (+11 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 14 - "clean_code.py"
Cohesion: 0.16
Nodes (5): check_file(), docstring_problems(), inline_comments(), is_exempt(), single_letter_names()

### Community 15 - "Services"
Cohesion: 0.05
Nodes (49): avant-worker, Contexto, issues e skills, GamNotConfigured, Services, FakePageViews, test_alerts_fire_once_and_mail_the_list_once(), test_open_checklists_checks_sites_that_earned_last_month(), earnings() (+41 more)

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "gam_reports.py"
Cohesion: 0.07
Nodes (10): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), _soap_date(), SoapReportClient, test_parse_ad_unit_report() (+2 more)

### Community 24 - "gam_metrics_tasks.py"
Cohesion: 0.15
Nodes (7): ReportKind, _network(), _network_busy(), _reads_groone_network(), _store(), sync_metrics(), _try_later()

### Community 25 - "conftest.py"
Cohesion: 0.18
Nodes (4): use_services(), engine(), services(), FakeEarnings

### Community 26 - "test_schedule_tasks.py"
Cohesion: 0.16
Nodes (3): test_alert_tasks_are_registered_on_their_queues(), test_report_preview_tasks_are_registered_on_the_default_queue(), test_schedule_tasks_are_registered_on_their_queues()

### Community 27 - "page_view_tasks.py"
Cohesion: 0.20
Nodes (4): _import(), run_tool(), _try_later(), _updated()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 32 - "alert_tasks.py"
Cohesion: 0.15
Nodes (6): check_alerts(), notify_alerts(), schedule_alerts(), test_publish_without_redis_is_a_no_op(), test_deployed_envs_need_redis_and_resend(), test_purge_expired()

### Community 35 - "mcm_tasks.py"
Cohesion: 0.25
Nodes (3): Importação, discover_mcm(), sync_contracts()

### Community 41 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 42 - ".list_mcm_earnings"
Cohesion: 0.22
Nodes (3): _micros(), _month(), test_client_reads_mcm_earnings_money_in_micros()

### Community 44 - "soap_writer"
Cohesion: 0.14
Nodes (5): FakeSoapClient, FakeSoapService, soap_writer(), test_writer_reads_seller_in_groone_network(), test_writer_skips_what_already_exists()

### Community 48 - "Avant: repositório e plano do MVP"
Cohesion: 0.17
Nodes (11): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+3 more)

### Community 49 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 55 - "logs.py"
Cohesion: 0.15
Nodes (4): _failure(), _logging(), configure_logging(), JsonFormatter

### Community 57 - "metrics/__init__.py"
Cohesion: 0.24
Nodes (3): months_to_fetch(), _shift(), test_months_backfill_then_previous_month_again()

### Community 62 - "avant-worker"
Cohesion: 0.22
Nodes (8): avant-worker, Como funciona, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 65 - "_route"
Cohesion: 0.20
Nodes (9): _route(), test_checklist_tasks_are_registered(), test_commission_tasks_are_registered_on_the_default_queue(), test_earnings_task_is_on_the_gam_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_tool_task_is_registered(), test_metrics_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue() (+1 more)

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 487 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `test_exchange_rates_tasks.py`, `HttpPageFetcher`, `Settings`, `alert_tasks.py`, `RestGamClient`, `network_tasks.py`, `test_gam_client.py`, `services.py`, `.exchange_rates`, `gam_reports.py`, `gam_metrics_tasks.py`, `conftest.py`, `page_view_tasks.py`, `OpenExchangeRates`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 55 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_exchange_rates_tasks.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Why does `SoapGamWriter` connect `test_exchange_rates_tasks.py` to `soap_writer`, `services.py`, `Services`, `gam_reports.py`, `OpenExchangeRates`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._