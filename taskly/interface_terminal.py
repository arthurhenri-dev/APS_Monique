
import sys
import time

from taskly.strategies.ordenar_por_data import OrdenarPorData
from taskly.strategies.ordenar_por_descricao import OrdenarPorDescricao


ANIMATION_STEPS = 30
ANIMATION_DELAY_SECONDS = 0.1


class InterfaceTerminal:
    """Responsável somente pela interação com o usuário."""

    def __init__(self, gerenciador):
        self._gerenciador = gerenciador

    def executar(self):
        self._mostrar_carregamento()
        print("\n=== Task.ly ===")
        while True:
            self._mostrar_menu()
            escolha = input("Selecione uma opção: ").strip()
            try:
                if escolha == "1":
                    self._listar_tarefas()
                elif escolha == "2":
                    self._adicionar_tarefa()
                elif escolha == "3":
                    self._concluir_tarefa()
                elif escolha == "4":
                    self._excluir_tarefa()
                elif escolha == "5":
                    self._mostrar_encerramento()
                    break
                else:
                    print("Opção inválida. Escolha de 1 a 5.")
            except (ValueError, IndexError, TypeError) as erro:
                print(f"Não foi possível realizar a operação: {erro}")


    @staticmethod
    def _mostrar_carregamento():
        for etapa in range(ANIMATION_STEPS + 1):
            porcentagem = int((etapa / ANIMATION_STEPS) * 100)
            barra = "█" * etapa + "░" * (ANIMATION_STEPS - etapa)
            sys.stdout.write(f"\rIniciando o Task.Ly... [{barra}] {porcentagem}% ")
            sys.stdout.flush()
            time.sleep(ANIMATION_DELAY_SECONDS)
        print("\nSistema pronto. Bem-vindo!\n")

    @staticmethod
    def _mostrar_encerramento():
        mensagem = "Programa encerrado com sucesso, até mais"
        for caractere in mensagem:
            print(caractere, end="", flush=True)
            time.sleep(ANIMATION_DELAY_SECONDS)
        print()

    @staticmethod
    def _mostrar_menu():
        print("\n1 - Ver tarefas")
        print("2 - Adicionar tarefa")
        print("3 - Concluir tarefa")
        print("4 - Excluir tarefa")
        print("5 - Sair")

    def _listar_tarefas(self):
        tarefas = self._gerenciador.consultar_tarefas()
        if not tarefas:
            print("Você ainda não possui tarefas.")
            return
        print("\nOrdenar: 1 - Data | 2 - Descrição | Enter - Sem ordenação")
        escolha = input("Opção: ").strip()
        estrategia = None
        if escolha == "1":
            estrategia = OrdenarPorData()
        elif escolha == "2":
            estrategia = OrdenarPorDescricao()
        tarefas = self._gerenciador.consultar_tarefas(estrategia)
        for indice, tarefa in enumerate(tarefas, start=1):
            print(f"{indice} - {tarefa}")

    def _adicionar_tarefa(self):
        data = input("Digite a data (DD/MM/AAAA): ").strip()
        descricao = input("Digite sua tarefa: ")
        self._gerenciador.adicionar_tarefa(data, descricao)
        print("Tarefa adicionada com sucesso!")

    def _solicitar_indice(self):
        tarefas = self._gerenciador.consultar_tarefas()
        if not tarefas:
            print("Você ainda não possui tarefas.")
            return None
        for indice, tarefa in enumerate(tarefas, start=1):
            print(f"{indice} - {tarefa}")
        try:
            indice = int(input("Número da tarefa: ")) - 1
        except ValueError as erro:
            raise ValueError("Digite um número inteiro válido.") from erro
        if indice < 0 or indice >= len(tarefas):
            raise IndexError("Número de tarefa inexistente.")
        return indice

    def _concluir_tarefa(self):
        indice = self._solicitar_indice()
        if indice is not None:
            self._gerenciador.concluir_tarefa(indice)
            print("Tarefa concluída!")

    def _excluir_tarefa(self):
        indice = self._solicitar_indice()
        if indice is not None:
            self._gerenciador.excluir_tarefa(indice)
            print("Tarefa removida!")
