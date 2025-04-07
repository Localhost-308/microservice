import os
import glob

class RegisterBlueprint:
    def __init__(self, app):
        self.app = app

    def registerAllBlueprint(self):
        # Encontra todos os arquivos que começam com 'endpoint' no diretório atual
        blueprint_files = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))

        for blueprint_file in blueprint_files:
            # Ignora o arquivo '__init__.py'
            if not blueprint_file.endswith('__init__.py'):
                # Importa dinamicamente o arquivo de Blueprint
                module_name = os.path.basename(blueprint_file).replace('.py', '')
                module = __import__(f'controller.{module_name}', fromlist=[module_name])

                # Busca o objeto Blueprint dentro do módulo
                blueprint = getattr(module, f'{module_name.replace('controller', 'bp')}', None)

                # Se o Blueprint for encontrado, registre-o
                if blueprint:
                    self.app.register_blueprint(blueprint)



# @portability_bp.route('/login', methods=['POST'])
# # @jwt_required()
# def login():
#     return 'Login feito com sucesso'

# @portability_bp.route('/user/info', methods=['POST'])
# # @jwt_required()
# def get_user_info():
#     email = request.form['email']
#     senha = request.form['senha']
#     callback = request.form['callback']
    
#     # Simulando uma "validação" - aqui poderia ser uma chamada de banco de dados ou autenticação externa
#     if email == "usuario@teste.com" and senha == "senha123":
#         # Sucesso na validação, agora redireciona
#         app_teste_url = f'{callback}?email={email}&senha={senha}'
#         return redirect(app_teste_url)
#     else:
#         # Se a validação falhar, podemos retornar uma mensagem ou reexibir o formulário
#         return "Credenciais inválidas", 400

