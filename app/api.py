from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from requests import Session
from database.database import Base, engine, get_db
from models.model import Supplier, User
from routers.users import router as users_router
from routers.suppliers import router as suppliers_router
from routers.orders import router as orders_router
from routers.address import router as address_router
from schemas.schema import LoginRequest, LoginResponse


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

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # Verifica se é um User
    user = db.query(User).filter(User.email == login_request.email).first()
    if user and user.check_password(login_request.password):
        return {"token": "dummy_token", "user_type": "user"}

    # Verifica se é um Supplier
    supplier = db.query(Supplier).filter(Supplier.email == login_request.email).first()
    if supplier and supplier.check_password(login_request.password):
        return {"token": "dummy_token", "user_type": "supplier"}

    # Se não encontrou nenhum, retorna erro
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Inclui as rotas
app.include_router(users_router)
app.include_router(suppliers_router)
app.include_router(orders_router)
app.include_router(address_router) 