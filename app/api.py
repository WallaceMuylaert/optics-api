from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import Base, engine, get_db
from routers.users import router as users_router
from routers.suppliers import router as suppliers_router
from routers.orders import router as orders_router
from routers.address import router as address_router
from routers.login import router as login_router


# Cria a aplicação FastAPI
app = FastAPI(title="optics-api", description="API para gerenciamento de óticas", version="1.0")

# Configura o CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inclui as rotas
app.include_router(login_router)
app.include_router(users_router)
app.include_router(suppliers_router)
app.include_router(orders_router)
app.include_router(address_router)