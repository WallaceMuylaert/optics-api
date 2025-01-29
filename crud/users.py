from sqlalchemy.orm import Session
from models.model import Address, User
from schemas.schema import *

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        cpf=user.cpf
    )
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.assign_default_role(db)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        return None
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user