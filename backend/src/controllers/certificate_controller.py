from flask import request, jsonify
from ..models.certificate import Certificate
from .. import db
import uuid

def upload_certificate():
    data = request.get_json()
    new_certificate = Certificate(
        id=str(uuid.uuid4()),
        name=data['name'],
        issuer=data['issuer'],
        issued_date=data['issuedDate'],
        type=data['type'],
        owner_id=data['ownerId']
    )
    db.session.add(new_certificate)
    db.session.commit()
    return jsonify({"message": "Certificate uploaded successfully"}), 201
