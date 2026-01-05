#!/usr/bin/env python3
"""
Sistema de Reservas de Artigos Desportivos
Redirecionamento para Projeto/main.py
"""
import sys
import os

# Adicionar o diretório Projeto ao path
projeto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Projeto')
sys.path.insert(0, projeto_path)

# Mudar para o diretório Projeto para que os caminhos relativos funcionem
os.chdir(projeto_path)

# Importar e executar o main do Projeto
from main import main

if __name__ == "__main__":
    main()
