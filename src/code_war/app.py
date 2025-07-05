from http import HTTPStatus

from dicttoxml import dicttoxml
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from code_war.database import engine, get_session
from code_war.models import Base, Filme
from code_war.schemas import (
    FilmeCreate,
    FilmeList,
    FilmePublic,
    FilmeUpdate,
    Message,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={'status': 'Erro de validação', 'errors': exc.errors()},
    )


def format_response(data: dict, request: Request, status_code: int = 200):
    accept = request.headers.get("accept", "application/json").lower()
    json_data = jsonable_encoder(data)

    if "application/xml" in accept:
        xml = dicttoxml(json_data, custom_root='response', attr_type=False)
        return Response(content=xml, media_type="application/xml", status_code=status_code)

    return JSONResponse(content=json_data, status_code=status_code)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'API de filmes do Studio Ghibli'}


@app.post(
    '/filmes/', status_code=HTTPStatus.CREATED, response_model=FilmePublic
)
def create_filme(filme: FilmeCreate, session: Session = Depends(get_session)):
    db_filme = Filme(**filme.dict())
    session.add(db_filme)
    session.commit()
    session.refresh(db_filme)
    return FilmePublic.model_validate(db_filme)


@app.get('/filmes/', response_model=FilmeList)
def read_filmes(
    request: Request,
    limit: int = Query(default=10),
    skip: int = Query(default=0),
    session: Session = Depends(get_session),
):
    filmes = session.scalars(select(Filme).offset(skip).limit(limit)).all()
    # Converta cada filme para o schema Pydantic
    filmes_public = [
        FilmePublic.model_validate(f).model_dump() for f in filmes
    ]
    return format_response({'filmes': filmes_public}, request)


@app.get('/filmes/{filme_id}', response_model=FilmePublic)
def read_filme(
    filme_id: int, request: Request, session: Session = Depends(get_session)
):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    return format_response(
        jsonable_encoder(FilmePublic.model_validate(db_filme)), request
    )


@app.put('/filmes/{filme_id}', response_model=FilmePublic)
def update_filme(
    filme_id: int, filme: FilmeUpdate, session: Session = Depends(get_session)
):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    update_data = filme.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_filme, key, value)

    session.commit()
    session.refresh(db_filme)
    return FilmePublic.model_validate(db_filme)


@app.delete('/filmes/{filme_id}', response_model=Message)
def delete_filme(filme_id: int, session: Session = Depends(get_session)):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    db_filme.data_exclusao = (
        db_filme.data_exclusao
        or db_filme.data_edicao
        or db_filme.data_inclusao
    )
    session.delete(db_filme)
    session.commit()
    return {'message': 'Filme excluído com sucesso'}
