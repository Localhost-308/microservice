import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
from flask_session import Session
from controller import RegisterBlueprint
from extension.jwt_extension import jwt
# from extension.database_extension import db
# from extension.google_extension import oauth
# from database.connection import DatabaseConnection

class App:
    def __init__(self):
        self.app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'src/main/template'))
        load_dotenv(dotenv_path=os.path.join('.env'))
        try:
            self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
            self.app.config['SESSION_TYPE'] = 'filesystem'

            # self.app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConnection.get_db_url()
            # self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            self.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
            self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
            self.app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))

            # CORS(self.app, resources={r"/*": {"origins": "http://localhost:4200"}})
            CORS(self.app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:4200"}})

            Session(self.app)
            # oauth.init_app(self.app)
            # db.init_app(self.app)
            jwt.init_app(self.app)

            # self.app.teardown_appcontext(self._close_database_connection)
            # self.app.before_request(self._create_database_connection)
         
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def getApp(self):
        return self.app

    def run(self, host:str='127.0.0.1', port:int=5000, debug:bool=True):
        self.app.run(host=host, port=port, debug=debug)
    
    def registerBlueprint(self):
        RegisterBlueprint(self.app).registerAllBlueprint()

    # def _close_database_connection(self, exception=None):
    #     DatabaseConnection.close_connection(exception)

    # def _create_database_connection(self):
    #     """Garante que a conexão seja criada antes da requisição"""
    #     DatabaseConnection.create_connection()

if __name__ == '__main__':
    app_instance = App()
    app_instance.registerBlueprint()
    app_instance.run()
