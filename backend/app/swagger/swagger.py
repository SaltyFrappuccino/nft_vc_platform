from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/swagger/swagger.yaml'  # URL для доступа к swagger.yaml через ваш Flask сервер

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "NFT VC Platform"
    }
)
