from fastapi import FastAPI

app = FastAPI()


@app.get('/')  # Raiz do site
def read_root():
    return {'message': 'Olá, mundo!'}
