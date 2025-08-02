import sys
from pathlib import Path

# Adicionar diretórios ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "api"))

# Importar a aplicação FastAPI
from api.main import app

# Expor a variável app para o Vercel
app = app
