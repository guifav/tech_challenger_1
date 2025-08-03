# Tech Challenge - Fase 1 - Machine Learning Engineering

## Visão Geral do Projeto

**Desafio**: Criação de uma API Pública para Consulta de Livros

Você foi contratado como Engenheiro de Machine Learning para desenvolver um sistema de recomendação de livros. O objetivo é criar uma infraestrutura completa de extração, transformação e disponibilização de dados via API pública para cientistas de dados e serviços de recomendação.

## Objetivo Principal

Desenvolver um **pipeline completo de dados** e uma **API pública** escalável e reutilizável para modelos de machine learning, servindo dados de livros extraídos via web scraping.

## Entregáveis Obrigatórios

### 1. Repositório GitHub Organizado
- **Estrutura**: Código organizado em módulos (`scripts/`, `api/`, `data/`, etc.)
- **README Completo** contendo:
  - Descrição do projeto e arquitetura
  - Instruções de instalação e configuração
  - Documentação das rotas da API
  - Exemplos de requests/responses
  - Instruções de execução

### 2. Sistema de Web Scraping
- **Fonte de dados**: https://books.toscrape.com/
- **Campos obrigatórios**: título, preço, rating, disponibilidade, categoria, imagem
- **Saída**: Arquivo CSV com todos os dados extraídos
- **Requisitos**: Script automatizado e bem documentado

### 3. API RESTful Funcional
- **Framework**: Fast API
- **Documentação**: Swagger
- **Endpoints obrigatórios** (ver seção detalhada abaixo)

### 4. Deploy Público
- **Plataformas**: Vercel
- **Requisito**: API totalmente operacional em produção
- **Entrega**: Link compartilhável funcional

### 5. Plano Arquitetural
- **Diagrama/Documento** detalhando:
  - Pipeline: ingestão → processamento → API → consumo
  - Arquitetura para escalabilidade futura
  - Cenário de uso para cientistas de dados/ML
  - Plano de integração com modelos de ML

### 6. Vídeo de Apresentação (3-12 minutos)
- Demonstração técnica (visão macro)
- Apresentação da arquitetura e pipeline
- Execução de chamadas reais à API em produção
- Comentários sobre boas práticas implementadas

## Especificações Técnicas

### Endpoints Obrigatórios da API

#### Endpoints Core
- `GET /api/v1/books` - Lista todos os livros disponíveis
- `GET /api/v1/books/{id}` - Detalhes completos de um livro específico
- `GET /api/v1/books/search?title={title}&category={category}` - Busca por título e/ou categoria
- `GET /api/v1/categories` - Lista todas as categorias disponíveis
- `GET /api/v1/health` - Status da API e conectividade

#### Endpoints Opcionais (Insights)
- `GET /api/v1/stats/overview` - Estatísticas gerais (total, preço médio, ratings)
- `GET /api/v1/stats/categories` - Estatísticas por categoria
- `GET /api/v1/books/top-rated` - Livros com melhor avaliação
- `GET /api/v1/books/price-range?min={min}&max={max}` - Filtro por faixa de preço

## Arquitetura Esperada

```
[Web Scraping] → [Dados CSV] → [API RESTful] → [Consumidores ML]
     ↓              ↓              ↓              ↓
  books.toscrape   Armazenamento   FastAPI      Cientistas
     .com          Local/CSV       + Swagger     de Dados
```

## Próximos Passos

1. **Desenvolvimento**: Implementar scraping, Armazenar dados em CSV e disponibilizar via FastAPI
2. **Deploy**: Publicar API no Vercel
3. **Documentação**: Criar README e documentação técnica
4. **Apresentação**: Gravar vídeo demonstrativo

