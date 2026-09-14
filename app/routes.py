from flask_openapi3 import APIBlueprint, Tag

import requests
from app.external_api import buscar_restaurantes_proximos
from app.schemas import DescobrirQuery
from app.database import db
from app.models import RestauranteFavorito
from app.schemas import FavoritoPath, FavoritoCreate, FavoritoUpdate

tag_favoritos = Tag(name="Favoritos", description="CRUD de restaurantes favoritos")

bp = APIBlueprint("favoritos", __name__, url_prefix="/api")


@bp.get("/favoritos", tags=[tag_favoritos], summary="Lista os restaurantes favoritos")
def listar_favoritos():
    favoritos = RestauranteFavorito.query.order_by(RestauranteFavorito.data_criacao.desc()).all()
    return {"resultados": [item.to_dict() for item in favoritos]}


@bp.get("/favoritos/<int:id>", tags=[tag_favoritos], summary="Detalha um favorito")
def obter_favorito(path: FavoritoPath):
    favorito = db.get_or_404(RestauranteFavorito, path.id)
    return favorito.to_dict()


@bp.post("/favoritos", tags=[tag_favoritos], summary="Adiciona um restaurante aos favoritos")
def criar_favorito(body: FavoritoCreate):
    favorito = RestauranteFavorito(
        nome=body.nome,
        endereco=body.endereco,
        latitude=body.latitude,
        longitude=body.longitude,
        categoria=body.categoria,
        nota_pessoal=body.nota_pessoal,
        comentario=body.comentario,
        tags=",".join(body.tags) if body.tags else None,
        osm_id=body.osm_id,
    )
    db.session.add(favorito)
    db.session.commit()
    return favorito.to_dict(), 201


@bp.put("/favoritos/<int:id>", tags=[tag_favoritos], summary="Atualiza um favorito")
def atualizar_favorito(path: FavoritoPath, body: FavoritoUpdate):
    favorito = db.get_or_404(RestauranteFavorito, path.id)

    dados = body.model_dump(exclude_unset=True)
    if "tags" in dados and dados["tags"] is not None:
        dados["tags"] = ",".join(dados["tags"])

    for campo, valor in dados.items():
        setattr(favorito, campo, valor)

    db.session.commit()
    return favorito.to_dict()


@bp.delete("/favoritos/<int:id>", tags=[tag_favoritos], summary="Remove um favorito")
def remover_favorito(path: FavoritoPath):
    favorito = db.get_or_404(RestauranteFavorito, path.id)
    db.session.delete(favorito)
    db.session.commit()
    return "", 204

tag_descoberta = Tag(name="Descoberta", description="Busca restaurantes via API externa (OpenStreetMap)")


@bp.get(
    "/descobrir",
    tags=[tag_descoberta],
    summary="Descobre restaurantes próximos via OpenStreetMap (Overpass API)",
)
def descobrir_restaurantes(query: DescobrirQuery):
    try:
        encontrados = buscar_restaurantes_proximos(query.lat, query.lng, query.raio)
    except requests.RequestException as erro:
        return {"erro": f"Falha ao consultar a API externa: {erro}"}, 502

    return {"total": len(encontrados), "resultados": encontrados}