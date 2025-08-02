# Deploy no Vercel - Instruções

## Problema Identificado

O erro 404 no Vercel indica que a aplicação FastAPI não está sendo servida corretamente. Isso acontece porque o Vercel precisa de configurações específicas para aplicações Python.

## Solução Implementada

### 1. Arquivo `vercel.json` Criado

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```

### 2. Correções no `database.py`

- Adicionado suporte a múltiplos caminhos para o arquivo CSV
- Compatibilidade com ambiente Vercel

## Próximos Passos

1. **Fazer novo deploy no Vercel**:
   - Acesse o dashboard do Vercel
   - Faça redeploy do projeto
   - O Vercel detectará automaticamente o `vercel.json`

2. **URLs de Acesso**:
   - **API Root**: `https://tech-challenger-1.vercel.app/`
   - **Documentação**: `https://tech-challenger-1.vercel.app/api/docs`
   - **Health Check**: `https://tech-challenger-1.vercel.app/api/v1/health`

3. **Verificar Funcionamento**:
   ```bash
   # Testar health check
   curl https://tech-challenger-1.vercel.app/api/v1/health
   
   # Testar endpoint de livros
   curl https://tech-challenger-1.vercel.app/api/v1/books?limit=3
   ```

## Estrutura de URLs

- `/` - Página inicial da API
- `/api/docs` - Documentação Swagger
- `/api/redoc` - Documentação ReDoc
- `/api/v1/*` - Endpoints da API

## Troubleshooting

Se ainda houver problemas:

1. Verificar logs no dashboard do Vercel
2. Confirmar que o arquivo `data/books_data.csv` está no repositório
3. Verificar se todas as dependências estão no `requirements.txt`

## Arquivos Importantes

- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements.txt` - Dependências Python
- ✅ `api/main.py` - Aplicação FastAPI
- ✅ `data/books_data.csv` - Dados dos livros