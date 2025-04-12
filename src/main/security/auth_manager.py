from functools import wraps
from flask_jwt_extended import decode_token
from werkzeug.exceptions import Unauthorized
from flask import redirect, url_for, session, flash
from util.message import ERROR_SESSION_EXPIRED

class AuthManager:
    def __check_jwt(self):
        """
        Checks if the access JWT token is present in the session.
        Returns True if the JWT token is present, otherwise False.
        """
        return 'access_token' in session

    def __get_jwt(self):
        """
        Retrieves the JWT token.
        """
        access_token = session.get('access_token')
        if access_token:
            try:
                decoded_token = decode_token(access_token)
                return decoded_token
            except Exception as e:
                flash(ERROR_SESSION_EXPIRED, 'error')
                return None
        return None

    def __verify_jwt(self):
        """
        Verifies if the JWT token is present and valid.
        """
        token = self.__get_jwt()
        if not token:
            raise Unauthorized(ERROR_SESSION_EXPIRED)
        # if token.get('exp') < datetime.now().timestamp():
        #     raise Unauthorized("Token expirado. Faça login novamente.")
        return token
    
    def __call__(self, fn):
        """
        Decorator to protect routes that require authentication.
        Checks if the JWT token is present in the session, if not, redirects to login.
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if self.__check_jwt():
                try:
                    self.__verify_jwt()
                except Unauthorized:
                    flash(ERROR_SESSION_EXPIRED, 'error')
                    return redirect(url_for('portability.login_form'))
            else:
                flash(ERROR_SESSION_EXPIRED, 'error')
                return redirect(url_for('portability.login_form'))
            return fn(*args, **kwargs)
        
        return wrapper
