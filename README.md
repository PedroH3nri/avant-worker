# avant-worker

Worker e agendador (Celery) do Groone Avant. As regras ficam no
[avant-core](https://github.com/PedroH3nri/avant-core), instalado por tag; aqui só há
as tarefas, que montam os adaptadores e chamam os casos de uso.

## Estrutura

Por domínio, como no avant-core:

```
src/avant_worker/
  app.py        Celery: filas, include das tarefas e agenda do beat
  settings.py   variáveis de ambiente
  services.py   monta os adaptadores e o Unit of Work para as tarefas
  logs.py       logs JSON
  adapters/     gam_client (REST), gam_reports (SOAP), page_views (Mongo do data),
                exchange_rates (Open Exchange Rates), events (Redis para o SSE)
  tasks/
    gam/          network_tasks (teste e importação), mcm_tasks (descoberta e contratos)
    metrics/      gam_metrics_tasks, page_view_tasks, mcm_earnings_tasks
    commissions/  commission_tasks (comissão da equipe Groone)
    money/        exchange_rate_tasks
    maintenance/  purge_tasks
```

## Processos

| Processo | Comando | Faz |
| --- | --- | --- |
| worker | `celery -A avant_worker.app worker -Q default,mail -l info` | limpeza e e-mails |
| worker-gam | `celery -A avant_worker.app worker -Q gam -c 2 -l info` | Google Ad Manager; o único com a chave da conta de serviço |
| worker-facebook | `celery -A avant_worker.app worker -Q facebook -c 2 -l info` | Graph API do Facebook (decisão 16); o único com o segredo do app da Meta e a chave dos tokens |
| worker-google-ads | `celery -A avant_worker.app worker -Q google_ads -c 2 -l info` | API do Google Ads (decisão 17); o único com o segredo do cliente OAuth, o developer token e a chave dos tokens |
| scheduler | `celery -A avant_worker.app beat -l info` | publica as tarefas agendadas; um só por ambiente |

O agendador não fala com o banco: só precisa de `CELERY_BROKER_URL`.

## Filas e tarefas

A fila sai do nome da tarefa, `avant.<fila>.<nome>`:

- `default`: limpeza e o resto.
- `mail`: e-mails (os avisos dos alertas, os envios agendados e o esqueci a senha, que a API enfileira só com o e-mail; os outros da API saem direto, depois do commit).
- `gam`: Google Ad Manager, que tem cota própria e não pode travar as outras filas.
- `facebook`: Graph API do Facebook (decisão 16), também com cota própria.
- `google_ads`: API do Google Ads (decisão 17), com a cota do developer token.

| Tarefa | Quando | Faz |
| --- | --- | --- |
| `avant.default.purge_expired` | todo dia às 04:00 UTC | apaga sessões encerradas há mais de 30 dias e links de nova senha vencidos há mais de 7 |
| `avant.gam.discover_mcm` | de hora em hora (minuto 5) | lê os child publishers da network da Groone: liga networks novas à Empresa do dono, guarda o MCM sem dono e desconecta o que foi encerrado |
| `avant.gam.sync_contracts` | de hora em hora (minuto 10) | lê o revshare aprovado de cada child publisher MCM Manage Account e, quando muda, encerra o contrato ativo da network e cria outro |
| `avant.gam.sync_network(company_id, network_id, test=True)` | ao conectar, no "sincronizar agora" e depois da descoberta | teste de acesso, sites e ad units, nessa ordem; depois dos ad units, apaga do Redis o cache das páginas de reward em "mais recentes" dos sites da network e o das ad tags (`avant:tag:{chave}`) |
| `avant.gam.run_tool(run_id)` | quando a API abre uma execução das ferramentas do GAM | roda a configuração completa, o setup de anúncio, os key values ou o "Sincronizar agora" passo a passo (`execute_gam_tool` do core, escritas por SOAP em `adapters/gam_writer.py`, o único arquivo que escreve no GAM); avisa o painel interno com `gam_tool_run.updated`; sem retry automático |
| `avant.gam.schedule_tests` | todo dia às 03:00 UTC | uma `avant.gam.check_access` por network ativa |
| `avant.gam.schedule_imports` | de 6 em 6 horas (minuto 20) | uma `avant.gam.sync_network(test=False)` por network ativa |
| `avant.gam.sync_metrics(company_id, network_id, start, end)` | pelos agendadores abaixo | relatórios por ad unit e por key-value do período (SOAP, só leitura), gravados com upsert em `metrics.*`; avisa o painel com `metrics.updated` |
| `avant.gam.schedule_metrics` | de hora em hora (minuto 35) | ontem e hoje de cada network ativa |
| `avant.gam.schedule_reprocess` | todo dia às 04:40 UTC | os três dias antes de ontem (o GAM ajusta os números) |
| `avant.gam.backfill_metrics(company_id, network_id, days=90)` | depois da primeira importação completa dos ad units da network | o histórico em lotes de 7 dias |
| `avant.default.sync_page_views(company_id, network_id, start, end)` | pelo agendador abaixo | visitas da network no contador do iGroone/data (Mongo, só leitura), gravadas com upsert em `metrics.page_views_hourly`; avisa o painel com `metrics.updated` |
| `avant.default.schedule_page_views` | de hora em hora (minuto 20) | ontem e hoje (datas de São Paulo, como no data) de cada network ativa; sem `PAGE_VIEWS_MONGO_URL`, não agenda nada |
| `avant.default.sync_exchange_rates` | a cada 6 horas (minuto 50) | cotações do Open Exchange Rates: os dias fechados que faltam (100 para trás na primeira vez) e a de agora para hoje; sem `OPENEXCHANGERATES_APP_ID`, não faz nada |
| `avant.default.flush_page_views` | a cada minuto | grava as páginas vistas que a api guardou em `avant:page-views:buffer` (país pelo IP com a GeoLite2; o IP não é gravado) nas visitas por hora, nas key-values e na saúde da tag |
| `avant.default.ensure_page_view_partitions` | todo dia às 02:30 | cria as partições diárias de `metrics.page_view_events` de hoje e dos 7 dias seguintes |
| `avant.gam.schedule_price_rule_hours` | minuto 55 de cada hora | para cada network com site de regra de preço ligada, `avant.gam.sync_price_rule_hours` baixa o relatório por hora da key `content_hash` (ontem e hoje) na moeda da network, sem conversão, e troca as linhas de `metrics.gam_key_value_hourly` |
| `avant.default.run_price_rules` | minuto 58 de cada hora | roda o motor das regras de preço (modelo Automática) e apaga `avant:price-floors:{site}:{hash}` dos hashes que mudaram |
| `avant.default.create_price_rules` | todo dia às 04:00 (São Paulo) | cria as regras novas dos blocos marcados (300+ requisições elegíveis ontem) |
| `avant.default.maintain_price_rule_partitions` | todo dia às 02:35 | cria as partições de `metrics.gam_key_value_hourly` dos próximos dias e apaga as de mais de 30 dias |
| `avant.gam.sync_mcm_earnings` | dias 15 a 20, 03:10 UTC | ganhos e deduções do MCM do mês anterior (`mcmEarnings:fetch` na network da Groone, só leitura), como o `PaymentsGamSync` do Genius; 12 meses para trás na primeira vez. Aceita `month="AAAA-MM"` para regravar um mês |
| `avant.default.calculate_today_commissions` | a cada hora, :45 | comissão de hoje em rascunho, depois de entregar aos responsáveis os prazos sem pessoa |
| `avant.default.calculate_recent_commissions` | 03:00 UTC | todos os dias ainda em aberto até ontem (da data de início, ou do mês seguinte ao último fechado) |
| `avant.default.transfer_clients` | 03:30 UTC | no fim de um prazo de cliente com transferência, passa o cliente para a pessoa do papel com menos clientes |
| `avant.default.close_commissions` | dias 15 a 20, 05:00 UTC | fecha o mês anterior com a dedução do GAM, só depois que o `Mcm_Earnings` do mês chegou; refazer não muda nada; no dia 20, se não fechou, registra erro; aceita `month="AAAA-MM"` |
| `avant.default.schedule_alerts` | de hora em hora (minuto 50) | pede uma `avant.default.check_alerts` por Empresa que tem alerta de métrica |
| `avant.default.check_alerts(company_id)` | pelo agendador acima | confere os alertas da Empresa (último dia fechado, como o dono do alerta) e grava os disparos; pede `avant.mail.notify_alerts` |
| `avant.default.open_checklists` | todo dia às 03:15 | abre o checklist de domínio do mês com os sites que faturaram no mês anterior (no dia 1 cria; depois só pega o que ficou sem conferir) e pede uma `avant.default.check_checklist` por site, a cada 5 s |
| `avant.default.check_checklist(checklist_id)` | pelo agendador acima e pelo "Conferir agora" do painel | busca a página inicial, um artigo e o `ads.txt` do site (GET, sem JavaScript, User-Agent `AvantChecklist/1.0`, 10 s, até 2 MB, 1 pedido por segundo por domínio) e grava o resultado de cada item automático |
| `avant.mail.notify_alerts(company_id)` | depois da conferência | um e-mail por alerta e dia para cada pessoa da lista, só dos disparos ainda sem aviso |
| `avant.default.schedule_reports` | de hora em hora (minuto 2) | pede uma `avant.mail.deliver_reports` por Empresa com envio agendado na hora |
| `avant.mail.deliver_reports(company_id)` | pelo agendador acima | roda o relatório ou o dashboard como cada pessoa da lista e manda o resumo com o CSV anexo; marca o horário antes de mandar, sem repetir |
| `avant.mail.request_password_reset(email)` | pela API, no esqueci a senha | gera o token e manda o e-mail de nova senha se a conta existir (`trusted_uow`); o token nunca vai para a fila nem para o log, e o e-mail sai mascarado no log e nos eventos do Celery; até 4 retries (30 s a 4 min) só em erro temporário (`MailNotSent` ou falha do banco). Cada tentativa grava um link novo antes de enviar: no pior caso, a pessoa tem até 3 links válidos na mesma hora (o limite de pedidos por hora encerra as tentativas) |
| `avant.default.flush_reward_events` | a cada minuto | esvazia `avant:reward:buffer` (eventos e contatos que o `reward.js` manda pela api): renomeia a lista para `avant:reward:processing:{lote}`, grava em pedaços de 5.000 com `record_reward_batch` (idempotente pelo lote) e apaga a chave; uma chave de processamento que sobrou é gravada na execução seguinte |
| `avant.facebook.schedule_structure` | de hora em hora (minuto 25) | uma `avant.facebook.sync_profile` por perfil com token válido (todas as Empresas) |
| `avant.facebook.sync_profile(company_id, profile_id)` | pelo agendador acima | contas do perfil e campanhas, conjuntos e anúncios mudados desde a última vez (`sync_facebook_profile` do core); grava o que mudou fora do Avant no histórico e os avisos de reprovação; token inválido marca o perfil e avisa quem conectou; até 4 retries (1 a 8 min) em `FacebookUnavailable` |
| `avant.facebook.schedule_insights(days=1)` | minutos 15 e 45; às 02:30 UTC com `days=3` | uma `avant.facebook.sync_insights` por conta com perfil válido; os 3 dias porque o Facebook ajusta os números |
| `avant.facebook.sync_insights(company_id, account_id, days)` | pelo agendador acima | números por anúncio e dia e por conjunto, dia e país, gravados com upsert em `metrics.facebook_*`; retries como acima |
| `avant.facebook.check_tokens` | todo dia às 08:00 UTC | avisa quem conectou um perfil cujo token vence em até 7 dias |
| `avant.google_ads.schedule_structure` | de hora em hora (minuto 35) | uma `avant.google_ads.sync_login` por login com token válido (todas as Empresas) |
| `avant.google_ads.sync_login(company_id, login_id)` | pelo agendador acima | contas do login (as novas da MCC também; as que ele deixou de ver ficam sem login) e campanhas, grupos, anúncios e palavras-chave de cada conta ativa (`sync_google_ads_login` do core); avisos de conta suspensa, sufixo trocado e anúncio reprovado; token revogado marca o login e avisa quem conectou; até 4 retries (1 a 8 min) em `GoogleAdsUnavailable` |
| `avant.google_ads.schedule_metrics(days=1, with_terms=False)` | minutos 5 e 35; às 02:40 UTC com `days=3` e `with_terms=True` | uma `avant.google_ads.sync_metrics` por conta ativa com login válido |
| `avant.google_ads.sync_metrics(company_id, account_id, days, with_terms)` | pelo agendador acima | números por campanha (inclui Performance Max), anúncio e palavra-chave e, com `with_terms`, por termo de pesquisa e posicionamento, gravados com upsert em `metrics.google_ads_*`; retries como acima |
| `avant.google_ads.schedule_changes` e `sync_changes(company_id, account_id)` | de hora em hora (minuto 37) | o `change_event` da conta desde a última vez (até 29 dias), no histórico; a primeira rodada só marca o ponto de partida |
| `avant.default.purge_reward_batches` | todo dia às 04:25 UTC | apaga os identificadores de lote de reward com mais de 7 dias |

As métricas das networks do MCM Manage Inventory ficam na network da Groone e ainda não
entram aqui: terão uma tarefa própria, que lê um relatório só e distribui pelas Empresas.

A API enfileira `avant.gam.sync_network` pelo nome (`send_task`), sem importar este pacote.

## Como funciona

- **Entrega**: `task_acks_late` e `prefetch_multiplier=1`. A mensagem só sai da fila
  quando a tarefa termina; se o worker cair, outra instância roda de novo. Toda tarefa
  precisa ser idempotente.
- **RLS**: tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` só para
  limpeza e para varrer todas as Empresas.
- **Conexões**: cada processo filho monta o próprio pool na primeira tarefa.
- **GAM**: API REST do Ad Manager (v1), só leitura (escopo `admanager.readonly`), em
  `adapters/gam_client.py`. 401/403 e 404 são falhas permanentes da network (três seguidas viram
  erro e aviso ao dono); 429, 5xx e falha de rede voltam para a fila em 1, 2, 4 e 8 minutos
  sem mudar o estado. Uma trava no Redis por network impede duas importações ao mesmo tempo.
- **Avisos em tempo real**: depois de cada etapa de uma network, o worker publica
  `{"type": "network.updated", "data": {"network_id"}}` no canal Redis
  `avant:events:{company_id}`; a API repassa por SSE (`GET /api/v1/events`).
- **Logs**: JSON em uma linha, com o stack trace quando uma tarefa falha.
- **Métricas**: o worker publica os eventos do Celery; o `celery-exporter` do
  avant-infra transforma em métricas do Prometheus.

## Variáveis

| Variável | Para quê |
| --- | --- |
| `DATABASE_URL` | papel `avant_app` |
| `CELERY_BROKER_URL` | RabbitMQ |
| `REDIS_URL` | travas, buffers e eventos; obrigatório em todo ambiente (`redis://` ou `rediss://`); vazio, o worker não sobe |
| `MAIL_TRANSPORT` | `resend` ou `smtp`, obrigatório e sem padrão em todo ambiente; sem ele, o worker não sobe |
| `RESEND_API_KEY` | obrigatório com `MAIL_TRANSPORT=resend` |
| `SMTP_URL` | obrigatório com `MAIL_TRANSPORT=smtp`: `smtps://usuario:senha@servidor:porta`, ou `smtp://` só para servidor na mesma rede (o Mailpit do compose) |
| `APP_BASE_URL`, `MAIL_FROM` | endereço dos links e remetente dos e-mails |
| `GAM_SERVICE_ACCOUNT_FILE` | caminho do JSON da chave da conta de serviço; só no worker-gam |
| `GAM_GROONE_NETWORK_CODE` | network da Groone (MCM) |
| `GAM_SOAP_VERSION` | opcional: versão da API SOAP dos relatórios (ex.: `v202608`); vazio usa a mais nova do `googleads` |
| `PAGE_VIEWS_MONGO_URL` | Mongo do iGroone/data, com um usuário só de leitura; sem ela, as visitas não sincronizam |
| `GEOLITE2_COUNTRY_FILE` | caminho da base GeoLite2 Country (`.mmdb`, da MaxMind) montada no container; sem ela, o país das visitas da tag fica `unknown` |
| `PAGE_VIEWS_MONGO_DATABASE` | banco do data no Mongo (padrão `admanager`) |
| `OPENEXCHANGERATES_APP_ID` | chave do Open Exchange Rates (o plano grátis basta); sem ela, as cotações não sincronizam e o painel só mostra dólar |
| `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET` | app da Meta que a Groone já tem; só no worker-facebook (e na API) |
| `FACEBOOK_TOKEN_KEY` | chave Fernet que cifra os tokens dos perfis; a mesma da API |
| `FACEBOOK_GRAPH_VERSION` | opcional: versão da Graph API (padrão `v25.0`) |
| `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_DEVELOPER_TOKEN` | cliente OAuth e developer token do Genius; só no worker-google-ads (e na API) |
| `GOOGLE_ADS_TOKEN_KEY` | chave Fernet que cifra os tokens dos logins do Google; a mesma da API |
| `GOOGLE_ADS_API_VERSION` | opcional: versão da API REST do Google Ads (padrão `v23`) |
| `LOG_LEVEL` | padrão `INFO` |

Os nomes estão no `.env.example` do avant-infra; os valores, só nas VMs.

## Desenvolvimento

Para subir o Avant inteiro na máquina (banco, API, worker e painel), siga o [guia de desenvolvimento](https://github.com/PedroH3nri/avant-infra/blob/develop/docs/desenvolvimento.md) do avant-infra.

```bash
uv sync
uv run ruff format . && uv run ruff check . && uv run mypy
export AVANT_TEST_MIGRATIONS_URL=postgresql+psycopg://avant_owner:SENHA@localhost:5432/avant_test
export AVANT_TEST_DATABASE_URL=postgresql+psycopg://avant_app:SENHA@localhost:5432/avant_test
export AVANT_TEST_REDIS_URL=redis://localhost:6379/15   # opcional: teste da trava
uv run pytest
```

Os testes rodam as tarefas no próprio processo (`task_always_eager`), contra o Postgres,
com um GAM em memória (`tests/fake_gam.py`). O adaptador REST é testado com respostas
gravadas do formato da API (`tests/test_gam_client.py`).
A CI faz o mesmo e usa o secret `AVANT_CORE_ACCESS` (token só de leitura do avant-core).

## Imagem

```bash
docker build --secret id=github_token,env=GITHUB_TOKEN -t ghcr.io/pedroh3nri/avant-worker .
```
