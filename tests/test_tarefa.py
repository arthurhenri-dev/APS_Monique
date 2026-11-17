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


    def test_rejeita_registro_que_nao_e_dicionario(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario(["14/11/2026", "Estudar"])

    def test_rejeita_ausencia_do_campo_data(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario({"Tarefa": "Estudar"})

    def test_rejeita_ausencia_do_campo_tarefa(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario({"Data": "14/11/2026"})

    def test_rejeita_data_que_nao_e_string(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario({
                "Data": 14112026,
                "Tarefa": "Estudar"
            })

    def test_rejeita_descricao_que_nao_e_string(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario({
                "Data": "14/11/2026",
                "Tarefa": 123
            })

    def test_rejeita_status_que_nao_e_booleano(self):
        with self.assertRaises(ValueError):
            Tarefa.de_dicionario({
                "Data": "14/11/2026",
                "Tarefa": "Estudar",
                "Concluída": "sim"
            })


if __name__ == "__main__":
    unittest.main()
