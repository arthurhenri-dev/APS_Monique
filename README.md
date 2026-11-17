# **Task.ly — versão refatorada**

Projeto acadêmico de gerenciamento de tarefas em Python, organizado em camadas e com aplicação demonstrativa de três padrões GoF.

## **Requisitos**

- Python 3.10 ou superior.
- Para executar os testes: biblioteca padrão `unittest`.
- Para métricas e cobertura: `pip install -r requirements-dev.txt`.

## **Como executar**

Abra o terminal na pasta `Taskly_refatorado` e execute:

```bash
python main.py
```

As tarefas são armazenadas em `tarefas.json`, na raiz do projeto.

## **Como executar os testes**

```bash
python -m unittest discover -s tests -v
```

## **Como medir cobertura**

```bash
python -m coverage erase
python -m coverage run --source=taskly -m unittest discover -s tests
python -m coverage report -m
```

## **Como analisar complexidade ciclomática**

```bash
radon cc taskly -s -a
radon mi taskly -s
```

## **Como executar análise estática**

```bash
pylint taskly
```

## **Organização**

- `taskly/domain`: entidade de negócio.
- `taskly/repositories`: contrato e persistência JSON.
- `taskly/factories`: Factory Method.
- `taskly/decorators`: Decorator de backup.
- `taskly/strategies`: Strategy de ordenação.
- `taskly/gerenciador_tarefas.py`: coordenação dos casos de uso.
- `taskly/interface_terminal.py`: interface de interação com o usuário.
- `tests`: testes automatizados.

Consulte `docs/relatorio_tecnico.md` para as decisões de projeto e limitações conhecidas.

## **Relatório e diagramas**

- `docs/relatorio_tecnico.md`: memorial técnico da arquitetura, padrões, refatorações e limitações.
- `docs/diagramas/`: diagrama de classes e dois diagramas de sequência (antes/depois), também disponíveis em formato `.dot` para edição.
- `docs/resultado_testes.txt`: resultado reproduzido dos testes automatizados.
- `docs/metricas_execucao.txt`: histórico de cobertura e métricas de qualidade.

A animação de inicialização e a mensagem animada de encerramento do código original foram preservadas na `InterfaceTerminal`, com constantes nomeadas. O relatório Word complementar registra as decisões e limitações conhecidas.

## **Validação de testes atualizada (17/11/2026)**

Na execução local mais recente, foram obtidos os seguintes resultados:

- **36 testes automatizados aprovados**, sem falhas.
- **98% de cobertura** do código de produção (248 instruções analisadas e 6 não cobertas).
- **100% de cobertura** nas classes `Tarefa`, `GerenciadorTarefas` e `InterfaceTerminal`.

Para reproduzir a validação, utilize os comandos apresentados nas seções de testes e cobertura.

Consulte `docs/metricas_execucao.txt` para o histórico das execuções e `docs/validacao_testes_atualizada.md` para informações complementares.