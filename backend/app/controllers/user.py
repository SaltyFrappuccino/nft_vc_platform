from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User
from database import db


def register():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid data"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        first_name=data.get("firstName"),
        last_name=data.get("lastName"),
        email=data["email"],
        password=generate_password_hash(data["password"]),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


def login():
    """
    User login
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: "john.doe@example.com"
              password:
                type: string
                example: "strongpassword"
    responses:
      200:
        description: Login successful
      401:
        description: Invalid email or password
    """
    data = request.json
    user = User.query.filter_by(email=data.get("email")).first()
    if user and check_password_hash(user.password, data.get("password")):
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid email or password"}), 401


def reset_password():
    """
    Reset user password
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: "john.doe@example.com"
    responses:
      200:
        description: Instructions for password recovery have been sent
      404:
        description: User not found
    """
    data = request.json
    user = User.query.filter_by(email=data.get("email")).first()
    if user:
        # Логика для восстановления пароля
        return jsonify({"message": "Instructions for password recovery have been sent"}), 200

    return jsonify({"error": "User not found"}), 404


def get_all_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of users
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  first_name:
                    type: string
                    example: "John"
                  last_name:
                    type: string
                    example: "Doe"
                  email:
                    type: string
                    example: "john.doe@example.com"
    """
    users = User.query.all()
    user_list = [{"first_name": user.first_name, "last_name": user.last_name, "email": user.email} for user in users]
    return jsonify(user_list), 200


def link_wallet(user_id, nft_wallet_address):
    """
    Update user's NFT wallet address.
    :param user_id: ID of the user
    :param nft_wallet_address: New NFT wallet address to be saved
    :return: Response message
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.nft_wallet_address = nft_wallet_address
    db.session.commit()

    return jsonify({"message": "NFT wallet address updated successfully"}), 200
