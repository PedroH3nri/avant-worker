# Graph Report - avant-worker  (2026-10-28)

## Corpus Check
- 50 files · ~30,190 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 681 nodes · 1267 edges · 49 communities (23 shown, 26 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ae5e6ed3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- OpenExchangeRates
- app.py
- logging
- steps
- Avant: conexão com o GAM
- Services
- Avant: models do MVP
- test_exchange_rates_tasks.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- test_gam_client.py
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- get_services
- clean_code.py
- avant-worker
- services.py
- session-start.sh
- avant-worker
- ExchangeRateSource
- gam_reports.py
- logging
- test_tasks.py
- network_tasks.py
- Settings
- Avant: grupos na Empresa e imagem da Empresa
- _failure
- parse_documents
- gam_client.py
- _route
- _HttpxResponse
- services.py
- _HttpxAuthRequest
- gam_metrics_tasks.py
- RestGamClient
- page_view_tasks.py
- exchange_rate_tasks.py
- publish
- _last
- .list_mcm_earnings
- purge_tasks.py
- _error
- datetime
- .list_child_publishers
- FakeCredentials

## God Nodes (most connected - your core abstractions)
1. `Services` - 48 edges
2. `get_services()` - 27 edges
3. `company()` - 23 edges
4. `network()` - 21 edges
5. `RestGamClient` - 17 edges
6. `fake()` - 17 edges
7. `ReportKind` - 14 edges
8. `client()` - 14 edges
9. `Groone Avant: contexto do projeto` - 14 edges
10. `publish()` - 13 edges

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

## Communities (49 total, 26 thin omitted)

### Community 0 - "OpenExchangeRates"
Cohesion: 0.12
Nodes (3): ExchangeRatesUnavailable, OpenExchangeRates, test_sync_stores_closed_days_and_today()

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "Services"
Cohesion: 0.09
Nodes (31): avant-worker, Contexto, issues e skills, Como funciona, GamNotConfigured, Services, FakeReports, test_sync_stores_the_month_for_networks_in_avant(), company() (+23 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "test_exchange_rates_tasks.py"
Cohesion: 0.20
Nodes (4): test_client_reads_mcm_earnings_money_in_micros(), test_client_reads_rates_as_decimals_and_fails_clearly(), test_sync_without_key_does_nothing(), test_http_errors_are_classified()

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "test_gam_client.py"
Cohesion: 0.24
Nodes (11): client(), record(), ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_network_and_admin_check(), handler(), test_network_failures_are_temporary() (+3 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "get_services"
Cohesion: 0.14
Nodes (7): get_services(), discover_mcm(), sync_contracts(), backfill_metrics(), _fan_out(), schedule_metrics(), schedule_reprocess()

### Community 14 - "clean_code.py"
Cohesion: 0.06
Nodes (29): Como trabalhar nos repositórios, Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos (+21 more)

### Community 15 - "avant-worker"
Cohesion: 0.25
Nodes (7): avant-worker, Desenvolvimento, Estrutura, Filas e tarefas, Imagem, Processos, Variáveis

### Community 16 - "services.py"
Cohesion: 0.07
Nodes (7): use_services(), engine(), services(), FakeEarnings, FakeExchangeRates, FakeGamClient, FakePageViews

### Community 22 - "ExchangeRateSource"
Cohesion: 0.10
Nodes (4): EarningsSource, ExchangeRateSource, PageViewSource, ReportSource

### Community 23 - "gam_reports.py"
Cohesion: 0.07
Nodes (11): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), ReportKind, _soap_date(), SoapReportClient (+3 more)

### Community 24 - "logging"
Cohesion: 0.21
Nodes (3): months_to_fetch(), _shift(), sync_mcm_earnings()

### Community 26 - "network_tasks.py"
Cohesion: 0.18
Nodes (7): check_access(), _fan_out(), _flat(), schedule_imports(), schedule_tests(), sync_network(), _updated()

### Community 28 - "Avant: grupos na Empresa e imagem da Empresa"
Cohesion: 0.20
Nodes (9): Avant: grupos na Empresa e imagem da Empresa, Decisões do Pedro (26/10), Herança de comissão e meta, Imagem da Empresa, Issues, Modelo de dados, Regras, Resumo (+1 more)

### Community 32 - "_route"
Cohesion: 0.33
Nodes (5): _route(), test_earnings_task_is_on_the_gam_queue(), test_exchange_rates_task_is_on_the_default_queue(), test_gam_tasks_are_registered_on_the_gam_queue(), test_page_view_tasks_are_registered_on_the_default_queue()

### Community 36 - "gam_metrics_tasks.py"
Cohesion: 0.20
Nodes (5): _network(), _reads_groone_network(), _store(), sync_metrics(), test_metrics_tasks_are_registered_on_the_gam_queue()

### Community 39 - "exchange_rate_tasks.py"
Cohesion: 0.21
Nodes (3): closed_days_to_fetch(), sync_exchange_rates(), test_closed_days_backfill_then_only_what_is_missing()

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 351 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `Services` to `OpenExchangeRates`, `services.py`, `gam_metrics_tasks.py`, `RestGamClient`, `test_exchange_rates_tasks.py`, `get_services`, `services.py`, `gam_reports.py`, `network_tasks.py`, `Settings`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Services` (e.g. with `OpenExchangeRates` and `RestGamClient`) actually correct?**
  _`Services` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `OpenExchangeRates` be split into smaller, more focused modules?**
  _Cohesion score 0.12380952380952381 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `RestGamClient` to `services.py`, `_HttpxAuthRequest`, `Services`, `test_exchange_rates_tasks.py`, `_last`, `.list_mcm_earnings`, `test_gam_client.py`, `.list_child_publishers`, `gam_client.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `company()` (e.g. with `Services` and `.trusted_uow()`) actually correct?**
  _`company()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._