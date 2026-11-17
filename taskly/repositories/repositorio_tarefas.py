from abc import ABC, abstractmethod


class RepositorioTarefas(ABC):
    """Abstração (contrato) para persistência das tarefas."""

    @abstractmethod
    def carregar(self):
        raise NotImplementedError

    @abstractmethod
    def salvar(self, tarefas):
        raise NotImplementedError
