import logging
import os
import requests
from dotenv import load_dotenv
from code_war.models import Filme

logger = logging.getLogger(__name__)
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def get_genre_mapping():
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": "pt-BR"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {genre["id"]: genre["name"] for genre in data["genres"]}
    except Exception as e:
        logger.error(f"Erro ao obter gêneros: {e}")
        return {}


def extract_filmes():
    filmes = []
    base_url = "https://api.themoviedb.org/3/movie/top_rated"

    if not TMDB_API_KEY:
        logger.error("TMDB_API_KEY não encontrada. Verifique o arquivo .env.")
        return filmes

    for page in range(1, 6):
        params = {
            "api_key": TMDB_API_KEY,
            "language": "pt-BR",
            "sort_by": "popularity.desc",
            "page": page,
        }

        try:
            response = requests.get(base_url, params=params)
            logger.info(f"Requisição para: {response.url}")
            response.raise_for_status()
            data = response.json()
            filmes.extend(data.get("results", []))
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar página {page}: {e}")
            logger.error(f"Resposta da API: {response.text}")
            break

    logger.info(f"{len(filmes)} filmes extraídos ao todo.")
    return filmes


def transform_filmes(data):
    filmes = []
    genre_map = get_genre_mapping()

    for item in data:
        generos = [genre_map.get(gid, "Desconhecido")
                   for gid in item.get("genre_ids", [])]

        filmes.append({
            "titulo": item.get("title", ""),
            "titulo_original": item.get("original_title", ""),
            "idioma_original": item.get("original_language", ""),
            "descricao": item.get("overview", ""),
            "data_lancamento": item.get("release_date", ""),
            "popularidade": item.get("popularity", 0.0),
            "media_votos": item.get("vote_average", 0.0),
            "quantidade_votos": item.get("vote_count", 0),
            "poster": item.get("poster_path", ""),
            "backdrop": item.get("backdrop_path", ""),
            "adulto": item.get("adult", False),
            "generos": ", ".join(generos),
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
