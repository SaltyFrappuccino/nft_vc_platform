from .user_routes import user_bp
from .company_routes import company_bp
from .certificate_routes import certificate_bp
from .nft_routes import nft_bp

def init_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(certificate_bp)
    app.register_blueprint(nft_bp)
