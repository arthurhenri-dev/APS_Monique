# Validação independente dos testes — 17/11/2026

Esta atualização acrescenta **8 testes** ao arquivo `tests/test_interface.py`, sem modificar o código de produção.

## Resultados reproduzidos

- `python -m pytest -q`: **25 testes aprovados**, sem falhas.
- `python -m coverage run --source=taskly -m pytest -q` e `python -m coverage report -m`: **96% de cobertura de instruções do pacote `taskly`** (235 instruções, 9 não executadas).
- `taskly/interface_terminal.py`: **100% de cobertura de instruções** (97 instruções, nenhuma ausente).

## O que os novos testes verificam

1. Concluir tarefa pelo menu.
2. Excluir tarefa pelo menu.
3. Índice não numérico tratado sem encerrar o sistema.
4. Índice inexistente tratado sem excluir a tarefa.
5. Listagem, conclusão e exclusão sem tarefas cadastradas.
6. Listagem ordenada por descrição.
7. Listagem ordenada por data.
8. Data inválida na inclusão, com preservação da lista.

## Limitações e cuidado acadêmico

A cobertura de 96% considera **apenas o código de produção** em `taskly`, e não os testes. Cobertura de instruções não equivale a cobertura de ramos nem prova ausência de defeitos. Os novos testes foram adicionados a uma implementação já existente; portanto, **não constituem evidência histórica de Red–Green–Refactor/TDD**. Os relatórios antigos no repositório podem apresentar 17 testes e percentuais diferentes; para a entrega, use os comandos acima e o resultado atual, ou atualize todos os documentos de forma coerente.
