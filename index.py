#!/usr/bin/env python3
"""
Ponto de entrada para o Vercel
Configuração robusta com fallbacks
"""

import sys
import os
from pathlib import Path

# Adicionar diretórios ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "api"))

try:
    from api.main import app
except ImportError as e:
    # Fallback usando importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location("api.main", current_dir / "api" / "main.py")
    if spec and spec.loader:
        api_main = importlib.util.module_from_spec(spec)
        sys.modules["api.main"] = api_main
        spec.loader.exec_module(api_main)
        app = api_main.app
    else:
        raise ImportError(f"Could not import api.main: {e}")

# Esta é a variável que o Vercel procura
handler = app