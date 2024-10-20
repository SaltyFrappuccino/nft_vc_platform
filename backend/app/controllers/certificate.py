from flask import request, jsonify

from ..models.certificate import Certificate, NFTToken, db
from ..models.user import User


def upload_certificate():
    data = request.get_json()
    try:
        certificate = Certificate(
            name=data['name'],
            issuer=data['issuer'],
            issued_date=data.get('issuedDate', None),
            owner_id=data['owner']['id']
        )
        db.session.add(certificate)
        db.session.commit()
        return jsonify({'message': 'Сертификат успешно загружен'}), 201
    except Exception as e:
        return jsonify({'error': 'Ошибка загрузки сертификата', 'details': str(e)}), 400


def convert_to_nft(id):
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    nft_token = NFTToken(certificate_id=certificate.id, token_hash=generate_nft_hash())
    certificate.type = 'NFT'

    try:
        db.session.add(nft_token)
        db.session.commit()
        return jsonify({'message': 'Сертификат успешно преобразован в NFT'}), 200
    except Exception as e:
        return jsonify({'error': 'Ошибка преобразования в NFT', 'details': str(e)}), 400


def revoke_certificate(id):
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    try:
        reason = request.json.get('reason')
        db.session.delete(certificate)
        db.session.commit()
        return jsonify({'message': f'Сертификат отозван. Причина: {reason}'}), 200
    except Exception as e:
        return jsonify({'error': 'Ошибка отзыва сертификата', 'details': str(e)}), 400


def transfer_certificate(id):
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    to_user_id = request.json.get('to_user_id')
    to_user = User.query.get(to_user_id)

    if not to_user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    try:
        certificate.owner_id = to_user.id
        db.session.commit()
        return jsonify({'message': 'Сертификат успешно передан'}), 200
    except Exception as e:
        return jsonify({'error': 'Ошибка передачи сертификата', 'details': str(e)}), 400


def get_certificate_after_course(id):
    data = request.get_json()
    user_id = data['user_id']

    try:
        certificate = Certificate(
            name="Course Completion",
            issuer="Course Platform",
            owner_id=user_id
        )
        db.session.add(certificate)
        db.session.commit()
        return jsonify({'message': 'Сертификат успешно выдан'}), 200
    except Exception as e:
        return jsonify({'error': 'Ошибка выдачи сертификата', 'details': str(e)}), 400


def generate_nft_hash():
    import hashlib, time
    return hashlib.sha256(str(time.time()).encode()).hexdigest()
