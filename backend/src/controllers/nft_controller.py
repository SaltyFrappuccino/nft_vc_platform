from flask import jsonify
from ..models.certificate import Certificate
from .. import db

def convert_to_nft(id):
    certificate = Certificate.query.get(id)
    if certificate:
        certificate.type = 'NFT'
        db.session.commit()
        return jsonify({"message": f"Certificate {id} converted to NFT"}), 200
    return jsonify({"message": "Certificate not found"}), 404