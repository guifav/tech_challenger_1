#!/usr/bin/env python3
"""
Ponto de entrada para o Vercel
Redireciona para a aplicação FastAPI
"""

from api.main import app

# Exportar a aplicação para o Vercel
app = app