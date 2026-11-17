import unittest
from datetime import date

from taskly.gerenciador_tarefas import GerenciadorTarefas
from taskly.domain.tarefa import Tarefa
from taskly.strategies.ordenar_por_data import OrdenarPorData
from taskly.strategies.ordenar_por_descricao import OrdenarPorDescricao


class RepositorioMemoria:
    def __init__(self, tarefas=None):
        self.dados = list(tarefas or [])
        self.salvamentos = 0

    def carregar(self):
        return list(self.dados)

    def salvar(self, tarefas):
        self.dados = list(tarefas)
        self.salvamentos += 1


class TestGerenciador(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioMemoria()
        self.gerenciador = GerenciadorTarefas(self.repo)

    def test_adiciona_tarefa_e_persiste(self):
        tarefa = self.gerenciador.adicionar_tarefa("14/11/2026", "Estudar")
        self.assertEqual(len(self.gerenciador.tarefas), 1)
        self.assertEqual(self.repo.salvamentos, 1)
        self.assertEqual(tarefa.descricao, "Estudar")

    def test_conclui_tarefa(self):
        self.gerenciador.adicionar_tarefa("14/11/2026", "Estudar")
        tarefa = self.gerenciador.concluir_tarefa(0)
        self.assertTrue(tarefa.concluida)

    def test_exclui_tarefa(self):
        self.gerenciador.adicionar_tarefa("14/11/2026", "Estudar")
        removida = self.gerenciador.excluir_tarefa(0)
        self.assertEqual(removida.descricao, "Estudar")
        self.assertEqual(self.gerenciador.tarefas, [])

    def test_indice_inexistente(self):
        with self.assertRaises(IndexError):
            self.gerenciador.concluir_tarefa(0)

    def test_ordena_por_data(self):
        self.gerenciador.adicionar_tarefa("20/11/2026", "Depois")
        self.gerenciador.adicionar_tarefa("10/11/2026", "Antes")
        ordenadas = self.gerenciador.consultar_tarefas(OrdenarPorData())
        self.assertEqual([t.descricao for t in ordenadas], ["Antes", "Depois"])

    def test_ordena_por_descricao(self):
        self.gerenciador.adicionar_tarefa("20/11/2026", "Zebra")
        self.gerenciador.adicionar_tarefa("10/11/2026", "Abacaxi")
        ordenadas = self.gerenciador.consultar_tarefas(OrdenarPorDescricao())
        self.assertEqual([t.descricao for t in ordenadas], ["Abacaxi", "Zebra"])

    def test_rejeita_estrategia_invalida(self):
        with self.assertRaises(TypeError):
            self.gerenciador.consultar_tarefas("data")

    def test_consulta_somente_tarefas_pendentes(self):
        self.gerenciador.adicionar_tarefa("20/11/2026", "Estudar")
        self.gerenciador.adicionar_tarefa("21/11/2026", "Apresentar trabalho")

        self.gerenciador.concluir_tarefa(0)

        pendentes = self.gerenciador.consultar_pendentes()

        self.assertEqual(len(pendentes), 1)
        self.assertEqual(pendentes[0].descricao, "Apresentar trabalho")

    def test_rejeita_indice_booleano_true(self):
        with self.assertRaises(TypeError):
            self.gerenciador._obter_por_indice(True)

    def test_rejeita_indice_booleano_false(self):
        with self.assertRaises(TypeError):
            self.gerenciador._obter_por_indice(False)


if __name__ == "__main__":
    unittest.main()
