#!/usr/bin/env python3
"""
Gerenciador de dados para a API de livros
"""

import pandas as pd
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
import asyncio
from .models import Book, BookSummary, Category, StatsOverview, CategoryStats

class BooksDatabase:
    """Classe para gerenciar dados de livros"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.data_loaded = False
        
    async def load_data(self):
        """Carrega dados do arquivo CSV"""
        try:
            # Buscar arquivo CSV na pasta data
            current_dir = Path(__file__).parent
            # Tentar diferentes caminhos para compatibilidade com Vercel
            possible_paths = [
                current_dir.parent / "data" / "books_data.csv",  # Local
                Path("data/books_data.csv"),  # Vercel
                Path("../data/books_data.csv"),  # Alternativo
            ]
            
            csv_path = None
            for path in possible_paths:
                if path.exists():
                    csv_path = path
                    break
            
            if csv_path is None:
                print("Arquivo CSV não encontrado em nenhum dos caminhos possíveis")
                print("Execute o scraper primeiro: python scripts/scraper.py")
                # Criar DataFrame vazio para evitar erros
                self.df = pd.DataFrame(columns=['id', 'title', 'price', 'rating', 'availability', 'category', 'image_url', 'book_url'])
                return
            
            self.df = pd.read_csv(csv_path)
            self.data_loaded = True
            print(f"Dados carregados: {len(self.df)} livros")
            
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.df = pd.DataFrame(columns=['id', 'title', 'price', 'rating', 'availability', 'category', 'image_url', 'book_url'])
    
    def _ensure_data_loaded(self):
        """Verifica se os dados foram carregados"""
        if not self.data_loaded or self.df is None:
            raise Exception("Dados não carregados. Execute o scraper primeiro.")
    
    async def count_books(self) -> int:
        """Retorna o total de livros"""
        if self.df is None:
            return 0
        return len(self.df)
    
    async def get_books(self, page: int = 1, limit: int = 50) -> List[BookSummary]:
        """Retorna lista paginada de livros"""
        if self.df is None or len(self.df) == 0:
            return []
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        books_slice = self.df.iloc[start_idx:end_idx]
        
        books = []
        for _, row in books_slice.iterrows():
            books.append(BookSummary(
                id=int(row['id']),
                title=str(row['title']),
                price=float(row['price']),
                rating=int(row['rating']),
                category=str(row['category']),
                availability=str(row['availability'])
            ))
        
        return books
    
    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Retorna um livro específico pelo ID"""
        if self.df is None:
            return None
        
        book_row = self.df[self.df['id'] == book_id]
        
        if book_row.empty:
            return None
        
        row = book_row.iloc[0]
        return Book(
            id=int(row['id']),
            title=str(row['title']),
            price=float(row['price']),
            rating=int(row['rating']),
            availability=str(row['availability']),
            category=str(row['category']),
            image_url=str(row['image_url']),
            book_url=str(row['book_url'])
        )
    
    async def search_books(self, title: Optional[str] = None, category: Optional[str] = None, 
                          page: int = 1, limit: int = 50) -> List[BookSummary]:
        """Busca livros por título e/ou categoria"""
        if self.df is None or len(self.df) == 0:
            return []
        
        filtered_df = self.df.copy()
        
        if title:
            filtered_df = filtered_df[filtered_df['title'].str.contains(title, case=False, na=False)]
        
        if category:
            filtered_df = filtered_df[filtered_df['category'].str.contains(category, case=False, na=False)]
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        books_slice = filtered_df.iloc[start_idx:end_idx]
        
        books = []
        for _, row in books_slice.iterrows():
            books.append(BookSummary(
                id=int(row['id']),
                title=str(row['title']),
                price=float(row['price']),
                rating=int(row['rating']),
                category=str(row['category']),
                availability=str(row['availability'])
            ))
        
        return books
    
    async def get_categories(self) -> List[Category]:
        """Retorna lista de categorias com contagem"""
        if self.df is None or len(self.df) == 0:
            return []
        
        category_counts = self.df['category'].value_counts()
        
        categories = []
        for category, count in category_counts.items():
            categories.append(Category(
                name=str(category),
                count=int(count)
            ))
        
        return categories
    
    async def get_overview_stats(self) -> StatsOverview:
        """Retorna estatísticas gerais"""
        if self.df is None or len(self.df) == 0:
            return StatsOverview(
                total_books=0,
                total_categories=0,
                average_price=0.0,
                average_rating=0.0,
                price_range={"min": 0.0, "max": 0.0},
                rating_distribution={}
            )
        
        rating_dist = self.df['rating'].value_counts().to_dict()
        rating_distribution = {str(k): int(v) for k, v in rating_dist.items()}
        
        return StatsOverview(
            total_books=len(self.df),
            total_categories=self.df['category'].nunique(),
            average_price=float(self.df['price'].mean()),
            average_rating=float(self.df['rating'].mean()),
            price_range={
                "min": float(self.df['price'].min()),
                "max": float(self.df['price'].max())
            },
            rating_distribution=rating_distribution
        )
    
    async def get_category_stats(self) -> List[CategoryStats]:
        """Retorna estatísticas por categoria"""
        if self.df is None or len(self.df) == 0:
            return []
        
        stats = []
        for category in self.df['category'].unique():
            category_df = self.df[self.df['category'] == category]
            
            stats.append(CategoryStats(
                category=str(category),
                total_books=len(category_df),
                average_price=float(category_df['price'].mean()),
                average_rating=float(category_df['rating'].mean()),
                price_range={
                    "min": float(category_df['price'].min()),
                    "max": float(category_df['price'].max())
                }
            ))
        
        return stats
    
    async def get_top_rated_books(self, limit: int = 10) -> List[BookSummary]:
        """Retorna livros com melhor avaliação"""
        if self.df is None or len(self.df) == 0:
            return []
        
        # Ordenar por rating (desc) e depois por preço (asc) para desempate
        top_books = self.df.nlargest(limit, ['rating', 'price'])
        
        books = []
        for _, row in top_books.iterrows():
            books.append(BookSummary(
                id=int(row['id']),
                title=str(row['title']),
                price=float(row['price']),
                rating=int(row['rating']),
                category=str(row['category']),
                availability=str(row['availability'])
            ))
        
        return books
    
    async def get_books_by_price_range(self, min_price: float, max_price: float, 
                                      page: int = 1, limit: int = 50) -> List[BookSummary]:
        """Retorna livros dentro de uma faixa de preço"""
        if self.df is None or len(self.df) == 0:
            return []
        
        filtered_df = self.df[
            (self.df['price'] >= min_price) & 
            (self.df['price'] <= max_price)
        ]
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        books_slice = filtered_df.iloc[start_idx:end_idx]
        
        books = []
        for _, row in books_slice.iterrows():
            books.append(BookSummary(
                id=int(row['id']),
                title=str(row['title']),
                price=float(row['price']),
                rating=int(row['rating']),
                category=str(row['category']),
                availability=str(row['availability'])
            ))
        
        return books