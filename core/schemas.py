from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date

class ClienteSchema(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    tipo: str = Field(..., pattern="^(PF|PJ)$")
    cpf_cnpj: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

class PropostaSchema(BaseModel):
    cliente_id: int
    servico: str = Field(..., min_length=3)
    descricao: str
    valor: float = Field(..., gt=0)
    prazo: str
    data_vencimento: date

    @field_validator('data_vencimento', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v
