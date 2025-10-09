from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    nome: str
    ativo: bool  # "cliente" ou "tatuador"

class UserCreate(UserBase):
    senha_hash: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode=True no Pydantic v2

# ✅ Modelo de resposta usado nas rotas
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
