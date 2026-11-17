from abc import ABC, abstractmethod


class EstrategiaOrdenacao(ABC):
    """Interface comum para estratégias de ordenação."""

    @abstractmethod
    def ordenar(self, tarefas):
        raise NotImplementedError
