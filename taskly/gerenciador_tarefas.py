
from taskly.domain.tarefa import Tarefa
from taskly.strategies.estrategia_ordenacao import EstrategiaOrdenacao


class GerenciadorTarefas:
    """Controller GRASP: coordena os casos de uso de tarefas."""

    def __init__(self, repositorio):
        self._repositorio = repositorio
        self._tarefas = repositorio.carregar()

    @property
    def tarefas(self):
        # Retorna uma cópia para impedir alterações externas na lista interna.
        return list(self._tarefas)

    def adicionar_tarefa(self, data, descricao):
        tarefa = Tarefa(data, descricao)
        self._tarefas.append(tarefa)
        self._repositorio.salvar(self._tarefas)
        return tarefa

    def consultar_tarefas(self, estrategia=None):
        if estrategia is None:
            return self.tarefas
        if not isinstance(estrategia, EstrategiaOrdenacao):
            raise TypeError("A estratégia deve implementar EstrategiaOrdenacao.")
        return estrategia.ordenar(self._tarefas)

    def concluir_tarefa(self, indice):
        tarefa = self._obter_por_indice(indice)
        tarefa.concluir()
        self._repositorio.salvar(self._tarefas)
        return tarefa
        
    def excluir_tarefa(self, indice):
        self._obter_por_indice(indice)
        removida = self._tarefas.pop(indice)
        self._repositorio.salvar(self._tarefas)
        return removida
        
    def _obter_por_indice(self, indice):
        if not isinstance(indice, int):
            raise TypeError("O índice da tarefa deve ser um número inteiro.")
        if indice < 0 or indice >= len(self._tarefas):
            raise IndexError("Não existe tarefa nessa posição.")
        return self._tarefas[indice]

    def consultar_pendentes(self):
        return [
            tarefa for tarefa in self.tarefas
            if not tarefa.concluida
        ]
