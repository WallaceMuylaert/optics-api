from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schema import *
from crud.suppliers import *

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post(
    "/",
    response_model=SupplierInDB,
    summary="Cria um novo fornecedor",
    description="Endpoint para criar um novo fornecedor no sistema. "
                "Verifica se o CNPJ ou e-mail já está registrado antes de criar o fornecedor.",
    response_description="Retorna os detalhes do fornecedor criado."
)
def create_new_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """
    Cria um novo fornecedor com base nos dados fornecidos.

    - **name**: Nome do fornecedor.
    - **email**: E-mail do fornecedor (deve ser único).
    - **cnpj**: CNPJ do fornecedor (deve ser único).
    - **phone**: Número de telefone do fornecedor (opcional).
    - **password**: Senha do fornecedor (será hasheada antes de ser armazenada).

    Se o CNPJ ou e-mail já estiver registrado, retorna um erro 400.
    """
    db_supplier = db.query(Supplier).filter(
        (Supplier.cnpj == supplier.cnpj) | (Supplier.email == supplier.email)
    ).first()
    
    if db_supplier:
        raise HTTPException(status_code=400, detail="Fornecedor com este CNPJ ou e-mail já registrado")
    
    return create_supplier(db=db, supplier=supplier)

@router.get(
    "/{supplier_id}",
    response_model=SupplierInDB,
    summary="Busca um fornecedor por ID",
    description="Endpoint para buscar um fornecedor específico pelo seu ID.",
    response_description="Retorna os detalhes do fornecedor encontrado."
)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """
    Busca um fornecedor pelo seu ID.

    - **supplier_id**: ID do fornecedor a ser buscado.

    Se o fornecedor não for encontrado, retorna um erro 404.
    """
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return db_supplier

@router.get(
    "/",
    response_model=list[SupplierInDB],
    summary="Lista todos os fornecedores",
    description="Endpoint para listar todos os fornecedores cadastrados no sistema. "
                "Permite paginação usando os parâmetros `skip` e `limit`.",
    response_description="Retorna uma lista de fornecedores."
)
def read_all_suppliers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos os fornecedores cadastrados.

    - **skip**: Número de registros a serem ignorados (para paginação).
    - **limit**: Número máximo de registros a serem retornados (para paginação).

    Retorna uma lista de fornecedores.
    """
    suppliers = get_all_suppliers(db, skip=skip, limit=limit)
    return suppliers

@router.put(
    "/{supplier_id}",
    response_model=SupplierInDB,
    summary="Atualiza um fornecedor existente",
    description="Endpoint para atualizar os dados de um fornecedor existente. "
                "Apenas os campos fornecidos serão atualizados.",
    response_description="Retorna os detalhes do fornecedor atualizado."
)
def update_existing_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um fornecedor existente.

    - **supplier_id**: ID do fornecedor a ser atualizado.
    - **supplier**: Dados do fornecedor a serem atualizados (apenas os campos fornecidos).

    Se o fornecedor não for encontrado, retorna um erro 404.
    """
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return update_supplier(db=db, supplier_id=supplier_id, supplier=supplier)

@router.delete(
    "/{supplier_id}",
    response_model=dict,
    summary="Exclui um fornecedor existente",
    description="Endpoint para excluir um fornecedor existente pelo seu ID.",
    response_description="Retorna uma mensagem de confirmação."
)
def delete_existing_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """
    Exclui um fornecedor existente.

    - **supplier_id**: ID do fornecedor a ser excluído.

    Se o fornecedor não for encontrado, retorna um erro 404.
    Retorna uma mensagem de confirmação da exclusão.
    """
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    delete_supplier(db=db, supplier_id=supplier_id)
    return {"message": "Fornecedor excluído com sucesso"}