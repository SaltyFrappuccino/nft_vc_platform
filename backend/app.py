from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)
    migrate.init_app(app, db)

    swagger_url = '/api/docs'  # URL для доступа к Swagger UI
    api_url = '/static/swagger.yaml'  # Путь к файлу спецификации OpenAPI
    swagger_blueprint = get_swaggerui_blueprint(swagger_url, api_url)
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)

    from src.routes.user_routes import user_blueprint
    from src.routes.company_routes import company_blueprint
    from src.routes.certificate_routes import certificate_blueprint
    from src.routes.nft_routes import nft_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(company_blueprint, url_prefix='/company')
    app.register_blueprint(certificate_blueprint, url_prefix='/certificates')
    app.register_blueprint(nft_blueprint, url_prefix='/nft')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
