from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Tarefa:
    """Representa uma tarefa do domínio do Task.ly."""

    data: date
    descricao: str
    concluida: bool = False

    def __post_init__(self):
        if isinstance(self.data, str):
            try:
                self.data = datetime.strptime(self.data, "%d/%m/%Y").date()
            except ValueError as erro:
                raise ValueError("A data deve ser válida e estar no formato DD/MM/AAAA.") from erro
        if not isinstance(self.data, date):
            raise TypeError("data deve ser um objeto datetime.date.")
        self.descricao = self.descricao.strip()
        if not self.descricao:
            raise ValueError("A descrição da tarefa não pode ficar vazia.")

    def concluir(self):
        self.concluida = True

    def para_dicionario(self):
        return {
            "Data": self.data.strftime("%d/%m/%Y"),
            "Tarefa": self.descricao,
            "Concluída": self.concluida,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            data=dados["Data"],
            descricao=dados["Tarefa"],
            concluida=dados.get("Concluída", False),
        )

    def __str__(self):
        status = "Concluída" if self.concluida else "Pendente"
        return f"Data: {self.data.strftime('%d/%m/%Y')} | Tarefa: {self.descricao} | Status: {status}"
