from flask import request, jsonify
from web3 import Web3

from ..models import Certificate, NFTToken, User
from database import  db
w3 = Web3(Web3.HTTPProvider('https://polygon-amoy.public.blastapi.io'))


def upload_certificate():
    """
    Upload a new certificate
    ---
    tags:
      - Certificates
    responses:
      201:
        description: Certificate uploaded successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Сертификат успешно загружен"
      400:
        description: Error uploading certificate
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Ошибка загрузки сертификата"
    """
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
    """
    Convert a certificate to NFT
    ---
    tags:
      - Certificates
    parameters:
      - name: id
        in: path
        required: true
        description: The ID of the certificate to convert
        schema:
          type: integer
    responses:
      200:
        description: Certificate successfully converted to NFT
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Сертификат успешно преобразован в NFT"
                transaction_hash:
                  type: string
                  example: "0x123abc..."
      404:
        description: Certificate or user not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Сертификат не найден"
      400:
        description: Error converting to NFT
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Ошибка преобразования в NFT"
    """
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    contract_address = 'YOUR_CONTRACT_ADDRESS'  # адрес контракта
    abi = 'YOUR_ABI'  # ABI контракта

    contract = w3.eth.contract(address=contract_address, abi=abi)

    user = User.query.get(certificate.owner_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    try:
        tx = contract.functions.createNFT(user.nft_wallet_address, certificate.name).buildTransaction({
            'chainId': 80001,
            'gas': 70000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': w3.eth.get_transaction_count(user.nft_wallet_address),
        })

        signed_tx = w3.eth.account.signTransaction(tx, private_key='Пупые приватные ключи.')
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        nft_token = NFTToken(certificate_id=certificate.id, token_hash=generate_nft_hash(), abi=abi)
        certificate.type = 'NFT'

        db.session.add(nft_token)
        db.session.commit()

        return jsonify({'message': 'Сертификат успешно преобразован в NFT', 'transaction_hash': tx_hash.hex()}), 200
    except Exception as e:
        return jsonify({'error': 'Ошибка преобразования в NFT', 'details': str(e)}), 400


def revoke_certificate(id):
    """
    Revoke a certificate
    ---
    tags:
      - Certificates
    parameters:
      - name: id
        in: path
        required: true
        description: The ID of the certificate to revoke
        schema:
          type: integer
    responses:
      200:
        description: Certificate successfully revoked
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Сертификат отозван."
      404:
        description: Certificate not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Сертификат не найден"
      400:
        description: Error revoking certificate
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Ошибка отзыва сертификата"
    """
    # Получаем сертификат по ID
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    # Отзываем сертификат
    # Здесь можете добавить любую логику, связанную с отзывом (например, пометить как отозванный)
    # Например, если есть поле revoked в таблице, то:
    # certificate.revoked = True
    # db.session.commit()

    db.session.delete(certificate)  # Пример: удаление сертификата из базы данных
    db.session.commit()

    return jsonify({'message': 'Сертификат отозван.'}), 200


def transfer_certificate(id):
    """
    Transfer a certificate to another user
    ---
    tags:
      - Certificates
    parameters:
      - name: id
        in: path
        required: true
        description: The ID of the certificate to transfer
        schema:
          type: integer
      - name: to_user_id
        in: body
        required: true
        description: The ID of the user to transfer the certificate to
        schema:
          type: object
          properties:
            to_user_id:
              type: integer
              example: 2
    responses:
      200:
        description: Certificate successfully transferred
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Сертификат успешно передан."
      404:
        description: Certificate or user not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Пользователь не найден"
      400:
        description: Error transferring certificate
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Ошибка передачи сертификата"
    """
    # Получаем сертификат по ID
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    # Получаем ID пользователя, которому передаём сертификат
    to_user_id = request.json.get('to_user_id')
    to_user = User.query.get(to_user_id)

    if not to_user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    # Меняем владельца сертификата
    certificate.owner_id = to_user.id
    db.session.commit()

    return jsonify({'message': 'Сертификат успешно передан.'}), 200



def get_certificate_after_course():
    """
    Issue a certificate after course completion
    ---
    tags:
      - Certificates
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id:
                type: integer
                example: 1
    responses:
      200:
        description: Certificate successfully issued
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Сертификат успешно выдан"
      400:
        description: Error issuing certificate
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Ошибка выдачи сертификата"
    """
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
