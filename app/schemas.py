from typing import Optional, List
from pydantic import BaseModel, Field


class FavoritoPath(BaseModel):
    id: int = Field(..., description="ID do restaurante favorito")


class FavoritoCreate(BaseModel):
    nome: str = Field(..., description="Nome do restaurante")
    endereco: Optional[str] = Field(None, description="Endereço do restaurante")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    categoria: Optional[str] = Field(None, description="Categoria/tipo de cozinha")
    nota_pessoal: Optional[int] = Field(None, ge=1, le=5, description="Nota pessoal de 1 a 5")
    comentario: Optional[str] = Field(None, description="Comentário livre")
    tags: Optional[List[str]] = Field(default_factory=list, description="Lista de tags")
    osm_id: Optional[str] = Field(None, description="ID do local no OpenStreetMap, se veio da descoberta")


class FavoritoUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    categoria: Optional[str] = None
    nota_pessoal: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = None
    tags: Optional[List[str]] = None

class DescobrirQuery(BaseModel):
    lat: float = Field(..., description="Latitude do centro da busca")
    lng: float = Field(..., description="Longitude do centro da busca")
    raio: int = Field(1000, ge=100, le=5000, description="Raio de busca em metros")