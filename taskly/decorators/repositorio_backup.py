import shutil
from pathlib import Path

from taskly.repositories.repositorio_tarefas import RepositorioTarefas


class RepositorioComBackup(RepositorioTarefas):
    """Decorator: cria uma cópia do arquivo atual antes de salvar alterações."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def carregar(self):
        return self._repositorio.carregar()

    def salvar(self, tarefas):
        caminho = getattr(self._repositorio, "caminho", None)
        if caminho is not None:
            caminho = Path(caminho)
            if caminho.exists():
                backup = caminho.with_name(caminho.stem + ".backup" + caminho.suffix)
                shutil.copy2(caminho, backup)
        self._repositorio.salvar(tarefas)
