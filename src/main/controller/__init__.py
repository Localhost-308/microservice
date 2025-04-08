import os
import glob

class RegisterBlueprint:
    def __init__(self, app):
        self.app = app

    def register_all_blueprint(self):
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
