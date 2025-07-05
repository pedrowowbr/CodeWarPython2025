from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class FilmeBase(BaseModel):
    titulo: str
    titulo_original: str
    titulo_romanizado: str
    descricao: str
    diretor: str
    produtor: str
    data_lancamento: str
    duracao_min: str
    pontuacao_rotten_tomatoes: str


class FilmeCreate(FilmeBase):
    pass


class FilmeUpdate(BaseModel):
    titulo: Optional[str] = None
    titulo_original: Optional[str] = None
    titulo_romanizado: Optional[str] = None
    descricao: Optional[str] = None
    diretor: Optional[str] = None
    produtor: Optional[str] = None
    data_lancamento: Optional[str] = None
    duracao_min: Optional[str] = None
    pontuacao_rotten_tomatoes: Optional[str] = None


class FilmePublic(FilmeBase):
    id: int
    data_inclusao: Optional[datetime] = None
    data_edicao: Optional[datetime] = None
    data_exclusao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FilmeList(BaseModel):
    filmes: list[FilmePublic]
