from contextlib import asynccontextmanager
from fastapi import FastAPI

# Importa a função que inicia o banco de dados
from app.database import init_db

# Importa as rotas (graças ao __init__.py, podemos importar tudo de uma vez)
from app.routes import (
    department_router,
    professor_router,
    course_router,
    student_router,
    query_router
)

# 1. LIFESPAN (Ciclo de Vida)
# Esta função roda antes da API começar a receber requisições.
# É o momento exato para conectar ao MongoDB Atlas.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Lógica de Inicialização ---
    print("🚀 Inicializando conexão com o MongoDB Atlas...")
    await init_db()
    print("✅ Banco de dados conectado com sucesso!")
    
    yield  # A aplicação roda aqui
    
    # --- Lógica de Desligamento (Opcional) ---
    print("🛑 Aplicação encerrada.")

# 2. INSTÂNCIA DA APP
app = FastAPI(
    title="API de Gestão Estudantil",
    description="API assíncrona com FastAPI, MongoDB Atlas e Beanie ODM.",
    version="1.0.0",
    lifespan=lifespan # Conecta o ciclo de vida definido acima
)

# 3. REGISTRO DE ROTAS
# Aqui "acoplamos" os módulos de rotas à aplicação principal
app.include_router(department_router)
app.include_router(professor_router)
app.include_router(course_router)
app.include_router(student_router)
app.include_router(query_router)

# 4. ROTA RAIZ (Health Check)
# Uma rota simples para verificar se a API está no ar
@app.get("/", tags=["Status"])
async def root():
    return {
        "message": "Bem-vindo à API de Gestão Estudantil",
        "docs": "/docs",
        "redoc": "/redoc"
    }