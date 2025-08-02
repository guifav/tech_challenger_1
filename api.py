#!/usr/bin/env python3
"""
Serverless function para Vercel
Ponto de entrada alternativo para a API FastAPI
"""

import sys
import os
from pathlib import Path

# Configurar path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "api"))

# Importar aplicação
from api.main import app

# Handler para Vercel
def handler(request):
    return app(request)

# Exportar app diretamente também
app = app