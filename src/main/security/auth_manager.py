from functools import wraps
from flask import redirect, url_for, session, flash
from flask_jwt_extended import decode_token
from werkzeug.exceptions import Unauthorized

class AuthManager:
    def __check_jwt(self):
        """
        Verifica se o cookie de acesso está presente na requisição.
        Retorna True se o cookie estiver presente, caso contrário False.
        """
        return 'access_token' in session

    def __get_jwt(self):
        """
        Obtém o JWT do cookie.
        """
        access_token = session.get('access_token')
        if access_token:
            try:
                decoded_token = decode_token(access_token)
                return decoded_token
            except Exception as e:
                flash(f"Sessão expirada. Faça login novamente.", 'error')
                return None
        return None

    def __verify_jwt(self):
        """
        Verifica se o JWT está presente e válido.
        """
        token = self.__get_jwt()
        if not token:
            raise Unauthorized("Token não encontrado ou inválido.")
        # if token.get('exp') < datetime.now().timestamp():
        #     raise Unauthorized("Token expirado. Faça login novamente.")
        print(token)
        return token
    
    def __call__(self, fn):
        """
        Decorador para proteger as rotas que requerem autenticação.
        Verifica se o JWT está presente no cookie, se não, redireciona para o login.
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if self.__check_jwt():
                try:
                    self.__verify_jwt()  # Verifica se o token é válido
                except Unauthorized:
                    flash('Sessão expirada ou inválida. Faça login novamente.', 'error')
                    return redirect(url_for('portability.login_form'))
            else:
                print('nao tem cookie')
                flash('Sessão expirada. Faça login novamente.', 'error')
                return redirect(url_for('portability.login_form'))
            return fn(*args, **kwargs)
        
        return wrapper
