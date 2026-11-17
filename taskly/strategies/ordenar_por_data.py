from taskly.strategies.estrategia_ordenacao import EstrategiaOrdenacao


class OrdenarPorData(EstrategiaOrdenacao):
    def ordenar(self, tarefas):
        return sorted(tarefas, key=lambda tarefa: tarefa.data)
