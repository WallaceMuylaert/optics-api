from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schema import AddressCreate, AddressUpdate, AddressInDB
from crud.address import *

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post(
    "/",
    response_model=AddressInDB,
    summary="Cria um novo endereço",
    description="Endpoint para criar um novo endereço no sistema.",
    response_description="Retorna os detalhes do endereço criado."
)
def create_new_address(address: AddressCreate, db: Session = Depends(get_db)):
    """
    Cria um novo endereço com base nos dados fornecidos.

    - **cep**: CEP do endereço.
    - **street**: Nome da rua.
    - **complement**: Complemento do endereço (opcional).
    - **state**: Estado do endereço.
    - **number**: Número do endereço.
    - **user_id**: ID do usuário associado ao endereço (opcional).
    - **supplier_id**: ID do fornecedor associado ao endereço (opcional).

    Retorna os detalhes do endereço criado.
    """
    return create_address(db=db, address=address)

@router.get(
    "/{address_id}",
    response_model=AddressInDB,
    summary="Busca um endereço por ID",
    description="Endpoint para buscar um endereço específico pelo seu ID.",
    response_description="Retorna os detalhes do endereço encontrado."
)
def read_address(address_id: int, db: Session = Depends(get_db)):
    """
    Busca um endereço pelo seu ID.

    - **address_id**: ID do endereço a ser buscado.

    Se o endereço não for encontrado, retorna um erro 404.
    """
    db_address = get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_address

@router.get(
    "/",
    response_model=list[AddressInDB],
    summary="Lista todos os endereços",
    description="Endpoint para listar todos os endereços cadastrados no sistema. "
                "Permite paginação usando os parâmetros `skip` e `limit`.",
    response_description="Retorna uma lista de endereços."
)
def read_all_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos os endereços cadastrados.

    - **skip**: Número de registros a serem ignorados (para paginação).
    - **limit**: Número máximo de registros a serem retornados (para paginação).

    Retorna uma lista de endereços.
    """
    return get_all_addresses(db, skip=skip, limit=limit)

@router.put(
    "/{address_id}",
    response_model=AddressInDB,
    summary="Atualiza um endereço existente",
    description="Endpoint para atualizar os dados de um endereço existente. "
                "Apenas os campos fornecidos serão atualizados.",
    response_description="Retorna os detalhes do endereço atualizado."
)
def update_existing_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um endereço existente.

    - **address_id**: ID do endereço a ser atualizado.
    - **address**: Dados do endereço a serem atualizados (apenas os campos fornecidos).

    Se o endereço não for encontrado, retorna um erro 404.
    """
    db_address = update_address(db=db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_address

@router.delete(
    "/{address_id}",
    response_model=dict,
    summary="Exclui um endereço existente",
    description="Endpoint para excluir um endereço existente pelo seu ID.",
    response_description="Retorna uma mensagem de confirmação."
)
def delete_existing_address(address_id: int, db: Session = Depends(get_db)):
    """
    Exclui um endereço existente.

    - **address_id**: ID do endereço a ser excluído.

    Se o endereço não for encontrado, retorna um erro 404.
    Retorna uma mensagem de confirmação da exclusão.
    """
    db_address = delete_address(db=db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": "Endereço excluído com sucesso"}