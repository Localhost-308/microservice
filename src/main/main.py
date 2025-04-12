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
        load_dotenv(dotenv_path=os.path.join('.env'))
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
            print(f"Erro inesperado: {e}")

    def get_app(self):
        return self.app

    def run(self, host:str='127.0.0.1', port:int=5000, debug:bool=True):
        self.app.run(host=host, port=port, debug=debug)
    
    def register_blueprint(self):
        RegisterBlueprint(self.app).register_all_blueprint()

    def remove_unknown_endpoints(self):
        """
        Configures redirects for any unknown routes, ensuring that:
        1. Access to the root ('/') is redirected to '/portability/'.
        2. Any other URL that does not match a defined route is redirected to '/portability/'.
        3. If a user tries to access a path under '/portability/' (e.g., '/portability/<some_path>'),
        they will also be redirected to the root of '/portability/'.

        These redirects ensure that the user is always directed to the '/portability/' page 
        and prevents 404 errors for invalid URLs.
        """
        # @self.app.route('/', methods=['GET'])
        # def root():
        #     return redirect('/portability/', code=301)
        
        # @self.app.route('/<path:path>', methods=['GET', 'POST'])
        # def catch_all(path):
        #     return redirect('/portability/', code=301)

        # @self.app.route('/portability/<path:path>', methods=['GET', 'POST'])
        # def catch_all_portability(path):
        #     return redirect('/portability/', code=301)

if __name__ == '__main__':
    app_instance = App()
    app_instance.register_blueprint()
    app_instance.remove_unknown_endpoints()
    app_instance.run()
