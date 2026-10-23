---
name: avant-nova-tarefa
description: Use ao criar ou mudar uma tarefa Celery no avant-worker (nome, fila, RLS, idempotência e agenda).
---

# Tarefa nova no avant-worker

A tarefa só monta os adaptadores, chama um caso de uso do avant-core e registra o resultado.

1. **Nome** `avant.<fila>.<nome>`; a fila sai do nome (`task_routes` em `app.py`). Filas: `default`, `mail`, `gam`.
2. **RLS**: tarefa de uma Empresa usa `services.uow(company_id)`. `trusted_uow()` só para limpeza ou para varrer todas as Empresas, sempre com um comentário na tarefa dizendo por quê.
3. **Idempotente**: `acks_late` está ligado e a tarefa pode rodar duas vezes. Grave com upsert ou confira o estado antes.
4. **GAM**: só leitura. `gam_client.py` não ganha método que escreve sem revisão do Pedro. 401/403/404 são falhas permanentes; 429, 5xx e rede voltam para a fila com espera crescente. Uma trava no Redis por network.
5. **Agenda**: em `beat.py`; o scheduler é um só por ambiente.
6. **Eventos** para a tela: publique no canal Redis `avant:events:{company_id}` com `{"type", "data"}`; a API repassa por SSE se o tipo estiver em `events.PERMISSION_FOR` do avant-api.
7. **Testes** com `task_always_eager`, o GAM em memória de `tests/fake_gam.py` e respostas gravadas em `tests/test_gam_client.py`.
8. Atualize a tabela de tarefas do README.
