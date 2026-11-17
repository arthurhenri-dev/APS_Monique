import json
import tempfile
import unittest
from pathlib import Path

from taskly.domain.tarefa import Tarefa
from taskly.repositories.repositorio_json import RepositorioJSON
from taskly.decorators.repositorio_backup import RepositorioComBackup
from taskly.factories.fabrica_repositorio import CriadorRepositorioJSON


class TestRepositorioJSON(unittest.TestCase):
    def test_arquivo_inexistente_retorna_lista_vazia(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = RepositorioJSON(Path(pasta) / "tarefas.json")
            self.assertEqual(repo.carregar(), [])

    def test_salva_e_carrega_tarefas(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = RepositorioJSON(Path(pasta) / "tarefas.json")
            original = [Tarefa("14/11/2026", "Estudar")]
            repo.salvar(original)
            recuperadas = repo.carregar()
            self.assertEqual(recuperadas[0].descricao, "Estudar")
            self.assertEqual(recuperadas[0].data, original[0].data)

    def test_json_corrompido_gera_erro_claro(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            caminho.write_text("{invalido", encoding="utf-8")
            with self.assertRaises(ValueError):
                RepositorioJSON(caminho).carregar()

    def test_factory_method_cria_repositorio_json(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = CriadorRepositorioJSON(Path(pasta) / "tarefas.json").criar_repositorio()
            self.assertIsInstance(repo, RepositorioJSON)

    def test_decorator_cria_backup_antes_de_salvar(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            repo = RepositorioComBackup(RepositorioJSON(caminho))
            repo.salvar([Tarefa("14/11/2026", "Primeira")])
            repo.salvar([Tarefa("15/11/2026", "Segunda")])
            backup = Path(pasta) / "tarefas.backup.json"
            self.assertTrue(backup.exists())
            dados_backup = json.loads(backup.read_text(encoding="utf-8"))
            self.assertEqual(dados_backup[0]["Tarefa"], "Primeira")


if __name__ == "__main__":
    unittest.main()
