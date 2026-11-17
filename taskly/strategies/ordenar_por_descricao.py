from taskly.strategies.estrategia_ordenacao import EstrategiaOrdenacao


class OrdenarPorDescricao(EstrategiaOrdenacao):
    def ordenar(self, tarefas):
        return sorted(tarefas, key=lambda tarefa: tarefa.descricao.casefold())
