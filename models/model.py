from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
from datetime import datetime
import bcrypt

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    cpf = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def assign_default_role(self, session):
        # Verifica se o papel "user" já existe
        default_role = session.query(Role).filter(Role.name == "user").first()
        if not default_role:
            # Se não existir, cria o papel "user"
            default_role = Role(name="user")
            session.add(default_role)
            session.commit()
        
        # Associa o papel "user" ao usuário
        user_role = UserRole(user_id=self.id, role_id=default_role.id)
        session.add(user_role)
        session.commit()

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    cnpj = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    
    orders = relationship("Order", back_populates="supplier", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="supplier", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    product_type = Column(String)
    quantity = Column(Integer)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="orders")
    supplier = relationship("Supplier", back_populates="orders")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String, nullable=False)
    street = Column(String, nullable=False)
    complement = Column(String, nullable=True)
    state = Column(String, nullable=False)
    number = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    user = relationship("User", back_populates="addresses")
    supplier = relationship("Supplier", back_populates="addresses")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # Ex: "admin", "user", "supplier"

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    user = relationship("User", back_populates="roles")
    role = relationship("Role")