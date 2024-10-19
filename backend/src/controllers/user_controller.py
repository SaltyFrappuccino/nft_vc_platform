from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from ..models.user import User
from datetime import datetime, timedelta
import jwt
from ..config import Config


def register():
    data = request.get_json()
    email = data.get('email')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User with this email already exists.'}), 400

    new_user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=email,
        password=generate_password_hash(data.get('password')),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, Config.SECRET_KEY)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@user_blueprint.route('/link-wallet', methods=['POST'])
def link_wallet():
    data = request.json
    user_id = data['user_id']
    user = User.query.get(user_id)
    if user:
        user.wallet_address = data['wallet_address']
        db.session.commit()
        return jsonify({'message': 'Wallet linked successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

@user_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        new_password = generate_password_hash('newpassword123', method='sha256')
        user.password = new_password
        db.session.commit()
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'message': 'User not found'}), 404