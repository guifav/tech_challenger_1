# Books API - Tech Challenge Fase 1

## Descrição

API pública para consulta de livros extraídos via web scraping do site [books.toscrape.com](https://books.toscrape.com/). Este projeto faz parte do Tech Challenge da Fase 1 de Machine Learning Engineering FIAP / ALURA.

**Aluno: Guilherme Favaron**

**Video de Apresentação deste Projeto**: [VIDEO](https://youtu.be/0UPtn1BMsTQ?si=VqZLD6QM9NNO7Jga)

## Funcionalidades

- **Web Scraping**: Extração automatizada de dados de livros
- **API RESTful**: Endpoints para consulta e busca de livros
- **Documentação Swagger**: Interface interativa para testes
- **Paginação**: Suporte a consultas paginadas
- **Filtros**: Busca por título, categoria e faixa de preço
- **Estatísticas**: Dados agregados sobre o catálogo

## Dados Extraídos

Cada livro contém as seguintes informações:
- **Título**: Nome completo do livro
- **Preço**: Valor em libras (£)
- **Rating**: Avaliação de 1 a 5 estrelas
- **Disponibilidade**: Status de estoque
- **Categoria**: Classificação do livro
- **Imagem**: URL da capa do livro
- **URL**: Link para a página do livro

## Tecnologias Utilizadas

- **Python 3.9+**
- **FastAPI**: Framework web moderno e rápido
- **BeautifulSoup4**: Web scraping
- **Pandas**: Manipulação de dados
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validação de dados

## Estrutura do Projeto

```
tech_challenge/
├── api/                    # API FastAPI
│   ├── main.py            # Aplicação principal
│   ├── models.py          # Modelos Pydantic
│   ├── database.py        # Gerenciamento de dados
│   └── __init__.py        # Inicialização do pacote
├── scripts/               # Scripts de web scraping
│   └── scraper.py         # Scraper principal
├── data/                  # Dados extraídos
│   └── books_data.csv     # Dataset de livros
├── docs/                  # Documentação
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```

## Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone git@github.com:guifav/tech_challenger_1.git
cd tech_challenger_1
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o web scraping** (opcional - dados já incluídos)
```bash
python3 scripts/scraper.py
```

4. **Inicie a API**
```bash
cd api
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Uso da API

### Documentação Interativa (localmente)
Acesse: http://localhost:8000/api/docs

### Endpoints Principais

#### Listar Livros
```http
GET /api/v1/books?page=1&limit=50
```

#### Buscar Livro por ID
```http
GET /api/v1/books/{book_id}
```

#### Buscar Livros
```http
GET /api/v1/books/search?title=python&category=technology
```

#### Listar Categorias
```http
GET /api/v1/categories
```

#### Estatísticas
```http
GET /api/v1/stats/overview
```

#### Top Livros
```http
GET /api/v1/books/top-rated?limit=10
```

#### Livros por Preço
```http
GET /api/v1/books/price-range?min_price=10&max_price=50
```

## Exemplos de Uso

### Python
```python
import requests

# Buscar livros
response = requests.get('http://localhost:8000/api/v1/books?limit=5')
books = response.json()

# Buscar por título
response = requests.get('http://localhost:8000/api/v1/books/search?title=python')
results = response.json()
```

### cURL
```bash
# Listar primeiros 5 livros
curl "http://localhost:8000/api/v1/books?limit=5"

# Buscar livro específico
curl "http://localhost:8000/api/v1/books/1"

# Estatísticas gerais
curl "http://localhost:8000/api/v1/stats/overview"
```

## Dados do Dataset

- **Total de livros**: 1.000
- **Formato**: CSV
- **Localização**: `data/books_data.csv`
- **Campos**: id, title, price, rating, availability, category, image_url, book_url

## Deploy

Este projeto está preparado para deploy no Vercel. Consulte o plano arquitetural para mais detalhes sobre escalabilidade e integração.

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é parte do Tech Challenge e está disponível para fins educacionais.

## Contato

Para dúvidas ou sugestões sobre este projeto, entre em contato comigo. Procure no LinkedIn por Guilherme Favaron (https://www.linkedin.com/in/guilhermefavaron/) ou acesse www.guilhermefavaron.com.br 

---

**Tech Challenge - Fase 1 - Machine Learning Engineering**