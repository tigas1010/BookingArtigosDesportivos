# Sistema de Reservas de Artigos Desportivos

Sistema de gestão de reservas de artigos desportivos desenvolvido em Python com interface gráfica Tkinter.

## Descrição

Este é um projeto universitário que implementa um sistema completo de booking/reservas de artigos desportivos. A aplicação permite:

- **Login de Utilizadores**: Sistema com autenticação para Clientes e Administradores
- **Clientes podem**:
  - Fazer reservas de artigos desportivos
  - Consultar histórico de reservas
  - Cancelar reservas pendentes ou confirmadas
  - Filtrar artigos por categoria
  
- **Administradores podem**:
  - Gerir stock de artigos (adicionar, remover, alterar disponibilidade)
  - Gerir categorias de artigos
  - Visualizar e cancelar reservas de todos os clientes
  - Filtrar reservas por estado

## Estrutura do Projeto

```
BookingArtigosDesportivos/
├── Projeto/
│   ├── main.py                 # Ficheiro principal da aplicação
│   ├── data/                   # Dados persistentes em JSON
│   │   ├── users.json
│   │   ├── categories.json
│   │   ├── sports_items.json
│   │   └── reservations.json
│   ├── models/                 # Classes do domínio (OOP)
│   │   ├── __init__.py
│   │   ├── user.py            # User, Client, Administrator
│   │   ├── category.py
│   │   ├── sports_item.py
│   │   └── reservation.py
│   └── Views/                  # Interface gráfica (Tkinter)
│       ├── __init__.py
│       ├── login_view.py
│       ├── client_view.py
│       └── admin_view.py
├── README.md
└── requirements.txt
```

## Requisitos

- Python 3.x
- Tkinter (geralmente já incluído com Python)

### Verificar se Tkinter está instalado

```bash
python3 -m tkinter
```

Se aparecer uma pequena janela, o Tkinter está instalado corretamente.

### Instalar Tkinter (se necessário)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter já vem instalado com Python do python.org

**Windows:**
Tkinter já vem instalado com Python

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/tigas1010/BookingArtigosDesportivos.git
cd BookingArtigosDesportivos
```

2. Não é necessário instalar dependências adicionais (Tkinter já vem com Python)

## Execução

Execute a aplicação a partir da pasta `Projeto`:

```bash
cd Projeto
python3 main.py
```

Ou execute diretamente:

```bash
python3 Projeto/main.py
```

## Contas de Teste

A aplicação vem com as seguintes contas pré-configuradas:

### Administrador
- **Email**: admin@sistema.com
- **Password**: admin123

### Cliente
- **Email**: joao@email.com
- **Password**: 123456

## Funcionalidades Principais

### Para Clientes

1. **Login/Registo**: Acesso ao sistema com credenciais ou criação de nova conta
2. **Consultar Artigos**: Visualizar artigos disponíveis com filtro por categoria
3. **Criar Reserva**: Selecionar artigos, definir período e confirmar reserva
4. **Histórico**: Consultar todas as reservas (pendentes, confirmadas, canceladas, completadas)
5. **Cancelar Reserva**: Cancelar reservas pendentes ou confirmadas

### Para Administradores

1. **Gerir Artigos**:
   - Adicionar novos artigos desportivos
   - Alterar disponibilidade (marcar como disponível/indisponível)
   - Remover artigos do sistema

2. **Gerir Categorias**:
   - Criar novas categorias
   - Remover categorias (apenas se não tiverem artigos associados)

3. **Gerir Reservas**:
   - Visualizar todas as reservas do sistema
   - Filtrar por estado (Pending, Confirmed, Cancelled, Completed)
   - Cancelar reservas de qualquer cliente

## Categorias Pré-configuradas

1. **Futebol**: Bolas, chuteiras, luvas de guarda-redes
2. **Desportos de Raquete**: Raquetes de ténis, badminton, bolas
3. **Natação**: Óculos, toucas, pranchas
4. **Fitness**: Halteres, tapetes de yoga, kettlebells

## Arquitetura

O projeto segue os princípios de **Programação Orientada a Objetos** com:

- **Herança**: Classe abstrata `User` com subclasses `Client` e `Administrator`
- **Encapsulamento**: Atributos privados com properties
- **Composição**: Relações entre objetos (Reservation contém SportsItems)
- **Persistência**: Dados guardados em ficheiros JSON

### Diagramas UML

O projeto inclui diagramas UML na pasta `Diagramas/`:
- Diagrama de Classes (mostra herança e relações)
- Diagrama de Objetos (exemplo de instâncias)

## Desenvolvimento

Este projeto foi desenvolvido como trabalho universitário para demonstrar:
- Programação Orientada a Objetos em Python
- Interfaces gráficas com Tkinter
- Persistência de dados com JSON
- Gestão de estados e fluxos de aplicação

## Autores

Projeto universitário - BookingArtigosDesportivos

## Licença

Projeto académico sem licença específica.
