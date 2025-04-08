import os
import jwt
import requests
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token
from flask import Blueprint, jsonify, request, redirect, render_template, session
from datetime import timedelta
import datetime

portability_bp = Blueprint('portability', __name__, url_prefix='/portability')

secret_key = "c700f8af41363085d048dd9b875cbaf30a9691467c954930c9b673a04e262ac6"

@portability_bp.route('/token', methods=['GET'])
# @jwt_required()
def generete_and_save_token():
    identity = 'api-portability'
    additional_claims = {
        'company_id': 1
    }
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(minutes=2)
    )
    # payload = {
    # "sub": '12345',
    # "user_id": 12345,
    # "exp": timedelta(seconds=10)
    # }

    # # Gerar o token JWT
    # access_token = jwt.encode(payload, secret_key, algorithm="HS256")
    return {'token': str(access_token)}


@portability_bp.route('/', methods=['GET'])
# @jwt_required()
def login_form():
    session['api_callback'] = 'localhost:teste'
    return render_template('portability_form.html')

@portability_bp.route('/login', methods=['POST'])
# @jwt_required()
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    try:
        response = requests.post("http://localhost:5005/api/v0/users/login", json={
            "email": email,
            "password": senha
        })

        if response.status_code == 200:
            session['api_user_email'] = email

            data = response.json()
            # access_token = data.get('access_token')
            user_data = data.get('user')

            # if not access_token:
            #     return "Token não recebido", 500

            session['api_token'] = data.get('access_token')
            session['api_user_id'] = user_data.get('id')
            # session['api_user_name'] = f"{user_data.get('first_name')} {user_data.get('last_name')}"
            return redirect('/portability/confirm')
        else:
            return redirect('/portability/') # arrumar para que mostre a mensagem de erro de email ou senha

    except Exception as e:
        return f"Erro ao tentar autenticar: {str(e)}", 500


@portability_bp.route('/confirm', methods=['GET'])
def confirm_page():
    if 'api_user_email' not in session:
        return redirect('/portability/')
    return render_template('confirm_portability.html')


@portability_bp.route('/confirm/yes', methods=['POST'])
def confirm_yes():
    if 'api_user_email' not in session:
        return redirect('/portability/')

    try:
        headers = {
            'Authorization': f'Bearer {session.get('api_token')}',
            'Content-Type': 'application/json'
        }

        area_response = requests.get(
            os.getenv('API_PORTABILITY_URL'),
            headers=headers
        )
        user_response = requests.get(
            os.getenv('API_USER_URL').format(user_id=session.get("api_user_id")),
            headers=headers
        )

        area_data = []
        user_data = []

        if area_response.status_code == 200:
            area_data = area_response.json()
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            del user_data['id']
        
        data = {
            'user_data': user_data,
            'area_data': area_data
        }
        
        return data

    except Exception as e:
        print(e)
        return f"Erro ao tentar autenticar: {str(e)}", 500
