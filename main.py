from taskly.decorators.repositorio_backup import RepositorioComBackup
from taskly.factories.fabrica_repositorio import CriadorRepositorioJSON
from taskly.gerenciador_tarefas import GerenciadorTarefas
from taskly.interface_terminal import InterfaceTerminal


def main():
    fabrica = CriadorRepositorioJSON()
    repositorio = RepositorioComBackup(fabrica.criar_repositorio())
    gerenciador = GerenciadorTarefas(repositorio)
    interface = InterfaceTerminal(gerenciador)
    interface.executar()


if __name__ == "__main__":
    main()
