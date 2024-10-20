from flask import request, jsonify

from app.models.company import Company, CompanyEmployee
from app.models.user import User
from database import db


def register_company():
    """
    Register a new company
    ---
    tags:
      - Companies
    responses:
      201:
        description: Company registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Company registered successfully"
      400:
        description: Company name is required
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Company name is required"
    """
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
    """
    Fire an employee from a company
    ---
    tags:
      - Companies
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the company
        schema:
          type: integer
    responses:
      200:
        description: Employee fired successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Employee fired successfully"
      404:
        description: Company or employee not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Company not found"
    """
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
    """
    Transfer an employee to a new position
    ---
    tags:
      - Companies
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the company
        schema:
          type: integer
    responses:
      200:
        description: Employee transferred successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Employee transferred successfully"
      404:
        description: Company or employee not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Company not found"
    """
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
    """
    Hire a new employee for a company
    ---
    tags:
      - Companies
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the company
        schema:
          type: integer
    responses:
      201:
        description: Employee hired successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Employee hired successfully"
      404:
        description: Company or user not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
    """
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
    """
    Verify the work experience of an employee
    ---
    tags:
      - Companies
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the company
        schema:
          type: integer
    responses:
      200:
        description: Work experience verified
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Work experience verified"
      404:
        description: Company or employee not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Employee not found"
    """
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
    """
    Search for users by query
    ---
    tags:
      - Users
    parameters:
      - in: query
        name: query
        required: true
        description: Search query
        schema:
          type: string
    responses:
      200:
        description: List of users found
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
      404:
        description: No users found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "No users found"
    """
    query = request.args.get('query')
    users = User.query.filter(
        (User.first_name.contains(query)) | (User.last_name.contains(query)) | (User.email.contains(query))).all()

    if not users:
        return jsonify({'message': 'No users found'}), 404

    return jsonify([user.to_dict() for user in users]), 200


def get_access_key(id):
    """
    Get access key for a company
    ---
    tags:
      - Companies
    parameters:
      - in: path
        name: id
        required: true
        description: The ID of the company
        schema:
          type: integer
    responses:
      200:
        description: Access key retrieved
        content:
          application/json:
            schema:
              type: object
              properties:
                access_key:
                  type: string
                  example: "generated-access-key"
      404:
        description: Company not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Company not found"
    """
    company = Company.query.get(id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    access_key = "generated-access-key"  # Пример ключа
    return jsonify({'access_key': access_key}), 200
