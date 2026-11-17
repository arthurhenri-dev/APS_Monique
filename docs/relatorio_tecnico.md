
# Relatório técnico — Task.ly

## 1. Escopo
A versão mantém as operações centrais da aplicação: cadastrar, consultar, concluir e excluir tarefas, além de persistir os dados localmente em JSON. Foi acrescentada a opção de ordenar a consulta por data ou descrição.

## 2. Arquitetura
Foi adotada uma organização em camadas simples:
- **Domínio:** `Tarefa`, responsável pelos dados e regras básicas de validade.
- **Aplicação:** `GerenciadorTarefas`, que coordena os casos de uso.
- **Persistência:** `RepositorioTarefas` (abstração) e `RepositorioJSON` (implementação).
- **Apresentação:** `InterfaceTerminal`, responsável por entrada e saída no terminal.
- **Composição:** `main.py`, que instancia e conecta os componentes.

## 3. Padrões GoF
| Categoria | Padrão | Implementação | Justificativa |
|---|---|---|---|
| Criacional | Factory Method | `CriadorRepositorio` e `CriadorRepositorioJSON` | Centraliza a criação do repositório e permite criar outros tipos de fábrica/armazenamento. |
| Estrutural | Decorator | `RepositorioComBackup` | Acrescenta backup antes de salvar sem alterar `RepositorioJSON`. |
| Comportamental | Strategy | `EstrategiaOrdenacao`, `OrdenarPorData`, `OrdenarPorDescricao` | Permite trocar o algoritmo de ordenação sem alterar o gerenciador. |

## 4. SOLID e GRASP
- **SRP:** `Tarefa`, `GerenciadorTarefas`, `InterfaceTerminal` e `RepositorioJSON` têm responsabilidades distintas.
- **OCP:** novas estratégias de ordenação podem ser adicionadas por extensão, sem modificar as estratégias existentes.
- **DIP:** `GerenciadorTarefas` recebe um repositório por construtor e trabalha com o contrato `RepositorioTarefas`, não cria o repositório concreto.
- **GRASP — Controller:** `GerenciadorTarefas` coordena operações de aplicação solicitadas pela interface.
- **GRASP — Information Expert:** `Tarefa` controla seu próprio estado de conclusão; o gerenciador conhece a coleção e coordena sua manutenção.
- **Alta coesão e baixo acoplamento:** responsabilidades de interface, domínio e persistência estão separadas e conectadas por dependências explícitas.

## 5. Refatorações realizadas
| Code Smell observado na versão anterior | Alteração realizada | Técnica/conceito |
|---|---|---|
| Classe `TaskLy` concentrava muitas responsabilidades | Separação em domínio, gerenciador, interface e repositório | Extract Class / Move Method |
| Gerenciamento dependia diretamente das funções JSON | Introdução de `RepositorioTarefas` | Dependência de abstração |
| Interface e regras de negócio misturadas | Entrada/saída movida para `InterfaceTerminal` | Separate Presentation |
| Verificação/conversão de dados sem validação adequada | Validação de data, descrição e índice | Guard Clauses / validação |
| Data representada somente como texto | Conversão para `datetime.date` no domínio | Encapsulamento de tipo |
| Caminho relativo dependia do diretório atual | Caminho padrão calculado a partir do projeto | Robustez de persistência |
| Salvamento poderia deixar arquivo incompleto em interrupção | Escrita temporária seguida de substituição | Escrita atômica |

## 6. Testes

Os testes automatizados foram desenvolvidos com `unittest` e executados pelo GitHub Actions. Eles verificam operações de cadastro, consulta, conclusão e exclusão de tarefas, validações, ordenação, persistência em JSON e funcionalidades relacionadas aos padrões de projeto.

Na execução bem-sucedida analisada, o projeto alcançou **96% de cobertura**, com 237 instruções analisadas e 9 não cobertas.

A execução dos testes pode ser reproduzida com:

`python -m unittest discover -s tests -v`

## 7. TDD — Consulta de tarefas pendentes

Para demonstrar o ciclo de desenvolvimento orientado a testes (TDD), foi utilizada a funcionalidade de consulta de tarefas pendentes.

O histórico da branch `evidencia-tdd` registra três etapas:

- **RED — commit `9a3acef`:** criação do teste para consultar somente tarefas pendentes.
- **GREEN — commit `7824189`:** implementação do método `consultar_pendentes()` no gerenciador.
- **REFACTOR — commit `5c60e19`:** simplificação da implementação, mantendo o comportamento esperado.

Após as alterações, a execução do GitHub Actions foi concluída com sucesso.

A etapa RED foi registrada na execução #9 do GitHub Actions, quando o teste falhou porque o método `consultar_pendentes()` ainda não existia. Na execução #10, após a implementação, o teste passou. Na execução #11, após a refatoração, o fluxo de qualidade continuou aprovado. Esses registros, juntamente com o histórico de commits, documentam o ciclo TDD realizado na branch `evidencia-tdd`.

## 8. Métricas e análise estática

A análise de qualidade foi realizada por meio do GitHub Actions, utilizando Coverage, Radon e Pylint.

Os resultados registrados foram:

- **Cobertura de testes:** 96%.
- **Complexidade ciclomática média:** 2,21, classificação A pelo Radon.
- **Pylint:** 8,46/10.

A organização em camadas favorece a coesão, pois cada componente concentra responsabilidades relacionadas à sua finalidade. O acoplamento é reduzido pela separação entre o gerenciador de tarefas e a implementação concreta de persistência, por meio da abstração `RepositorioTarefas`.

Essas observações sobre coesão e acoplamento são qualitativas; não foram apresentados indicadores quantitativos específicos para essas duas características.

Os comandos utilizados para a análise são:

- `radon cc taskly -s -a`
- `radon mi taskly -s`
- `pylint taskly`
- `coverage run --source=taskly -m unittest discover -s tests -v`
- `coverage report -m`
  
## 9. Decisões e limitações
- A aplicação é de terminal e utiliza arquivo JSON; não foi introduzido banco de dados. A animação de carregamento e a mensagem animada de encerramento do programa original foram preservadas na InterfaceTerminal, usando constantes nomeadas para controlar quantidade de etapas e intervalo.
- O Decorator cria um único arquivo de backup (`tarefas.backup.json`), atualizado a cada salvamento posterior ao primeiro. Para histórico de versões, seria necessário evoluir a estratégia de backup.
- Um JSON corrompido gera erro explícito em vez de retornar silenciosamente uma lista vazia. Isso evita que um salvamento posterior apague dados que não puderam ser lidos.
- A ordenação é aplicada à consulta e não altera a ordem original armazenada.
- A data continua sendo exibida no formato brasileiro `DD/MM/AAAA`.


