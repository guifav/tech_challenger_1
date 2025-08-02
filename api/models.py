#!/usr/bin/env python3
"""
Modelos Pydantic para a API de livros
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    """Modelo base para livros"""
    title: str = Field(..., description="Título do livro")
    price: float = Field(..., ge=0, description="Preço do livro")
    rating: int = Field(..., ge=0, le=5, description="Avaliação do livro (0-5)")
    availability: str = Field(..., description="Status de disponibilidade")
    category: str = Field(..., description="Categoria do livro")
    image_url: str = Field(..., description="URL da imagem do livro")

class Book(BookBase):
    """Modelo completo do livro"""
    id: int = Field(..., description="ID único do livro")
    book_url: str = Field(..., description="URL da página do livro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "A Light in the Attic",
                "price": 51.77,
                "rating": 3,
                "availability": "In stock (22 available)",
                "category": "Poetry",
                "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg",
                "book_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
            }
        }

class BookSummary(BaseModel):
    """Modelo resumido do livro para listagens"""
    id: int = Field(..., description="ID único do livro")
    title: str = Field(..., description="Título do livro")
    price: float = Field(..., ge=0, description="Preço do livro")
    rating: int = Field(..., ge=0, le=5, description="Avaliação do livro (0-5)")
    category: str = Field(..., description="Categoria do livro")
    availability: str = Field(..., description="Status de disponibilidade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "A Light in the Attic",
                "price": 51.77,
                "rating": 3,
                "category": "Poetry",
                "availability": "In stock (22 available)"
            }
        }

class Category(BaseModel):
    """Modelo para categorias"""
    name: str = Field(..., description="Nome da categoria")
    count: int = Field(..., ge=0, description="Número de livros na categoria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Poetry",
                "count": 15
            }
        }

class HealthStatus(BaseModel):
    """Modelo para status de saúde da API"""
    status: str = Field(..., description="Status da API")
    message: str = Field(..., description="Mensagem de status")
    total_books: int = Field(..., ge=0, description="Total de livros disponíveis")
    version: str = Field(..., description="Versão da API")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da verificação")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "API funcionando corretamente",
                "total_books": 1000,
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class StatsOverview(BaseModel):
    """Modelo para estatísticas gerais"""
    total_books: int = Field(..., ge=0, description="Total de livros")
    total_categories: int = Field(..., ge=0, description="Total de categorias")
    average_price: float = Field(..., ge=0, description="Preço médio")
    average_rating: float = Field(..., ge=0, le=5, description="Avaliação média")
    price_range: dict = Field(..., description="Faixa de preços (min/max)")
    rating_distribution: dict = Field(..., description="Distribuição de ratings")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_books": 1000,
                "total_categories": 50,
                "average_price": 35.67,
                "average_rating": 3.2,
                "price_range": {"min": 10.00, "max": 59.99},
                "rating_distribution": {"1": 50, "2": 100, "3": 300, "4": 350, "5": 200}
            }
        }

class CategoryStats(BaseModel):
    """Modelo para estatísticas por categoria"""
    category: str = Field(..., description="Nome da categoria")
    total_books: int = Field(..., ge=0, description="Total de livros na categoria")
    average_price: float = Field(..., ge=0, description="Preço médio na categoria")
    average_rating: float = Field(..., ge=0, le=5, description="Avaliação média na categoria")
    price_range: dict = Field(..., description="Faixa de preços na categoria")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Fiction",
                "total_books": 150,
                "average_price": 32.45,
                "average_rating": 3.8,
                "price_range": {"min": 15.99, "max": 55.99}
            }
        }

class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    detail: str = Field(..., description="Descrição do erro")
    status_code: int = Field(..., description="Código de status HTTP")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do erro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Livro não encontrado",
                "status_code": 404,
                "timestamp": "2024-01-15T10:30:00"
            }
        }