from datetime import datetime
from app.database import db


class RestauranteFavorito(db.Model):
    __tablename__ = "restaurantes_favoritos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(60), nullable=True, index=True)
    nota_pessoal = db.Column(db.Integer, nullable=True) 
    comentario = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)  
    osm_id = db.Column(db.String(60), nullable=True)  
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "categoria": self.categoria,
            "nota_pessoal": self.nota_pessoal,
            "comentario": self.comentario,
            "tags": self.tags.split(",") if self.tags else [],
            "osm_id": self.osm_id,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
        }