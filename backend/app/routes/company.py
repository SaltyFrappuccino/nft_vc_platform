from flask import Flask

from app.controllers.company import (
    register_company,
    fire_employee,
    transfer_employee,
    hire_employee,
    verify_work_experience,
    search_users,
    get_access_key
)


def init_company_routes(app: Flask):
    app.route("/company/register", methods=['POST'])(register_company)
    app.route("/company/<int:id>/fire-employee", methods=['POST'])(fire_employee)
    app.route("/company/<int:id>/transfer-employee", methods=['POST'])(transfer_employee)
    app.route("/company/<int:id>/hire-employee", methods=['POST'])(hire_employee)
    app.route("/company/<int:id>/verify-work-experience", methods=['GET'])(verify_work_experience)
    app.route("/company/search-users", methods=['GET'])(search_users)
    app.route("/company/<int:id>/access-key", methods=['GET'])(get_access_key)
