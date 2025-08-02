#!/usr/bin/env python3
"""
API FastAPI para consulta de livros
Tech Challenge - Fase 1 - Machine Learning Engineering
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from pathlib import Path

# Importar modelos
from models import Book, BookSummary, Category, HealthStatus, StatsOverview, CategoryStats
from database import BooksDatabase

# Configuração da aplicação
app = FastAPI(
    title="Books API - Tech Challenge",
    description="API pública para consulta de livros extraídos via web scraping",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar banco de dados
db = BooksDatabase()

# Handler para Vercel
from mangum import Mangum
handler = Mangum(app)

@app.on_event("startup")
async def startup_event():
    """Carregar dados na inicialização"""
    await db.load_data()

# Endpoints Core

@app.get("/api/v1/health", response_model=HealthStatus)
async def health_check():
    """Status da API e conectividade"""
    total_books = await db.count_books()
    return HealthStatus(
        status="healthy",
        message="API funcionando corretamente",
        total_books=total_books,
        version="1.0.0"
    )

@app.get("/api/v1/books", response_model=List[BookSummary])
async def get_all_books(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(50, ge=1, le=100, description="Livros por página")
):
    """Lista todos os livros disponíveis com paginação"""
    books = await db.get_books(page=page, limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    return books

@app.get("/api/v1/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    """Detalhes completos de um livro específico"""
    book = await db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

@app.get("/api/v1/books/search", response_model=List[BookSummary])
async def search_books(
    title: Optional[str] = Query(None, description="Buscar por título"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(50, ge=1, le=100, description="Livros por página")
):
    """Busca por título e/ou categoria"""
    if not title and not category:
        raise HTTPException(status_code=400, detail="Pelo menos um parâmetro de busca é necessário")
    
    books = await db.search_books(title=title, category=category, page=page, limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado com os critérios especificados")
    return books

@app.get("/api/v1/categories", response_model=List[Category])
async def get_categories():
    """Lista todas as categorias disponíveis"""
    categories = await db.get_categories()
    if not categories:
        raise HTTPException(status_code=404, detail="Nenhuma categoria encontrada")
    return categories

# Endpoints Opcionais (Insights)

@app.get("/api/v1/stats/overview", response_model=StatsOverview)
async def get_stats_overview():
    """Estatísticas gerais (total, preço médio, ratings)"""
    stats = await db.get_overview_stats()
    return stats

@app.get("/api/v1/stats/categories", response_model=List[CategoryStats])
async def get_category_stats():
    """Estatísticas por categoria"""
    stats = await db.get_category_stats()
    if not stats:
        raise HTTPException(status_code=404, detail="Nenhuma estatística encontrada")
    return stats

@app.get("/api/v1/books/top-rated", response_model=List[BookSummary])
async def get_top_rated_books(
    limit: int = Query(10, ge=1, le=50, description="Número de livros a retornar")
):
    """Livros com melhor avaliação"""
    books = await db.get_top_rated_books(limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    return books

@app.get("/api/v1/books/price-range", response_model=List[BookSummary])
async def get_books_by_price_range(
    min_price: float = Query(0, ge=0, description="Preço mínimo"),
    max_price: float = Query(100, ge=0, description="Preço máximo"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(50, ge=1, le=100, description="Livros por página")
):
    """Filtro por faixa de preço"""
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="Preço mínimo não pode ser maior que o máximo")
    
    books = await db.get_books_by_price_range(min_price=min_price, max_price=max_price, page=page, limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado na faixa de preço especificada")
    return books

# Endpoint raiz
@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Books API - Tech Challenge",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)