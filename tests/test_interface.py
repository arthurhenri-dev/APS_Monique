import unittest
from unittest.mock import patch

from taskly.interface_terminal import InterfaceTerminal
from taskly.gerenciador_tarefas import GerenciadorTarefas


class RepositorioMemoria:
    def __init__(self):
        self.dados = []

    def carregar(self):
        return list(self.dados)

    def salvar(self, tarefas):
        self.dados = list(tarefas)


class TestInterfaceTerminal(unittest.TestCase):
    def setUp(self):
        self.gerenciador = GerenciadorTarefas(RepositorioMemoria())
        self.interface = InterfaceTerminal(self.gerenciador)

    @patch('taskly.interface_terminal.time.sleep', return_value=None)
    @patch('builtins.print')
    def test_opcao_invalida_nao_interrompe_menu(self, mock_print, _mock_sleep):
        with patch('builtins.input', side_effect=['opcao-invalida', '5']):
            self.interface.executar()
        mensagens = ' '.join(str(chamada) for chamada in mock_print.call_args_list)
        self.assertIn('Opção inválida', mensagens)

    @patch('taskly.interface_terminal.time.sleep', return_value=None)
    @patch('builtins.print')
    def test_adiciona_tarefa_pela_interface(self, _mock_print, _mock_sleep):
        with patch('builtins.input', side_effect=['2', '14/11/2026', 'Estudar', '5']):
            self.interface.executar()
        self.assertEqual(len(self.gerenciador.tarefas), 1)
        self.assertEqual(self.gerenciador.tarefas[0].descricao, 'Estudar')


if __name__ == '__main__':
    unittest.main()
