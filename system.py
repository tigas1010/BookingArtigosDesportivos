# Aqui será criado as regras do booking: login, utilizadores, validar o login, criar as reservas, ver a disponibilidade

class BookingSystem():
    
    # Gestão de utilizadores
    def __init__(self):
        self.utilizadores = [] # começamos como listas vazias 
        self.artigos = [] 
        self.categorias = []
        self.reservas = []
        self.user_autenticado = None
    
    # Este método de receber o user e a passe
    # percorrer a lista dos utilizadores
    # verificar se existe um user valido e guardar o user autenticado no sistema
    def login(self, username, passe): 
        for i in self.utilizadores: 
            if username == i[0] and passe == i[1]: # percorre a lista de user e passe
                self.user_autenticado = i #verifica se for igual entrou senao não
                print("Entrada com Sucesso!")
                return True
            
        print("Utilizador ou Palavra-Passe incorretas!")
        return False        
            
    def adicionar_utilizador(self, username, passe):
        utilizador_criado = (username , passe) 
        self.utilizadores.append(utilizador_criado)
    
    def logout (self):
        self.user_autenticado = None # volta ao estado inicial
        print("Logout efetuado com sucesso.")
    
    # Categorias de reservas
    
    def adicionar_categoria(self, nome_categoria, descricao):
        categoria_criada = (nome_categoria, descricao)
        self.categorias.append(categoria_criada)
        return categoria_criada
    
    # Gestão de Artigos
    
    def adicionar_artigo(self, nome_artigo, quantidade): # adicionar um artigo com nome e quantidade
        artigo_criado = (nome_artigo, quantidade) # criar uma lista tupla para os artigos
        self.artigos.append(artigo_criado) #adiciona artigo
        return artigo_criado
        
    def remover_artigo(self, nome_artigo):  # remover um artigo pelo nome
        for artigo in self.artigos: # percorre a lista de artigos
            if artigo[0] == nome_artigo:   # verifica se o nome é igual ao que queremos remover
                self.artigos.remove(artigo) # remove o artigo
                print(f"Artigo {nome_artigo} foi removido com sucesso.")
                
                return True
            
        print(f"Artigo {nome_artigo} não foi encontrado.")
        return False
    
    def lista_artigos(self):
        return self.artigos # retorna a lista de todos artigos
    
    def artigos_disponiveis(self):
        disponiveis = [] #lista vazia para os artigos que irão estar disponiveis
        print("Artigos disponiveis: ")
        for artigo in self.artigos:
            if artigo[1] > 0:
                disponiveis.append(artigo)
        return disponiveis
    
    
    # Gestão de Reservas

    def criar_reserva(self, nome_cliente, dia_reserva, termino_reserva, nome_artigo, quantidade):
        reserva = (nome_cliente, dia_reserva, termino_reserva, nome_artigo, quantidade)
        for artigo in self.artigos:
            if artigo[0] == nome_artigo:
                if artigo[1] >= quantidade:
                    self.reservas.append(reserva)
                    
                
                 
                
            
        
         
    
     
    