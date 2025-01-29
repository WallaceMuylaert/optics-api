from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_type: str  # "user" ou "supplier"
    
# Esquemas para User
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    cpf: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Esquemas para Supplier
class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    cnpj: str
    phone: Optional[str] = None

class SupplierCreate(SupplierBase):
    password: str

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class SupplierInDB(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Esquemas para Order
class OrderBase(BaseModel):
    product_type: str
    quantity: int
    status: str

class OrderCreate(OrderBase):
    user_id: int
    supplier_id: int

class OrderUpdate(BaseModel):
    product_type: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None

class OrderInDB(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AddressBase(BaseModel):
    cep: str
    street: str
    complement: Optional[str] = None
    state: str
    number: str

class AddressCreate(AddressBase):
    user_id: Optional[int] = None
    supplier_id: Optional[int] = None

class AddressUpdate(BaseModel):
    cep: Optional[str] = None
    street: Optional[str] = None
    complement: Optional[str] = None
    state: Optional[str] = None
    number: Optional[str] = None
    user_id: Optional[int] = None
    supplier_id: Optional[int] = None

class AddressInDB(AddressBase):
    id: int
    user_id: Optional[int] = None
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True