# Graph Report - avant-worker  (2026-10-24)

## Corpus Check
- 31 files · ~22,098 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 5, .lock 1)

## Summary
- 379 nodes · 598 edges · 22 communities (16 shown, 6 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1b796086`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- gam_client.py
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
- Avant: repositório e plano do MVP
- avant-worker
- .gam
- session-start.sh
- avant-worker

## God Nodes (most connected - your core abstractions)
1. `Services` - 26 edges
2. `RestGamClient` - 14 edges
3. `client()` - 14 edges
4. `Groone Avant: contexto do projeto` - 14 edges
5. `FakeGamClient` - 12 edges
6. `company()` - 12 edges
7. `Arquitetura do MVP do Avant` - 12 edges
8. `get_services()` - 11 edges
9. `fake()` - 11 edges
10. `network()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Sites e ad units` --references--> `network()`  [INFERRED]
  docs/decisoes/06-endpoints-api.md → tests/test_gam_tasks.py
- `Importação` --references--> `discover_mcm()`  [INFERRED]
  docs/decisoes/04-conexao-gam.md → src/avant_worker/tasks/gam.py
- `test_deployed_envs_need_redis_and_resend()` --uses--> `Settings`  [INFERRED]
  tests/test_tasks.py → src/avant_worker/settings.py
- `test_sync_publishes_network_events()` --calls--> `channel()`  [INFERRED]
  tests/test_gam_tasks.py → src/avant_worker/events.py
- `test_publish_without_redis_is_a_no_op()` --calls--> `publish()`  [INFERRED]
  tests/test_gam_tasks.py → src/avant_worker/events.py

## Import Cycles
- None detected.

## Communities (22 total, 6 thin omitted)

### Community 0 - "gam_client.py"
Cohesion: 0.07
Nodes (7): _delegation(), _error(), _HttpxAuthRequest, _HttpxResponse, _last(), _message(), RestGamClient

### Community 1 - "services.py"
Cohesion: 0.07
Nodes (5): use_services(), engine(), services(), FakeGamClient, test_deployed_envs_need_redis_and_resend()

### Community 2 - "app.py"
Cohesion: 0.08
Nodes (11): create_app(), _failure(), _logging(), _route(), configure_logging(), JsonFormatter, _mailer(), BrokerSettings (+3 more)

### Community 3 - "steps"
Cohesion: 0.06
Nodes (32): AVANT_CORE_ACCESS, AVANT_TEST_DATABASE_URL, AVANT_TEST_MIGRATIONS_URL, AVANT_TEST_REDIS_URL, PGPASSWORD, POSTGRES_PASSWORD, jobs, test (+24 more)

### Community 4 - "gam.py"
Cohesion: 0.11
Nodes (13): Importação, channel(), publish(), get_services(), check_access(), discover_mcm(), _fan_out(), _flat() (+5 more)

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
Nodes (15): Arquitetura, Como trabalhar nos repositórios, Dicas de ambiente para o agente, Documentos de decisão, GAM, Groone Avant: contexto do projeto, Identidade visual, Infraestrutura e operação (+7 more)

### Community 9 - "Avant: endpoints da API do MVP"
Cohesion: 0.12
Nodes (16): API first e chaves de API, Atribuição de sites, Avant: endpoints da API do MVP, Catálogo de permissões, Convenções, Convites, Decisões de Pedro (23/10/2026), Empresa (+8 more)

### Community 10 - "Arquitetura do MVP do Avant"
Cohesion: 0.14
Nodes (13): Ambientes, deploy e backup, Arquitetura do MVP do Avant, Controle de acesso no estilo do Defender, Decisões e perguntas em aberto, Endpoints da API REST, Estrutura do repositório, Fluxos, Isolamento, autenticação e permissões (+5 more)

### Community 11 - "Requisitos do novo SaaS AdTech Groone"
Cohesion: 0.17
Nodes (11): Conta e equipe, Escopo herdado do Genius, Integrações e onboarding no Google Ad Manager, Modelo de cobrança, MVP, Opções de nome, Perguntas em aberto, Problemas a resolver (+3 more)

### Community 12 - "Avant: fluxos de login e convite"
Cohesion: 0.17
Nodes (11): 2FA, Avant: fluxos de login e convite, Com Google, Com senha, Convite e primeiro acesso, Decisões de Pedro (23/10/2026), Endpoints de autenticação, Escolha da Empresa ativa (+3 more)

### Community 13 - "Avant: conexão com o GAM"
Cohesion: 0.22
Nodes (8): Avant: conexão com o GAM, Caminho conta de serviço, Caminho MCM, Decisões de Pedro (23/10/2026), Erros e estados, Fontes, Resumo, Segurança e limites

### Community 14 - "Avant: repositório e plano do MVP"
Cohesion: 0.22
Nodes (8): Avant: repositório e plano do MVP, Decisões de Pedro (23/10/2026), Estrutura de pastas, Pipeline, Plano até 31/12, Primeira semana (23/10 a 02/11), Resumo, Serviços e ferramentas

### Community 15 - "avant-worker"
Cohesion: 0.29
Nodes (6): avant-worker, Desenvolvimento, Filas e tarefas, Imagem, Processos, Variáveis

## Knowledge Gaps
- **1 isolated node(s):** `avant-worker`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 206 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Services` connect `test_gam_tasks.py` to `gam_client.py`, `services.py`, `app.py`, `gam.py`, `.gam`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Services` (e.g. with `RestGamClient` and `Settings`) actually correct?**
  _`Services` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `avant-worker` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `gam_client.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06659619450317125 - nodes in this community are weakly interconnected._
- **Why does `RestGamClient` connect `gam_client.py` to `.gam`, `services.py`, `test_gam_tasks.py`, `test_gam_client.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `RestGamClient` (e.g. with `Services` and `client()`) actually correct?**
  _`RestGamClient` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `services.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07307692307692308 - nodes in this community are weakly interconnected._