import logging
from http import HTTPStatus

import requests
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

# Configuração do logger
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(f'Erro de validação: {exc.errors()}')
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={'status': 'Erro de validação', 'errors': exc.errors()},
    )


def format_response(data: dict, request: Request, status_code: int = 200):
    accept = request.headers.get('accept', 'application/json').lower()
    json_data = jsonable_encoder(data)

    if 'application/xml' in accept:
        xml = dicttoxml(json_data, custom_root='response', attr_type=False)
        return Response(
            content=xml, media_type='application/xml', status_code=status_code
        )

    return JSONResponse(content=json_data, status_code=status_code)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    logger.info("Endpoint raiz '/' acessado.")
    return {'message': 'API de filmes do Studio Ghibli'}


@app.post(
    '/filmes/', status_code=HTTPStatus.CREATED, response_model=FilmePublic
)
def create_filme(filme: FilmeCreate, session: Session = Depends(get_session)):
    db_filme = Filme(**filme.dict())
    session.add(db_filme)
    session.commit()
    session.refresh(db_filme)
    logger.info(f'Filme criado: {db_filme.titulo}')
    return FilmePublic.model_validate(db_filme)


@app.get('/filmes/', response_model=FilmeList)
def read_filmes(
    request: Request,
    limit: int = Query(default=10),
    skip: int = Query(default=0),
    session: Session = Depends(get_session),
):
    filmes = session.scalars(select(Filme).offset(skip).limit(limit)).all()
    filmes_public = [
        FilmePublic.model_validate(f).model_dump() for f in filmes
    ]
    logger.info(
        f'{len(filmes)} filmes recuperados (limit={limit}, skip={skip})'
    )
    return format_response({'filmes': filmes_public}, request)


@app.get('/filmes/{filme_id}', response_model=FilmePublic)
def read_filme(
    filme_id: int, request: Request, session: Session = Depends(get_session)
):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        logger.warning(f'Filme não encontrado: ID {filme_id}')
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    logger.info(f'Filme recuperado: ID {filme_id}')
    return format_response(
        jsonable_encoder(FilmePublic.model_validate(db_filme)), request
    )


@app.put('/filmes/{filme_id}', response_model=FilmePublic)
def update_filme(
    filme_id: int, filme: FilmeUpdate, session: Session = Depends(get_session)
):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        logger.warning(
            f'Tentativa de atualizar filme inexistente: ID {filme_id}'
        )
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    update_data = filme.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_filme, key, value)

    session.commit()
    session.refresh(db_filme)
    logger.info(f'Filme atualizado: ID {filme_id}')
    return FilmePublic.model_validate(db_filme)


@app.delete('/filmes/{filme_id}', response_model=Message)
def delete_filme(filme_id: int, session: Session = Depends(get_session)):
    db_filme = session.get(Filme, filme_id)
    if not db_filme:
        logger.warning(
            f'Tentativa de deletar filme inexistente: ID {filme_id}'
        )
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    db_filme.data_exclusao = (
        db_filme.data_exclusao
        or db_filme.data_edicao
        or db_filme.data_inclusao
    )
    session.delete(db_filme)
    session.commit()
    logger.info(f'Filme deletado: ID {filme_id}')
    return {'message': 'Filme excluído com sucesso'}

@app.post('/etl/ghibli', response_model=Message)
def etl_ghibli(session: Session = Depends(get_session)):
    url = 'https://ghibliapi.vercel.app/films/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        filmes = response.json()

        inseridos = 0
        for filme in filmes:
            novo_filme = Filme(
                titulo=filme['title'],
                titulo_original=filme['original_title'],
                titulo_romanizado=filme['original_title_romanised'],
                descricao=filme['description'],
                diretor=filme['director'],
                produtor=filme['producer'],
                data_lancamento=filme['release_date'],
                duracao_min=filme['running_time'],
                pontuacao_rotten_tomatoes=filme['rt_score'],
            )
            session.add(novo_filme)
            inseridos += 1

        session.commit()
        logger.info(f'ETL concluído: {inseridos} filmes inseridos.')
        return {'message': f'{inseridos} filmes inseridos com sucesso'}

    except requests.RequestException as e:
        logger.error(f'Erro na requisição à API do Ghibli: {e}')
        raise HTTPException(
            status_code=HTTPStatus.BAD_GATEWAY,
            detail='Erro ao extrair dados da API pública.',
        )
