#!/usr/bin/env python3
"""
Ponto de entrada para o Vercel
Redireciona para a aplicação FastAPI
"""
Running build in Washington, D.C., USA (East) – iad1
Build machine configuration: 2 cores, 8 GB
Cloning github.com/guifav/tech_challenger_1 (Branch: main, Commit: 90282e8)
Skipping build cache, deployment was triggered without cache.
Cloning completed: 308.000ms
Running "vercel build"
Vercel CLI 44.6.4
Installing required dependencies...
Installing required dependencies...
Installing required dependencies...
Build Completed in /vercel/output [45s]
Deploying outputs...
Deployment completed
Uploading build cache [4.00 kB]...
Build cache uploaded: 71.244ms
Exiting build container

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from api.main import app
except ImportError:
    # Fallback para ambiente Vercel
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", current_dir / "api" / "main.py")
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    app = main_module.app

# Exportar a aplicação para o Vercel
handler = app