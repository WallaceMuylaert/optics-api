from sqlalchemy.orm import Session
from models.model import Order
from schemas.schema import *

def create_order(db: Session, order: OrderCreate):
    db_order = Order(
        user_id=order.user_id,
        supplier_id=order.supplier_id,
        product_type=order.product_type,
        quantity=order.quantity,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        return None
    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order