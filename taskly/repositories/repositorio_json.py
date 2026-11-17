import json
from pathlib import Path

from taskly.domain.tarefa import Tarefa
from taskly.repositories.repositorio_tarefas import RepositorioTarefas


class RepositorioJSON(RepositorioTarefas):
    """Persistência local em JSON. Não depende do diretório de execução."""

    def __init__(self, caminho=None):
        raiz_projeto = Path(__file__).resolve().parents[2]
        self.caminho = Path(caminho) if caminho else raiz_projeto / "tarefas.json"

    def carregar(self):
        if not self.caminho.exists():
            return []
        try:
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except json.JSONDecodeError as erro:
            # Não esconder corrupção: evita carregar lista vazia e sobrescrever dados sem querer.
            raise ValueError(f"O arquivo {self.caminho} contém JSON inválido.") from erro

        if not isinstance(dados, list):
            raise ValueError("O conteúdo do arquivo de tarefas deve ser uma lista.")
        return [Tarefa.de_dicionario(item) for item in dados]

    def salvar(self, tarefas):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        dados = [tarefa.para_dicionario() for tarefa in tarefas]
        temporario = self.caminho.with_suffix(self.caminho.suffix + ".tmp")
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        temporario.replace(self.caminho)
