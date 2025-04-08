import os
import requests
from datetime import timedelta
from security.auth_manager import AuthManager
from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request, redirect, render_template, session, flash

# user.fortest@gmail.com

portability_bp = Blueprint('portability', __name__, url_prefix='/portability')

@portability_bp.route('/', methods=['GET'])
def login_form():
    session['api_callback'] = 'localhost:teste'
    return render_template('portability_form.html')


@portability_bp.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    try:
        response = requests.post(os.getenv('API_LOGIN_URL'), json={
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

            session['access_token'] = create_access_token(
                identity=str(user_data.get('id')),
                expires_delta=timedelta(minutes=2)
            )
            # session['api_user_name'] = f"{user_data.get('first_name')} {user_data.get('last_name')}"
            return redirect('/portability/confirm')
            # resp = make_response()
            # resp.set_cookie(key='access_token_cookie', value=session.get('token'), httponly=True, secure=True, max_age=timedelta(minutes=10))
            # return resp
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect('/portability/')
    except Exception as e:
        flash('Ocorreu um erro ao validar seu usuario. Tente novamente em alguns minutos', 'error')
        # return f"Erro ao tentar autenticar: {str(e)}", 500
        return redirect('/portability/')


@portability_bp.route('/confirm', methods=['GET'])
@AuthManager()
def confirm_page():
    # if 'api_user_email' not in session:
    #     return redirect('/portability/')
    return render_template('confirm_portability.html')


@portability_bp.route('/confirm/yes', methods=['POST'])
@AuthManager()
def confirm_yes():
    # if 'api_user_email' not in session:
    #     return redirect('/portability/')
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
