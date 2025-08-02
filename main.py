#!/usr/bin/env python3
"""
Ponto de entrada principal para Vercel
Configuração simplificada seguindo as melhores práticas
"""

import sys
import os
from pathlib import Path

# Adicionar diretórios ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "api"))

# Importar a aplicação FastAPI
from api.main import app

# Esta é a variável que o Vercel procura
app = app