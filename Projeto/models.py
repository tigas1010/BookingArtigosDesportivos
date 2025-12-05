from datetime import datetime, timedelta


class Utilizador:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

    def login(self):
        return True


class Cliente(Utilizador):
    def __init__(self, id, nome, email, morada, telefone):
        super().__init__(id, nome, email)
        self.morada = morada
        self.telefone = telefone
        self.reservas = []

    def fazer_reserva(self, reserva):
        self.reservas.append(reserva)

    def consultar_historico(self):
        return self.reservas


class Administrador(Utilizador):
    def __init__(self, id, nome, email, nivel_acesso):
        super().__init__(id, nome, email)
        self.nivel_acesso = nivel_acesso

    def gerir_stock(self, artigo, disponivel):
        artigo.disponivel = disponivel

    def cancelar_reserva(self, reserva):
        reserva.estado = "Cancelada"


class Categoria:
    def __init__(self, id, nome, descricao=""):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.artigos = []

    def adicionar_artigo(self, artigo):
        self.artigos.append(artigo)


class ArtigoDesportivo:
    def __init__(self, id, nome, marca, preco_por_hora, categoria, disponivel=True):
        self.id = id
        self.nome = nome
        self.marca = marca
        self.preco_por_hora = preco_por_hora
        self.disponivel = disponivel
        self.categoria = categoria

    def verificar_disponibilidade(self):
        return self.disponivel


class Reserva:
    def __init__(self, id, cliente, artigos, data_inicio, data_fim):
        self.id = id
        self.cliente = cliente
        self.artigos = artigos
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_total = 0.0
        self.estado = "Pendente"

    def calcular_total(self):
        horas = (self.data_fim - self.data_inicio) / timedelta(hours=1)
        total = 0.0
        for artigo in self.artigos:
            total += artigo.preco_por_hora * horas
        self.valor_total = total
        return total

    def confirmar(self):
        self.estado = "Confirmada"
