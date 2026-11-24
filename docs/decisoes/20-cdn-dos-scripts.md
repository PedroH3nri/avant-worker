# 20. CDN dos scripts do site (cdn.groone.com)

Situação: **requisito do deploy de produção** (Pedro, 23/11/2026). Milestone M2 Segurança e
produção. Issues: avant-infra#168 (CDN no ar), avant-tag#47 (scripts modulares) e avant-web#400 (linhas de
instalação). Complementa a decisão 13 (ad tag) e a 12 (rewards).

Hoje o site do cliente carrega os scripts do próprio painel: `https://avant.groone.com/tag.js` e
`/reward.js`, servidos pelo nginx do avant-web. Pedro decidiu (23/11) que os scripts saem de um
CDN próprio, sem "avant" no endereço.

## O que ficou decidido

- **Endereço:** `cdn.groone.com`, sem o nome do Avant no DNS. Todos os scripts que rodam no site
  do cliente ficam lá: ad tag, loader, visitas (page views), reward e os que vierem depois.
- **Cache pela Cloudflare:** o registro `cdn` fica com o proxy da Cloudflare ligado; a origem é a
  VM principal. Os scripts ficam guardados na borda da Cloudflare, e o servidor do Avant quase não
  recebe esses pedidos.
- **Scripts modulares** (Pedro, 23/11): o cliente escolhe o que instala.
  - `tag.js`: a ad tag completa, tudo num script só (loader, visitas, anúncios, regras de preço,
    Analytics, MGID e reward), como hoje.
  - Scripts soltos, cada um com só o seu módulo: `page-views.js` (visitas), `loader.js` (tela de
    carregamento e adblock) e `reward.js` (reward e quiz). Dá para usar, por exemplo, só
    `page-views.js` e `loader.js`, sem os anúncios.
  - Os módulos saem do mesmo código do `avant-tag` (cada pasta de `src/` já é um módulo). Cada
    script solto leva junto o `core` de que precisa, para funcionar sozinho.
  - Sem duplicar: se a página tem o `tag.js`, os soltos que ele já cobre desistem (como o
    `reward.js` faz hoje). Dois soltos diferentes rodam juntos.
- **Instalação:** `<script async src="https://cdn.groone.com/tag.js" data-tag="{chave}"></script>`.
  Os soltos que precisam saber de qual site são (visitas e loader) usam a mesma chave da tag em
  `data-tag`; o `reward.js` continua sem chave. O painel mostra as linhas com o `cdn.groone.com`.

## Como fica no ar (proposta para o avant-infra)

- DNS `cdn.groone.com` na Cloudflare com proxy, HTTPS na borda e na origem (certificado de
  origem da Cloudflare ou Let's Encrypt no nginx).
- Origem: um `server` do nginx para `cdn.groone.com` que serve só os arquivos do build do
  `avant-tag` (pasta própria, sem o painel e sem a API), com
  `Access-Control-Allow-Origin: *` e `Content-Type: application/javascript`.
- Cache: endereço fixo (`/tag.js`) com cache curto no navegador e mais longo na borda, e o deploy
  limpa o cache da Cloudflare desses arquivos (token da API da Cloudflare só no Jenkins/VM, nunca
  no repositório). Endereços com versão (`/v/{versão}/tag.js`) podem ficar em cache por um ano.
- Staging: `cdn-staging.groone.com` (ou equivalente), para testar antes de produção.
- Compatibilidade: `avant.groone.com/tag.js` e `/reward.js` continuam respondendo (redirecionando
  para o CDN) enquanto houver site com a linha antiga.

## Em aberto

- **Onde os scripts chamam a API.** Hoje o `tag.js` monta o endereço da API a partir do endereço
  do próprio script. Saindo do CDN, ele precisa saber o endereço da API. Proposta: as chamadas
  também passam pelo `cdn.groone.com` (sem cache para visitas e eventos; configuração da tag com
  cache curto na borda), para a página do cliente não citar o Avant em lugar nenhum. A outra
  opção é o script chamar `avant.groone.com/api/tag/*` direto. Pedro decide.
- Nome do script de visitas: `page-views.js` (proposto) ou `page-views-v2.js`, como no Data.
