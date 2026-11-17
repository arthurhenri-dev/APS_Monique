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

class TestFluxosAdicionaisInterface(unittest.TestCase):
    def setUp(self):
        self.gerenciador = GerenciadorTarefas(RepositorioMemoria())
        self.interface = InterfaceTerminal(self.gerenciador)

    def _executar(self, entradas):
        with patch('taskly.interface_terminal.time.sleep', return_value=None), \
             patch('builtins.input', side_effect=entradas), \
             patch('builtins.print') as imprimir, \
             patch('taskly.interface_terminal.sys.stdout.write'), \
             patch('taskly.interface_terminal.sys.stdout.flush'):
            self.interface.executar()
        return ' '.join(str(c) for c in imprimir.call_args_list)

    def test_concluir_tarefa_pelo_menu(self):
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Estudar')
        saida = self._executar(['3', '1', '5'])
        self.assertTrue(self.gerenciador.tarefas[0].concluida)
        self.assertIn('Tarefa concluída!', saida)

    def test_excluir_tarefa_pelo_menu(self):
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Estudar')
        saida = self._executar(['4', '1', '5'])
        self.assertEqual(self.gerenciador.tarefas, [])
        self.assertIn('Tarefa removida!', saida)

    def test_indice_nao_numerico_e_tratado(self):
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Estudar')
        saida = self._executar(['3', 'abc', '5'])
        self.assertFalse(self.gerenciador.tarefas[0].concluida)
        self.assertIn('Digite um número inteiro válido', saida)

    def test_indice_inexistente_e_tratado(self):
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Estudar')
        saida = self._executar(['4', '99', '5'])
        self.assertEqual(len(self.gerenciador.tarefas), 1)
        self.assertIn('Número de tarefa inexistente', saida)

    def test_lista_vazia_e_operacoes_sem_tarefas(self):
        saida = self._executar(['1', '3', '4', '5'])
        self.assertIn('Você ainda não possui tarefas', saida)

    def test_listagem_com_ordenacao_por_descricao(self):
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Zebra')
        self.gerenciador.adicionar_tarefa('15/11/2026', 'Abelha')
        saida = self._executar(['1', '2', '5'])
        self.assertIn('1 -', saida)
        self.assertLess(saida.find('Abelha'), saida.find('Zebra'))

    def test_listagem_com_ordenacao_por_data(self):
        self.gerenciador.adicionar_tarefa('15/11/2026', 'Depois')
        self.gerenciador.adicionar_tarefa('14/11/2026', 'Antes')
        saida = self._executar(['1', '1', '5'])
        self.assertLess(saida.find('Antes'), saida.find('Depois'))

    def test_data_invalida_na_adicao_nao_encerra_menu(self):
        saida = self._executar(['2', '31/02/2026', 'Invalida', '5'])
        self.assertEqual(len(self.gerenciador.tarefas), 0)
        self.assertIn('Não foi possível realizar a operação', saida)
