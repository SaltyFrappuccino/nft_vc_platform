from flask import Flask
from app.controllers.certificate import (
    upload_certificate,
    convert_to_nft,
    revoke_certificate,
    transfer_certificate,
    get_certificate_after_course
)


def init_certificate_routes(app: Flask):
    app.route("/certificates/upload", methods=['POST'])(upload_certificate)
    app.route("/certificates/<int:id>/convert-to-nft", methods=['POST'])(convert_to_nft)
    app.route("/certificates/<int:id>/revoke", methods=['POST'])(revoke_certificate)
    app.route("/certificates/<int:id>/transfer", methods=['POST'])(transfer_certificate)
    app.route("/course/<int:id>/certificate", methods=['POST'])(get_certificate_after_course)
