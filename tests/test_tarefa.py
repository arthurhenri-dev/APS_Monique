import unittest
from datetime import date

from taskly.domain.tarefa import Tarefa


class TestTarefa(unittest.TestCase):
    def test_cria_tarefa_com_data_brasileira(self):
        tarefa = Tarefa("14/11/2026", "Estudar padrões")
        self.assertEqual(tarefa.data, date(2026, 11, 14))
        self.assertFalse(tarefa.concluida)

    def test_rejeita_data_invalida(self):
        with self.assertRaises(ValueError):
            Tarefa("45/19/2026", "Estudar")

    def test_rejeita_descricao_vazia(self):
        with self.assertRaises(ValueError):
            Tarefa("14/11/2026", "   ")

    def test_concluir_altera_status(self):
        tarefa = Tarefa("14/11/2026", "Estudar")
        tarefa.concluir()
        self.assertTrue(tarefa.concluida)


if __name__ == "__main__":
    unittest.main()
