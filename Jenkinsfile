// Pipeline do avant-worker no Jenkins: checagens, imagem no GHCR e deploy (develop em staging,
// main em produção). Tudo vem da biblioteca em avant-infra/jenkins (ver o README de lá).
// A main (produção) usa a biblioteca da main do avant-infra; o resto, a da develop.
library(env.BRANCH_NAME == 'main' ? 'avant-main' : 'avant')

avantPipeline(service: 'worker', checks: 'python')
