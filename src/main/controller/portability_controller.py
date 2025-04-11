import os
import requests
from datetime import timedelta
from security.auth_manager import AuthManager
from security.crypto_manager import CryptoManager
from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request, redirect, render_template, session, flash

portability_bp = Blueprint('portability', __name__, url_prefix='/portability')
crypto_manager = CryptoManager()

# @portability_bp.route('/favicon.ico')
# def favicon():
#     return '', 204


@portability_bp.route('/', methods=['GET'])
def login_form():
    session.clear()
    session['api_callback'] = request.args.get('callback')
    return render_template('portability_form.html')


@portability_bp.route('/login', methods=['POST'])
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
            user_data = data.get('user')

            session['api_token'] = data.get('access_token')
            session['api_user_id'] = user_data.get('id')

            session['access_token'] = create_access_token(
                identity=str(user_data.get('id')),
                expires_delta=timedelta(minutes=5)
            )

            return redirect('/portability/confirm')
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect('/portability/')
    except Exception as e:
        flash('Ocorreu um erro ao validar seu usuario. Tente novamente em alguns minutos', 'error')
        return redirect('/portability/')


@portability_bp.route('/confirm', methods=['GET'])
@AuthManager()
def confirm_page():
    return render_template('confirm_portability.html')


@portability_bp.route('/confirm/yes', methods=['POST'])
@AuthManager()
def confirm_yes():
    try:
        user_fields = request.form.getlist('user_data')
        area_fields = request.form.getlist('area_data')

        headers = {
            'Authorization': f'Bearer {session.get('api_token')}',
            'Content-Type': 'application/json'
        }

        area_response = requests.get(
            os.getenv('API_PORTABILITY_URL'),
            headers=headers,
            json={'columns': area_fields}
        )
        user_response = requests.get(
            os.getenv('API_USER_URL').format(user_id=session.get("api_user_id")),
            headers=headers
        )

        area_data = []
        user_data = {}

        if area_response.status_code == 200:
            area_data = area_response.json()
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            del user_data['id']
        
        data = {
            'user_data': {k: v for k,v in user_data.items() if k in user_fields},
            'area_data': area_data
        }

        return redirect(f"{session.get('api_callback')}?data={crypto_manager.encrypt_data(data)}", code=302)
    except Exception as e:
        flash('Ocorreu um erro ao pegar as suas informações. Tente novamente em alguns minutos', 'error')
        return redirect('/portability/')

