# Graph Report - avant-worker  (2026-10-24)

## Corpus Check
- 35 files · ~25,730 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 6, .lock 1)

## Summary
- 526 nodes · 906 edges · 29 communities (16 shown, 13 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 78 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a4707ba`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- RestGamClient
- app.py
- gam_client.py
- steps
- Avant: conexão com o GAM
- test_gam_tasks.py
- Avant: models do MVP
- test_gam_client.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- Arquitetura do MVP do Avant
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- metrics.py
- clean_code.py
- avant-worker
- services.py
- session-start.sh
- avant-worker
- _HttpxResponse
- test_metrics_tasks.py
- .gam
- _last
- _HttpxAuthRequest
- _error
- .list_child_publishers

## God Nodes (most connected - your core abstractions)
1. `Services` - 37 edges
2. `get_services()` - 19 edges
3. `ReportKind` - 18 edges
4. `company()` - 18 edges
5. `network()` - 16 edges
6. `RestGamClient` - 14 edges
7. `client()` - 14 edges
8. `fake()` - 14 edges
9. `Groone Avant: contexto do projeto` - 14 edges
10. `sync_metrics()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam.py
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

## Communities (29 total, 13 thin omitted)

### Community 1 - "app.py"
Cohesion: 0.06
Nodes (11): create_app(), _failure(), _logging(), _route(), configure_logging(), JsonFormatter, BrokerSettings, test_gam_tasks_are_registered_on_the_gam_queue() (+3 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "Avant: conexão com o GAM"
Cohesion: 0.20
Nodes (9): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Importação, Resumo (+1 more)

### Community 5 - "test_gam_tasks.py"
Cohesion: 0.14
Nodes (26): avant-worker, Contexto, issues e skills, Como funciona, Services, FakeReports, company(), count(), fake() (+18 more)

### Community 6 - "Avant: models do MVP"
Cohesion: 0.07
Nodes (26): Acesso, AdUnit, ApiKey, AuditLog, Avant: models do MVP, Company, Decisões de Pedro (22/10/2026), Empresa e equipe (+18 more)

### Community 7 - "test_gam_client.py"
Cohesion: 0.14
Nodes (13): client(), record(), FakeCredentials, ok(), test_ad_units_without_root_and_archived(), test_child_publishers(), test_http_errors_are_classified(), test_network_and_admin_check() (+5 more)

### Community 8 - "Groone Avant: contexto do projeto"
Cohesion: 0.12
Nodes (14): Arquitetura, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação, Modelo de contas (+6 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "Arquitetura do MVP do Avant"
Cohesion: 0.15
Nodes (12): Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões, Modelo de dados (+4 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "metrics.py"
Cohesion: 0.06
Nodes (21): channel(), publish(), get_services(), check_access(), discover_mcm(), _fan_out(), _flat(), schedule_imports() (+13 more)

### Community 14 - "clean_code.py"
Cohesion: 0.08
Nodes (17): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+9 more)

### Community 15 - "avant-worker"
Cohesion: 0.29
Nodes (6): avant-worker, Desenvolvimento, Filas e tarefas, Imagem, Processos, Variáveis

### Community 16 - "services.py"
Cohesion: 0.06
Nodes (6): _mailer(), use_services(), Settings, engine(), services(), FakeGamClient

### Community 23 - "test_metrics_tasks.py"
Cohesion: 0.06
Nodes (12): _ad_unit_path(), _classify(), _integer(), parse_report(), report_query(), ReportKind, _soap_date(), SoapReportClient (+4 more)

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 280 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `test_gam_tasks.py` to `RestGamClient`, `metrics.py`, `services.py`, `test_metrics_tasks.py`, `.gam`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `Services` (e.g. with `RestGamClient` and `SoapReportClient`) actually correct?**
  _`Services` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06363636363636363 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `RestGamClient` to `gam_client.py`, `test_gam_tasks.py`, `test_gam_client.py`, `services.py`, `.gam`, `_last`, `_HttpxAuthRequest`, `.list_child_publishers`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ReportKind` (e.g. with `ReportSource` and `_store()`) actually correct?**
  _`ReportKind` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Should `steps` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._