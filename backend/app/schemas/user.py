from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    nome: str
    ativo: bool  # "cliente" ou "tatuador"


class UserCreate(UserBase):
    senha: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode=True no Pydantic v2


# ✅ Modelo de resposta usado nas rotas
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
