from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class FilmeBase(BaseModel):
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str
    data_lancamento: str
    popularidade: float
    media_votos: float
    quantidade_votos: int
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    adulto: bool
    generos: str


class FilmeCreate(FilmeBase):
    pass


class FilmeUpdate(BaseModel):
    titulo: str
    titulo_original: str
    idioma_original: str
    descricao: str
    data_lancamento: str
    popularidade: float
    media_votos: float
    quantidade_votos: int
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    adulto: bool
    generos: str


class FilmePublic(FilmeBase):
    id: int
    data_inclusao: datetime
    data_edicao: Optional[datetime] = None
    data_exclusao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FilmeList(BaseModel):
    filmes: list[FilmePublic]
