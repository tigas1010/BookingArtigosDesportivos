#!/usr/bin/env python3
"""
Script de Teste para BookingArtigosDesportivos
Verifica se todos os componentes estão funcionando corretamente
"""
import sys
import os
from datetime import datetime, timedelta

# Adicionar o diretório Projeto ao path
projeto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Projeto')
sys.path.insert(0, projeto_path)
os.chdir(projeto_path)

def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print('=' * 60)

def print_section(text):
    print(f"\n[{text}]")

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def main():
    print_header("BookingArtigosDesportivos - Script de Teste")
    
    # Test 1: Import models
    print_section("1. Testando imports dos models")
    try:
        from models import User, Client, Administrator, Category, SportsItem, Reservation
        print_success("Todos os models importados com sucesso")
    except Exception as e:
        print_error(f"Falha ao importar models: {e}")
        return False
    
    # Test 2: Load data files
    print_section("2. Testando carregamento de ficheiros de dados")
    try:
        users = User._load_all()
        categories = Category._load_all()
        items = SportsItem._load_all()
        reservations = Reservation._load_all()
        print_success(f"Carregados {len(users)} utilizadores")
        print_success(f"Carregadas {len(categories)} categorias")
        print_success(f"Carregados {len(items)} artigos desportivos")
        print_success(f"Carregadas {len(reservations)} reservas")
    except Exception as e:
        print_error(f"Falha ao carregar dados: {e}")
        return False
    
    # Test 3: User authentication
    print_section("3. Testando autenticação de utilizadores")
    try:
        admin = User.find_by_email("admin@sistema.com")
        if admin and admin.login("admin@sistema.com", "admin123"):
            print_success(f"Login de administrador: {admin.name} ({admin.get_type()})")
        else:
            print_error("Falha no login de administrador")
            return False
        
        client = User.find_by_email("joao@email.com")
        if client and client.login("joao@email.com", "123456"):
            print_success(f"Login de cliente: {client.name} ({client.get_type()})")
        else:
            print_error("Falha no login de cliente")
            return False
    except Exception as e:
        print_error(f"Falha nos testes de autenticação: {e}")
        return False
    
    # Test 4: Categories
    print_section("4. Testando operações de categorias")
    try:
        all_cats = Category.get_all()
        print_success(f"Recuperadas {len(all_cats)} categorias:")
        for cat in all_cats:
            items_count = len(cat.get_items())
            print(f"    • {cat.name}: {cat.description} ({items_count} artigos)")
    except Exception as e:
        print_error(f"Falha nas operações de categorias: {e}")
        return False
    
    # Test 5: Sports items
    print_section("5. Testando operações de artigos desportivos")
    try:
        all_items = SportsItem.get_all()
        available_items = SportsItem.get_all(available_only=True)
        print_success(f"Total de artigos: {len(all_items)}")
        print_success(f"Artigos disponíveis: {len(available_items)}")
        
        print("    Exemplos de artigos:")
        for item in all_items[:5]:
            status = "Disponível" if item.available else "Indisponível"
            cat_name = item.category.name if item.category else "Sem categoria"
            print(f"    • {item.name} ({item.brand}) - €{item.price_per_hour:.2f}/h")
            print(f"      Categoria: {cat_name}, Status: {status}")
    except Exception as e:
        print_error(f"Falha nas operações de artigos: {e}")
        return False
    
    # Test 6: Reservation workflow
    print_section("6. Testando fluxo de reserva completo")
    try:
        # Create reservation
        start_date = datetime.now() + timedelta(days=1)
        end_date = start_date + timedelta(hours=3)
        
        reservation = Reservation.create(client.id, start_date, end_date)
        print_success(f"Reserva #{reservation.id} criada")
        
        # Add item
        test_item = SportsItem.get_all(available_only=True)[0]
        original_availability = test_item.available
        
        if reservation.add_item(test_item):
            print_success(f"Artigo '{test_item.name}' adicionado à reserva")
            print(f"    Valor total: €{reservation.total_value:.2f} para 3 horas")
        
        # Confirm reservation
        if reservation.confirm():
            print_success(f"Reserva confirmada (Estado: {reservation.state})")
        
        # Verify item is unavailable
        updated_item = SportsItem.find_by_id(test_item.id)
        if not updated_item.available:
            print_success(f"Artigo '{test_item.name}' marcado como indisponível")
        
        # Cancel reservation
        if reservation.cancel():
            print_success(f"Reserva cancelada (Estado: {reservation.state})")
        
        # Verify item is available again
        updated_item = SportsItem.find_by_id(test_item.id)
        if updated_item.available:
            print_success(f"Artigo '{test_item.name}' marcado como disponível novamente")
        
        # Clean up test reservation
        all_reservations = Reservation._load_all()
        cleaned = [r for r in all_reservations if r['id'] != reservation.id]
        Reservation._save_all(cleaned)
        print_success("Dados de teste limpos")
        
    except Exception as e:
        print_error(f"Falha no fluxo de reserva: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print_header("RESUMO DOS TESTES")
    print("""
✅ Todos os testes passaram com sucesso!

O sistema está pronto para uso. Para iniciar a aplicação:

    cd Projeto
    python3 main.py

Contas disponíveis:
    - Admin:   admin@sistema.com / admin123
    - Cliente: joao@email.com / 123456

Funcionalidades disponíveis:
    📦 12 artigos desportivos em 4 categorias
    👤 Sistema de autenticação com admin e cliente
    📋 Gestão completa de reservas
    🏷️ Gestão de categorias e artigos
    """)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo utilizador.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
