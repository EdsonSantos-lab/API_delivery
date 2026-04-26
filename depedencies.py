from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oaut2_schema


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        sessao = Session()
        yield sessao
    finally:
        sessao.close()



def verificar_token(token : str = Depends(oaut2_schema), session : Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access inválido, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()  
    if not usuario:
        raise HTTPException(status_code=401, detail="Access inválido")

    return usuario
    