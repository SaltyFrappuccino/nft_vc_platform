from flask import Blueprint
from ..controllers.certificate_controller import upload_certificate

certificate_bp = Blueprint('certificate_bp', __name__)

certificate_bp.route('/certificates/upload', methods=['POST'])(upload_certificate)