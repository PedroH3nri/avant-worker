# Graph Report - avant-worker  (2026-10-24)

## Corpus Check
- 32 files · ~22,942 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 5, .lock 1)

## Summary
- 432 nodes · 666 edges · 28 communities (15 shown, 13 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `27b9918b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- RestGamClient
- services.py
- app.py
- steps
- gam.py
- test_gam_tasks.py
- Avant: models do MVP
- test_gam_client.py
- Groone Avant: contexto do projeto
- Avant: endpoints da API do MVP
- Arquitetura do MVP do Avant
- Requisitos do novo SaaS AdTech Groone
- Avant: fluxos de login e convite
- Avant: conexão com o GAM
- clean_code.py
- avant-worker
- .gam
- session-start.sh
- avant-worker
- _HttpxResponse
- _last
- _HttpxAuthRequest
- _error
- .list_child_publishers

## God Nodes (most connected - your core abstractions)
1. `Services` - 26 edges
2. `RestGamClient` - 14 edges
3. `client()` - 14 edges
4. `Groone Avant: contexto do projeto` - 14 edges
5. `get_services()` - 12 edges
6. `FakeGamClient` - 12 edges
7. `company()` - 12 edges
8. `Arquitetura do MVP do Avant` - 12 edges
9. `fake()` - 11 edges
10. `network()` - 11 edges

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

## Communities (28 total, 13 thin omitted)

### Community 1 - "services.py"
Cohesion: 0.06
Nodes (7): _mailer(), use_services(), Settings, engine(), services(), FakeGamClient, test_deployed_envs_need_redis_and_resend()

### Community 2 - "app.py"
Cohesion: 0.06
Nodes (11): create_app(), _failure(), _logging(), _route(), channel(), publish(), configure_logging(), JsonFormatter (+3 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "gam.py"
Cohesion: 0.12
Nodes (11): Importação, get_services(), check_access(), discover_mcm(), _fan_out(), _flat(), schedule_imports(), schedule_tests() (+3 more)

### Community 5 - "test_gam_tasks.py"
Cohesion: 0.19
Nodes (18): avant-worker, Contexto, issues e skills, Como funciona, Services, company(), count(), fake(), inventory() (+10 more)

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

### Community 13 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 14 - "clean_code.py"
Cohesion: 0.08
Nodes (17): Como trabalhar nos repositórios, Ambientes, deploy e backup, Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11) (+9 more)

### Community 15 - "avant-worker"
Cohesion: 0.29
Nodes (6): avant-worker, Desenvolvimento, Filas e tarefas, Imagem, Processos, Variáveis

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 238 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `test_gam_tasks.py` to `RestGamClient`, `services.py`, `gam.py`, `.gam`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Services` (e.g. with `RestGamClient` and `Settings`) actually correct?**
  _`Services` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `services.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05725490196078432 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `RestGamClient` to `services.py`, `test_gam_tasks.py`, `test_gam_client.py`, `.gam`, `gam_client.py`, `_last`, `_HttpxAuthRequest`, `.list_child_publishers`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `RestGamClient` (e.g. with `Services` and `client()`) actually correct?**
  _`RestGamClient` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06280193236714976 - nodes in this community are weakly interconnected._