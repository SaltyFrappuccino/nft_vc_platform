from flask import request, jsonify

from app.models.company import Company, CompanyEmployee
from app.models.user import User
from database import db


def register_company():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')

    if not name:
        return jsonify({'message': 'Company name is required'}), 400

    company = Company(name=name, address=address)
    db.session.add(company)
    db.session.commit()

    return jsonify({'message': 'Company registered successfully'}), 201


def fire_employee(id):
    data = request.get_json()
    employee_id = data.get('employee_id')

    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    employee = CompanyEmployee.query.filter_by(company_id=id, user_id=employee_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee fired successfully'}), 200


def transfer_employee(id):
    data = request.get_json()
    employee_id = data.get('employee_id')
    new_position = data.get('new_position')

    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    employee = CompanyEmployee.query.filter_by(company_id=id, user_id=employee_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    # Логика перевода сотрудника (например, обновление позиции)

    return jsonify({'message': 'Employee transferred successfully'}), 200


def hire_employee(id):
    data = request.get_json()
    employee_id = data.get('employee_id')

    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    user = User.query.get(employee_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_employee = CompanyEmployee(company_id=id, user_id=employee_id)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'Employee hired successfully'}), 201


def verify_work_experience(id):
    employee_id = request.args.get('employee_id')

    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    employee = CompanyEmployee.query.filter_by(company_id=id, user_id=employee_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    # Логика проверки стажа

    return jsonify({'message': 'Work experience verified'}), 200


def search_users():
    query = request.args.get('query')
    users = User.query.filter(
        (User.first_name.contains(query)) | (User.last_name.contains(query)) | (User.email.contains(query))).all()

    if not users:
        return jsonify({'message': 'No users found'}), 404

    return jsonify([user.to_dict() for user in users]), 200


def get_access_key(id):
    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    access_key = "generated-access-key"  # Пример ключа
    return jsonify({'access_key': access_key}), 200
