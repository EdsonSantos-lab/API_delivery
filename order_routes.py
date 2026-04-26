from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema    
from typing import List
from depedencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])       

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session=Depends(pegar_sessao)):

    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem":f"Pedido criado com sucesso para o usuário {novo_pedido.usuario}"}
  
@order_router.post("/pedido/canselar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session=Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):

    # USIARIO ADM = TRUE
    # ID PEDIDO EXISTE = ID PEDIDO EXISTE

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if  not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar esse pedido")
    
    pedido.status = "CANCELADO"
    session.commit()

    return {
        "mensagem": f"Pedido {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session=Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):

    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar essa rota")
    else:
        pedidos = session.query(Pedido).all()
    return {
        "pedidos": pedidos
    }

@order_router.post("/pedido/adicionar_item/{id_usuario}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema,
                                usuario : Usuario = Depends(verificar_token),
                                session: Session=Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if  not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens nesse pedido")
    
    # criar o item do pedido
    item_pedido = ItemPedido(quantidade=item_pedido_schema.quantidade,
                            sabor=item_pedido_schema.sabor,
                            tamanho=item_pedido_schema.tamanho,
                            preco_unitario=item_pedido_schema.preco_unitario,
                            pedido=id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem": f"Item adicionado com sucesso ao pedido {pedido.id}",
        "item_pedido": item_pedido.id,
        "preco_total_pedido": pedido.preco
    }


@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                              usuario : Usuario = Depends(verificar_token),
                              session: Session=Depends(pegar_sessao)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado")
    
    if  not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover itens desse pedido")
   
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item do pedido {item_pedido.id} removido com sucesso",
        "preco_total_pedido": item_pedido
    }


@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int,
                           usuario : Usuario = Depends(verificar_token),
                           session: Session=Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if  not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para finalizar esse pedido")
   
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }


@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int,
                            session: Session=Depends(pegar_sessao),
                            usuario : Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if  not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para visualizar esse pedido")
    return {
        "pedido": pedido
    }


@order_router.get("/listar/pedidos/usuario, response_model=List[ResponsePedidoSchema]")
async def listar_pedidos(session: Session=Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return {
        "pedidos": pedidos
    }