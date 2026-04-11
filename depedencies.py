from sqlalchemy.orm import sessionmaker
from models import db

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        sessao = Session()
        yield sessao
    finally:
        sessao.close()