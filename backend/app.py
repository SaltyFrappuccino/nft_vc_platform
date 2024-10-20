from flask import Flask
from database import db
from app.routes.user import init_user_routes
from app.routes.company import init_company_routes
from app.routes.certificate import init_certificate_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

init_user_routes(app)
init_company_routes(app)
init_certificate_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
