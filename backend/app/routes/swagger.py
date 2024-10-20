from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/swagger/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "NFT VC Platform"
    }
)

swagger_routes = Blueprint('swagger_routes', __name__)
swagger_routes.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
