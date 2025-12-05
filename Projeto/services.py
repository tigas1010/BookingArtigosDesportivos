from datetime import datetime
from models import (
    Cliente,
    Administrador,
    Categoria,
    ArtigoDesportivo,
    Reserva,
)


class SistemaReservas:
    """
    Classe de alto nível que gere utilizadores, artigos, categorias e reservas.
    Esta classe será usada pela GUI (Tkinter) como ponto de entrada para a lógica de negócio.
    """

    def __init__(self):
        self.clientes = {}  # key: email, value: Cliente
        self.administradores = {}  # key: email, value: Administrador
        self.categorias = {}  # key: id,    value: Categoria
        self.artigos = {}  # key: id,    value: ArtigoDesportivo
        self.reservas = {}  # key: id,    value: Reserva

        self._proximo_id_reserva = 1

        # Criar dados de exemplo (como no diagrama de objetos)
        self._criar_dados_exemplo()

    # Dados de exemplo
    def _criar_dados_exemplo(self):
        """Cria alguns utilizadores, categorias e artigos para testes iniciais."""

        # Categoria
        cat_tenis = Categoria(
            1, "Desportos de Raquete", "Artigos para ténis e modalidades semelhantes"
        )
        self.categorias[cat_tenis.id] = cat_tenis

        # Artigos
        a1 = ArtigoDesportivo(
            id=1,
            nome="Raquete Pro Staff",
            marca="Wilson",
            preco_por_hora=5.0,
            categoria=cat_tenis,
            disponivel=True,
        )
        a2 = ArtigoDesportivo(
            id=2,
            nome="Pack 3 Bolas",
            marca="Dunlop",
            preco_por_hora=2.5,
            categoria=cat_tenis,
            disponivel=True,
        )

        self.artigos[a1.id] = a1
        self.artigos[a2.id] = a2
        cat_tenis.adicionar_artigo(a1)
        cat_tenis.adicionar_artigo(a2)

        # Cliente (c1_Joao)
        c1 = Cliente(
            id=1,
            nome="João Silva",
            email="joao@email.com",
            morada="Rua Exemplo 123",
            telefone="912345678",
        )
        self.clientes[c1.email] = c1

        # Administrador
        admin = Administrador(
            id=100,
            nome="admin",
            email="admin@email.com",
            nivel_acesso=1,
        )
        self.administradores[admin.email] = admin

    # Autenticação simples
    def login_cliente(self, email: str) -> Cliente | None:
        """Devolve o Cliente com o email indicado ou None se não existir."""
        return self.clientes.get(email)

    def login_admin(self, email: str) -> Administrador | None:
        """Devolve o Administrador com o email indicado ou None se não existir."""
        return self.administradores.get(email)

    # Artigos / stock
    def listar_categorias(self):
        return list(self.categorias.values())

    def listar_artigos(self, apenas_disponiveis: bool = False):
        artigos = list(self.artigos.values())
        if apenas_disponiveis:
            artigos = [a for a in artigos if a.disponivel]
        return artigos

    def listar_artigos_por_categoria(
        self, categoria_id: int, apenas_disponiveis: bool = False
    ):
        artigos = [a for a in self.artigos.values() if a.categoria.id == categoria_id]
        if apenas_disponiveis:
            artigos = [a for a in artigos if a.disponivel]
        return artigos

    def gerir_stock(self, artigo_id: int, disponivel: bool) -> bool:
        artigo = self.artigos.get(artigo_id)
        if artigo is None:
            return False
        artigo.disponivel = disponivel
        return True

    # Reservas
    def criar_reserva(
        self,
        cliente: Cliente,
        ids_artigos: list[int],
        data_inicio: datetime,
        data_fim: datetime,
    ) -> Reserva | None:
        """
        Cria uma reserva para o cliente, com os artigos e datas indicados.
        Calcula o total e marca a reserva como 'Confirmada'.
        Devolve a reserva criada ou None se houver erro (ex.: artigo inexistente).
        """

        if data_fim <= data_inicio:
            # regra simples: não aceitar datas inválidas
            return None

        artigos = []
        for art_id in ids_artigos:
            artigo = self.artigos.get(art_id)
            if artigo is None or not artigo.verificar_disponibilidade():
                # se algum artigo não existir ou estiver indisponível, falha
                return None
            artigos.append(artigo)

        reserva = Reserva(
            id=self._proximo_id_reserva,
            cliente=cliente,
            artigos=artigos,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
        reserva.calcular_total()
        reserva.confirmar()

        # guardar
        self.reservas[reserva.id] = reserva
        self._proximo_id_reserva += 1

        # associar ao cliente
        cliente.fazer_reserva(reserva)

        return reserva

    def listar_reservas(self):
        return list(self.reservas.values())

    def listar_reservas_cliente(self, cliente: Cliente):
        return cliente.consultar_historico()

    def cancelar_reserva(self, reserva_id: int) -> bool:
        reserva = self.reservas.get(reserva_id)
        if reserva is None:
            return False
        reserva.estado = "Cancelada"
        return True
