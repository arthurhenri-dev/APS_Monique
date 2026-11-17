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
Os testes usam `unittest` e cobrem:
- validação da entidade;
- cadastro, conclusão e exclusão;
- ordenação por data e descrição;
- arquivo inexistente;
- salvamento e recuperação;
- JSON inválido;
- criação pelo Factory Method;
- backup pelo Decorator.

Execute `python -m unittest discover -s tests -v` para reproduzir a execução.

## 7. TDD — funcionalidade de ordenação
Os testes de ordenação estão em `tests/test_gerenciador.py`. Para apresentar evidência de TDD na entrega, a equipe deve reproduzir e registrar a sequência abaixo no ambiente de desenvolvimento:
1. Antes de criar `OrdenarPorData` e `OrdenarPorDescricao`, escrever os testes que definem a ordem esperada.
2. Executar os testes nesse estado inicial e registrar a falha esperada (Red).
3. Implementar a interface `EstrategiaOrdenacao` e as estratégias concretas (Green).
4. Executar novamente os testes e registrar a aprovação.
5. Se necessário, reorganizar o código sem alterar o comportamento (Refactor).

**Importante:** o pacote entregue contém os testes e a implementação final, mas não contém capturas de tela de uma execução histórica em estado Red. A equipe deve produzir essas capturas ao reproduzir a sequência, sem apresentar uma falha simulada como se fosse registro anterior.

## 8. Métricas
As métricas devem ser coletadas no ambiente da equipe após a instalação das ferramentas:
- Complexidade ciclomática: `radon cc taskly -s -a`
- Índice de manutenibilidade: `radon mi taskly -s`
- Análise estática: `pylint taskly`
- Cobertura: `coverage run -m unittest discover -s tests` e `coverage report -m`

Não foram inseridos valores numéricos estimados neste relatório. Registrem a saída real dessas ferramentas e, se possível, comparem com a versão anterior.

## 9. Decisões e limitações
- A aplicação é de terminal e utiliza arquivo JSON; não foi introduzido banco de dados. A animação de carregamento e a mensagem animada de encerramento do programa original foram preservadas na InterfaceTerminal, usando constantes nomeadas para controlar quantidade de etapas e intervalo.
- O Decorator cria um único arquivo de backup (`tarefas.backup.json`), atualizado a cada salvamento posterior ao primeiro. Para histórico de versões, seria necessário evoluir a estratégia de backup.
- Um JSON corrompido gera erro explícito em vez de retornar silenciosamente uma lista vazia. Isso evita que um salvamento posterior apague dados que não puderam ser lidos.
- A ordenação é aplicada à consulta e não altera a ordem original armazenada.
- A data continua sendo exibida no formato brasileiro `DD/MM/AAAA`.
