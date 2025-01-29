from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schema import *
from crud.orders import *

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "/",
    response_model=OrderInDB,
    summary="Cria um novo pedido",
    description="Endpoint para criar um novo pedido no sistema.",
    response_description="Retorna os detalhes do pedido criado."
)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Cria um novo pedido com base nos dados fornecidos.

    - **user_id**: ID do usuário que fez o pedido.
    - **supplier_id**: ID do fornecedor associado ao pedido.
    - **product_type**: Tipo de produto solicitado.
    - **quantity**: Quantidade do produto.

    Retorna os detalhes do pedido criado.
    """
    return create_order(db=db, order=order)

@router.get(
    "/{order_id}",
    response_model=OrderInDB,
    summary="Busca um pedido por ID",
    description="Endpoint para buscar um pedido específico pelo seu ID.",
    response_description="Retorna os detalhes do pedido encontrado."
)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Busca um pedido pelo seu ID.

    - **order_id**: ID do pedido a ser buscado.

    Se o pedido não for encontrado, retorna um erro 404.
    """
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return db_order

@router.get(
    "/",
    response_model=list[OrderInDB],
    summary="Lista todos os pedidos",
    description="Endpoint para listar todos os pedidos cadastrados no sistema. "
                "Permite paginação usando os parâmetros `skip` e `limit`.",
    response_description="Retorna uma lista de pedidos."
)
def read_all_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos os pedidos cadastrados.

    - **skip**: Número de registros a serem ignorados (para paginação).
    - **limit**: Número máximo de registros a serem retornados (para paginação).

    Retorna uma lista de pedidos.
    """
    orders = get_all_orders(db, skip=skip, limit=limit)
    return orders

@router.put(
    "/{order_id}",
    response_model=OrderInDB,
    summary="Atualiza um pedido existente",
    description="Endpoint para atualizar os dados de um pedido existente. "
                "Apenas os campos fornecidos serão atualizados.",
    response_description="Retorna os detalhes do pedido atualizado."
)
def update_existing_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um pedido existente.

    - **order_id**: ID do pedido a ser atualizado.
    - **order**: Dados do pedido a serem atualizados (apenas os campos fornecidos).

    Se o pedido não for encontrado, retorna um erro 404.
    """
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return update_order(db=db, order_id=order_id, order=order)

@router.delete(
    "/{order_id}",
    response_model=dict,
    summary="Exclui um pedido existente",
    description="Endpoint para excluir um pedido existente pelo seu ID.",
    response_description="Retorna uma mensagem de confirmação."
)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    """
    Exclui um pedido existente.

    - **order_id**: ID do pedido a ser excluído.

    Se o pedido não for encontrado, retorna um erro 404.
    Retorna uma mensagem de confirmação da exclusão.
    """
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    delete_order(db=db, order_id=order_id)
    return {"message": "Pedido excluído com sucesso"}