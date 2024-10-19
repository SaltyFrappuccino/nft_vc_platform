from flask import Blueprint
from ..controllers.company_controller import register_company

company_bp = Blueprint('company_bp', __name__)

company_bp.route('/company/register', methods=['POST'])(register_company)
