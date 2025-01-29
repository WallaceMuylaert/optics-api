from sqlalchemy.orm import Session
from models.model import Address
from schemas.schema import AddressCreate, AddressUpdate

def create_address(db: Session, address: AddressCreate):
    db_address = Address(
        cep=address.cep,
        street=address.street,
        complement=address.complement,
        state=address.state,
        number=address.number,
        user_id=address.user_id,
        supplier_id=address.supplier_id
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def get_all_addresses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Address).offset(skip).limit(limit).all()

def update_address(db: Session, address_id: int, address: AddressUpdate):
    db_address = get_address(db, address_id=address_id)
    if db_address is None:
        return None
    for key, value in address.model_dump(exclude_unset=True).items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id=address_id)
    if db_address is None:
        return None
    db.delete(db_address)
    db.commit()
    return db_address