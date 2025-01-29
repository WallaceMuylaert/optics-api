from sqlalchemy.orm import Session
from models.model import Address, Supplier
from schemas.schema import *

def create_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(
        name=supplier.name,
        email=supplier.email,
        cnpj=supplier.cnpj,
        phone=supplier.phone
    )
    db_supplier.set_password(supplier.password)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_all_suppliers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Supplier).offset(skip).limit(limit).all()

def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate):
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        return None
    for key, value in supplier.model_dump(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    db_supplier = get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        return None
    db.delete(db_supplier)
    db.commit()
    return db_supplier