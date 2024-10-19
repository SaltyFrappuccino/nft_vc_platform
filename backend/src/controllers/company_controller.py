from flask import Blueprint, request, jsonify
from ..models.company import Company
from datetime import datetime, timedelta
import jwt
from functools import wraps
from ..config import Config

company_blueprint = Blueprint('company', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            company_id = data['company_id']
            access_key = CompanyAccessKey.query.filter_by(company_id=company_id).first()
            if access_key.expires_at < datetime.utcnow():
                return jsonify({'message': 'Access key expired'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

@company_blueprint.route('/register', methods=['POST'])
def register_company():
    data = request.json
    new_company = Company(name=data['name'], address=data['address'])
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company registered successfully'}), 201

# Получение ключа доступа компании
@company_blueprint.route('/<int:id>/access-key', methods=['GET'])
def generate_access_key(id):
    company = Company.query.get(id)
    if company:
        key = jwt.encode({'company_id': company.id, 'exp': datetime.utcnow() + timedelta(days=30)}, Config.SECRET_KEY)
        new_access_key = CompanyAccessKey(company_id=company.id, access_key=key, expires_at=datetime.utcnow() + timedelta(days=30))
        db.session.add(new_access_key)
        db.session.commit()
        return jsonify({'access_key': key}), 200
    return jsonify({'message': 'Company not found'}), 404
