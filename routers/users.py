from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schema import *
from crud.users import *

router = APIRouter(prefix="/users", tags=["users"])

# Criar um novo usuário
@router.post(
    "/",
    response_model=UserInDB,
    summary="Cria um novo usuário",
    description="Endpoint para criar um novo usuário no sistema. "
                "Verifica se o e-mail já está registrado antes de criar o usuário.",
    response_description="Retorna os detalhes do usuário criado."
)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com base nos dados fornecidos.

    - **name**: Nome completo do usuário.
    - **email**: E-mail do usuário (deve ser único).
    - **password**: Senha do usuário (será hasheada antes de ser armazenada).
    - **phone**: Número de telefone do usuário (opcional).
    - **cpf**: CPF do usuário (deve ser único).

    Se o e-mail já estiver registrado, retorna um erro 400.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return create_user(db=db, user=user)

# Buscar um usuário por ID
@router.get(
    "/{user_id}",
    response_model=UserInDB,
    summary="Busca um usuário por ID",
    description="Endpoint para buscar um usuário específico pelo seu ID.",
    response_description="Retorna os detalhes do usuário encontrado."
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Busca um usuário pelo seu ID.

    - **user_id**: ID do usuário a ser buscado.

    Se o usuário não for encontrado, retorna um erro 404.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

# Listar todos os usuários
@router.get(
    "/",
    response_model=list[UserInDB],
    summary="Lista todos os usuários",
    description="Endpoint para listar todos os usuários cadastrados no sistema. "
                "Permite paginação usando os parâmetros `skip` e `limit`.",
    response_description="Retorna uma lista de usuários."
)
def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos os usuários cadastrados.

    - **skip**: Número de registros a serem ignorados (para paginação).
    - **limit**: Número máximo de registros a serem retornados (para paginação).

    Retorna uma lista de usuários.
    """
    users = get_all_users(db, skip=skip, limit=limit)
    return users

# Atualizar um usuário
@router.put(
    "/{user_id}",
    response_model=UserInDB,
    summary="Atualiza um usuário existente",
    description="Endpoint para atualizar os dados de um usuário existente. "
                "Apenas os campos fornecidos serão atualizados.",
    response_description="Retorna os detalhes do usuário atualizado."
)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um usuário existente.

    - **user_id**: ID do usuário a ser atualizado.
    - **user**: Dados do usuário a serem atualizados (apenas os campos fornecidos).

    Se o usuário não for encontrado, retorna um erro 404.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return update_user(db=db, user_id=user_id, user=user)

# Excluir um usuário
@router.delete(
    "/{user_id}",
    response_model=dict,
    summary="Exclui um usuário existente",
    description="Endpoint para excluir um usuário existente pelo seu ID.",
    response_description="Retorna uma mensagem de confirmação."
)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """
    Exclui um usuário existente.

    - **user_id**: ID do usuário a ser excluído.

    Se o usuário não for encontrado, retorna um erro 404.
    Retorna uma mensagem de confirmação da exclusão.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    delete_user(db=db, user_id=user_id)
    return {"message": "Usuário excluído com sucesso"}