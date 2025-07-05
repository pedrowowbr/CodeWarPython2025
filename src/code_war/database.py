from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from code_war.settings import Settings

# Criação do engine a partir da URL do banco
engine = create_engine(
    Settings().DATABASE_URL, connect_args={'check_same_thread': False}
)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função que fornece a sessão para ser usada com Depends


def get_session():  # pragma: no cover
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
