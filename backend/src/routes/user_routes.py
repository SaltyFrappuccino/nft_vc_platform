from flask import Blueprint
from ..controllers.user_controller import register_user, login_user

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/user/register', methods=['POST'])(register_user)
user_bp.route('/user/login', methods=['POST'])(login_user)
