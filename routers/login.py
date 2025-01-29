from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from database.database import get_db
from models.model import Supplier, User
from schemas.schema import LoginRequest, LoginResponse
from schemas.schema import *
from crud.orders import *


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # Verifica se é um User
    user = db.query(User).filter(User.email == login_request.email).first()
    if user and user.check_password(login_request.password):
        return {"token": "dummy_token", "user_type": "user"} # TODO: fAZER O TOKEN 

    # Verifica se é um Supplier
    supplier = db.query(Supplier).filter(Supplier.email == login_request.email).first()
    if supplier and supplier.check_password(login_request.password):
        return {"token": "dummy_token", "user_type": "supplier"} # TODO: fAZER O TOKEN 

    # Se não encontrou nenhum, retorna erro
    raise HTTPException(status_code=401, detail="Credenciais inválidas")