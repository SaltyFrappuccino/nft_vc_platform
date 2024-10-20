from flask import Flask
from app.controllers.user import register, login, link_wallet, reset_password, get_all_users


def init_user_routes(app: Flask):
    app.route("/user/register", methods=['POST'])(register)
    app.route("/user/login", methods=['POST'])(login)
    app.route("/user/link-wallet", methods=['POST'])(link_wallet)
    app.route("/user/reset-password", methods=['POST'])(reset_password)
    app.route("/users", methods=['GET'])(get_all_users)
