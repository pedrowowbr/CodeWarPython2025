from fastapi.testclient import TestClient

from code_war.app import app

client = TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')
    assert response.json() == {'message': 'Olá, mundo!'}
