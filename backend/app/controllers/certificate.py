from flask import request, jsonify
from web3 import Web3
from ..models.certificate import Certificate, NFTToken, db
from ..models.user import User

w3 = Web3(Web3.HTTPProvider('https://polygon-amoy.public.blastapi.io'))


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

    contract_address = 'YOUR_CONTRACT_ADDRESS'  # адрес  контракта
    abi = 'YOUR_ABI'  # ABI  контракта

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
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    nft_token = NFTToken.query.filter_by(certificate_id=certificate.id).first()
    if nft_token and nft_token.token_hash:
        abi = nft_token.abi
        token_address = Web3.to_checksum_address(nft_token.token_hash)

        contract = w3.eth.contract(address=token_address, abi=abi)

        user = User.query.get(certificate.owner_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404

        try:
            tx = contract.functions.revoke(user.nft_wallet_address).buildTransaction({
                'chainId': 80001,
                'gas': 70000,
                'gasPrice': w3.to_wei('20', 'gwei'),
                'nonce': w3.eth.get_transaction_count(user.nft_wallet_address),
            })

            signed_tx = w3.eth.account.signTransaction(tx, private_key='Как передавать ключ пока не придумал, '
                                                                       'мб брать отюзеров, но тогда его нужно сейвить'
                                                                       ' по хитрому в БД.')
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            return jsonify({'message': 'Сертификат отозван. TX Hash: ' + tx_hash.hex()}), 200
        except Exception as e:
            return jsonify({'error': 'Ошибка отзыва NFT', 'details': str(e)}), 400
    else:
        return jsonify({'error': 'NFT не найден'}), 404


def transfer_certificate(id):
    certificate = Certificate.query.get(id)
    if not certificate:
        return jsonify({'error': 'Сертификат не найден'}), 404

    to_user_id = request.json.get('to_user_id')
    to_user = User.query.get(to_user_id)

    if not to_user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    nft_token = NFTToken.query.filter_by(certificate_id=certificate.id).first()
    if nft_token and nft_token.token_hash:
        abi = nft_token.abi
        token_address = Web3.to_checksum_address(nft_token.token_hash)

        contract = w3.eth.contract(address=token_address, abi=abi)

        try:
            tx = contract.functions.transfer(to_user.nft_wallet_address).buildTransaction({
                'chainId': 80001,
                'gas': 70000,
                'gasPrice': w3.to_wei('20', 'gwei'),
                'nonce': w3.eth.get_transaction_count(certificate.owner.nft_wallet_address),
            })

            signed_tx = w3.eth.account.signTransaction(tx, private_key='Как передавать ключ пока не придумал, '
                                                                       'мб брать отюзеров, но тогда его нужно сейвить'
                                                                       ' по хитрому в БД.')
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            certificate.owner_id = to_user.id
            db.session.commit()

            return jsonify({'message': 'Сертификат успешно передан. TX Hash: ' + tx_hash.hex()}), 200
        except Exception as e:
            return jsonify({'error': 'Ошибка передачи NFT', 'details': str(e)}), 400
    else:
        return jsonify({'error': 'NFT не найден'}), 404


def get_certificate_after_course():
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
