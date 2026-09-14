from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS

from app.database import init_db
from app.routes import bp as favoritos_bp


def create_app():
    info = Info(
        title="Restaurantes Favoritos API",
        version="1.0.0",
        description="API para salvar restaurantes favoritos e descobrir novos.",
    )
    app = OpenAPI(__name__, info=info)
    CORS(app)

    init_db(app)
    app.register_api(favoritos_bp)

    return app