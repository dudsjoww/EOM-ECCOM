from pydantic import BaseModel
from typing import Optional


# Schema para login
class SchemaLogin(BaseModel):
    username: str
    password: str


# Schema para resposta de token
class SchemaTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Schema para refresh token
class SchemaRefreshToken(BaseModel):
    refresh_token: str


# Schema para resposta de refresh token
class SchemaRefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
