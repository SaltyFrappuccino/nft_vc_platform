from flask import Blueprint
from ..controllers.nft_controller import convert_to_nft

nft_bp = Blueprint('nft_bp', __name__)

nft_bp.route('/certificates/<id>/convert-to-nft', methods=['POST'])(convert_to_nft)
