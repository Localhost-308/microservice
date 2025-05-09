import os
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, redirect
from flask_session import Session
from extension.jwt_extension import jwt
from controller import RegisterBlueprint

class App:
    def __init__(self):
        self.app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'src/main/template'))
        load_dotenv(dotenv_path=os.path.join('.env'), override=True)
        try:
            self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
            self.app.config['SESSION_TYPE'] = 'filesystem'

            self.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
            self.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
            self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
            self.app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))

            CORS(self.app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:4200"}})
            Session(self.app)
            jwt.init_app(self.app)
         
        except Exception as e:
            pass

    def get_app(self):
        return self.app

    def run(self, host:str='127.0.0.1', port:int=5000, debug:bool=True):
        self.app.run(host=host, port=port, debug=debug)
    
    def register_blueprint(self):
        RegisterBlueprint(self.app).register_all_blueprint()

if __name__ == '__main__':
    app_instance = App()
    app_instance.register_blueprint()
    app_instance.run()
