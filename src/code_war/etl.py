import logging
import requests
from code_war.models import Filme

logger = logging.getLogger(__name__)


def extract_filmes():
    url = 'https://ghibliapi.vercel.app/films/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f'Erro ao extrair dados da API Ghibli: {e}')
        raise

def transform_filmes(data):
    filmes = []
    for item in data:
        filmes.append({
            'titulo': item['title'],
            'titulo_original': item['original_title'],
            'titulo_romanizado': item['original_title_romanised'],
            'descricao': item['description'],
            'diretor': item['director'],
            'produtor': item['producer'],
            'data_lancamento': item['release_date'],
            'duracao_min': item['running_time'],
            'pontuacao_rotten_tomatoes': item['rt_score'],
        })
    return filmes

def load_filmes(filmes, session):
    inseridos = 0
    for filme in filmes:
        novo_filme = Filme(**filme)
        session.add(novo_filme)
        inseridos += 1
    session.commit()
    logger.info(f'{inseridos} filmes inseridos com sucesso.')
    return inseridos
