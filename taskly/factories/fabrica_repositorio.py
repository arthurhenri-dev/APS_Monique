from abc import ABC, abstractmethod

from taskly.repositories.repositorio_json import RepositorioJSON


class CriadorRepositorio(ABC):
    """Creator do Factory Method."""

    @abstractmethod
    def criar_repositorio(self):
        raise NotImplementedError


class CriadorRepositorioJSON(CriadorRepositorio):
    """Concrete Creator: fabrica um repositório JSON."""

    def __init__(self, caminho=None):
        self.caminho = caminho

    def criar_repositorio(self):
        return RepositorioJSON(self.caminho)
