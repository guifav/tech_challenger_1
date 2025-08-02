#!/usr/bin/env python3
"""
Web Scraper para books.toscrape.com
Extrai dados de livros e salva em formato CSV
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin, urlparse
import os

class BooksScraper:
    def __init__(self, base_url="https://books.toscrape.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.books_data = []
        
    def get_rating_number(self, rating_class):
        """Converte rating em texto para número"""
        rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
        }
        for word, num in rating_map.items():
            if word in rating_class:
                return num
        return 0
    
    def clean_price(self, price_text):
        """Remove símbolos de moeda e converte para float"""
        return float(re.sub(r'[^\d.]', '', price_text))
    
    def extract_category_from_page(self, page_url):
        """Extrai a categoria da página atual"""
        try:
            response = self.session.get(page_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tentar extrair categoria do breadcrumb ou título da página
            breadcrumb = soup.find('ul', class_='breadcrumb')
            if breadcrumb:
                breadcrumb_items = breadcrumb.find_all('li')
                if len(breadcrumb_items) > 1:
                    return breadcrumb_items[-1].get_text(strip=True)
            
            # Fallback: tentar extrair do título da página
            title_tag = soup.find('title')
            if title_tag and 'Books to Scrape' in title_tag.get_text():
                title_parts = title_tag.get_text().split('|')
                if len(title_parts) > 1:
                    return title_parts[0].strip()
            
            return "General"
        except Exception as e:
            print(f"Erro ao extrair categoria da página {page_url}: {e}")
            return "General"
    
    def scrape_page(self, page_url):
        """Extrai dados de uma página de livros"""
        try:
            response = self.session.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair categoria da página atual
            current_category = self.extract_category_from_page(page_url)
            
            books = soup.find_all('article', class_='product_pod')
            
            for book in books:
                # Título
                title_element = book.find('h3').find('a')
                title = title_element.get('title', title_element.get_text(strip=True))
                
                # URL do livro
                book_url = urljoin(self.base_url, title_element.get('href'))
                
                # Preço
                price_element = book.find('p', class_='price_color')
                price = self.clean_price(price_element.get_text()) if price_element else 0.0
                
                # Rating
                rating_element = book.find('p', class_='star-rating')
                rating = 0
                if rating_element:
                    rating_class = rating_element.get('class', [])
                    for cls in rating_class:
                        if cls != 'star-rating':
                            rating = self.get_rating_number(cls)
                            break
                
                # Imagem
                img_element = book.find('div', class_='image_container').find('img')
                image_url = urljoin(self.base_url, img_element.get('src')) if img_element else ""
                
                # Disponibilidade - tentar extrair da página principal
                availability = "In stock"
                availability_element = book.find('p', class_='instock')
                if availability_element:
                    availability = availability_element.get_text(strip=True)
                else:
                    # Verificar se há indicação de falta de estoque
                    if book.find('p', class_='outofstock'):
                        availability = "Out of stock"
                
                book_data = {
                    'id': len(self.books_data) + 1,
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': availability,
                    'category': current_category,
                    'image_url': image_url,
                    'book_url': book_url
                }
                
                self.books_data.append(book_data)
                print(f"Livro extraído: {title} - Categoria: {current_category}")
                
        except Exception as e:
            print(f"Erro ao processar página {page_url}: {e}")
    
    def scrape_all_books(self):
        """Extrai todos os livros do site"""
        print("Iniciando scraping de books.toscrape.com...")
        
        page_num = 1
        while True:
            if page_num == 1:
                page_url = self.base_url
            else:
                page_url = f"{self.base_url}catalogue/page-{page_num}.html"
            
            print(f"Processando página {page_num}...")
            
            # Verificar se a página existe
            try:
                response = self.session.get(page_url)
                response.raise_for_status()
                
                # Verificar se há livros na página
                soup = BeautifulSoup(response.content, 'html.parser')
                books = soup.find_all('article', class_='product_pod')
                
                if not books:
                    print(f"Nenhum livro encontrado na página {page_num}. Finalizando...")
                    break
                
                self.scrape_page(page_url)
                page_num += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar página {page_num}: {e}")
                break
        
        print(f"Scraping concluído! Total de livros extraídos: {len(self.books_data)}")
    
    def save_to_csv(self, filename="books_data.csv"):
        """Salva os dados em arquivo CSV"""
        if not self.books_data:
            print("Nenhum dado para salvar!")
            return
        
        # Criar diretório data se não existir
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        filepath = os.path.join(data_dir, filename)
        
        df = pd.DataFrame(self.books_data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Dados salvos em: {filepath}")
        
        # Mostrar estatísticas
        print(f"\nEstatísticas dos dados:")
        print(f"Total de livros: {len(df)}")
        print(f"Categorias únicas: {df['category'].nunique()}")
        print(f"Preço médio: £{df['price'].mean():.2f}")
        print(f"Rating médio: {df['rating'].mean():.1f}")

def main():
    """Função principal"""
    scraper = BooksScraper()
    scraper.scrape_all_books()
    scraper.save_to_csv()

if __name__ == "__main__":
    main()