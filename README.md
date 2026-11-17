# Task.ly — versão refatorada

Projeto acadêmico de gerenciamento de tarefas em Python, organizado em camadas e com aplicação demonstrativa de três padrões GoF.

## Requisitos
- Python 3.10 ou superior.
- Para executar os testes: biblioteca padrão `unittest`.
- Para métricas/cobertura: `pip install -r requirements-dev.txt`.

## Como executar
Abra o terminal na pasta `Taskly_refatorado` e execute:

```bash
python main.py
```

As tarefas são armazenadas em `tarefas.json`, na raiz do projeto.

## Como executar os testes

```bash
python -m unittest discover -s tests -v
```

## Como medir cobertura

```bash
coverage run -m unittest discover -s tests
coverage report -m
```

## Como analisar complexidade ciclomática

```bash
radon cc taskly -s -a
radon mi taskly -s
```

## Como executar análise estática

```bash
pylint taskly
```

## Organização
- `taskly/domain`: entidade de negócio.
- `taskly/repositories`: contrato e persistência JSON.
- `taskly/factories`: Factory Method.
- `taskly/decorators`: Decorator de backup.
- `taskly/strategies`: Strategy de ordenação.
- `tests`: testes automatizados.

Consulte `docs/relatorio_tecnico.md` para as decisões de projeto e limitações conhecidas.

## Relatório e diagramas
- `docs/relatorio_tecnico.md`: memorial técnico da arquitetura, padrões, refatorações e limitações.
- `docs/diagramas/`: diagrama de classes e dois diagramas de sequência (antes/depois), também disponíveis em formato `.dot` para edição.
- `docs/resultado_testes.txt`: resultado reproduzido dos testes automatizados.
- `docs/metricas_execucao.txt`: cobertura observada e comandos pendentes para Radon/Pylint.

A animação de inicialização e a mensagem animada de encerramento do código original foram preservadas na InterfaceTerminal, com constantes nomeadas. O relatório Word complementar registra as decisões e limitações conhecidas.
