import os
import requests
from datetime import timedelta
from urllib.parse import quote
from security.auth_manager import AuthManager
from security.crypto_manager import CryptoManager
from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request, redirect, render_template, session, flash, abort
from util.session import ACCESS_TOKEN, API_CALLBACK, API_PUBLIC_KEY, API_TOKEN, API_USER_DATA, SHOW_AREA_INFO
from util.message import ERROR_LOGIN_VALIDATION, ERROR_LOGIN_INVALID_CREDENTIALS, ERROR_PORTABILITY_DATA_FETCH, ERROR_API_MISSING_PARAMS

portability_bp = Blueprint('portability', __name__, url_prefix='/portability')
crypto_manager = CryptoManager()

@portability_bp.route('/', methods=['GET'])
def login_form():
    print('env user url: ', os.getenv('API_USER_URL'))
    if not session.get(API_CALLBACK):
        params = request.args
        session[API_PUBLIC_KEY] = '-----BEGIN PUBLIC KEY-----' + params.get('public_key') + '-----END PUBLIC KEY-----'
        session[API_CALLBACK] = params.get('callback')
        if not session.get(API_CALLBACK):
            abort(400, ERROR_API_MISSING_PARAMS)
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
            data = response.json()
            user_data = data.get('user')
            
            session[API_TOKEN] = data.get(ACCESS_TOKEN)
            session[API_USER_DATA] = user_data
            session[ACCESS_TOKEN] = create_access_token(
                identity=str(user_data.get('id')),
                expires_delta=timedelta(minutes=5)
            )

            return redirect('/portability/confirm')
        else:
            flash(ERROR_LOGIN_INVALID_CREDENTIALS, 'error')
            return redirect('/portability/')
    except Exception as e:
        flash(ERROR_LOGIN_VALIDATION, 'error')
        return redirect('/portability/')


@portability_bp.route('/confirm', methods=['GET'])
@AuthManager()
def confirm_page():
    return render_template('confirm_portability.html')


@portability_bp.route('/confirm/yes', methods=['POST'])
@AuthManager()
def confirm_yes():
    try:
        data = session.get(API_USER_DATA)
        if 'id' in data:
            del data['id']
        encrypted_data = crypto_manager.encrypt_data(data, external_public_key=session.get(API_PUBLIC_KEY))
        external_api_callback = session.get(API_CALLBACK)
        session.clear()
        return redirect(f'{external_api_callback}?data={quote(encrypted_data)}', code=302)
    except Exception as e:
        print(e)
        flash(ERROR_PORTABILITY_DATA_FETCH, 'error')
        return redirect('/portability/')
