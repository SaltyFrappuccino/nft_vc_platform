from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from app.routes.certificate import init_certificate_routes
from app.routes.company import init_company_routes
from app.routes.user import init_user_routes
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

init_user_routes(app)
init_company_routes(app)
init_certificate_routes(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "NFT VC Platform",
        "description": "API documentation",
        "version": "1.0.0"
    }})

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
