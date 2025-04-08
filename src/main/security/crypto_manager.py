import os
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class CryptoManager:
    def __init__(self):
        path_to_project = os.getcwd() + '\\'
        private_key = os.path.exists(path_to_project + os.getenv('PRIVATE_KEY_PATH'))
        public_key = os.path.exists(path_to_project + os.getenv('PUBLIC_KEY_PATH'))
        
        if not (private_key and public_key):
            self.__generate_keys()

    @staticmethod
    def encrypt_data(json_data, public_key):
        data = json.dumps(json_data)
        data_bytes = data.encode('utf-8')

        symmetric_key = get_random_bytes(32)
        cipher_aes = AES.new(symmetric_key, AES.MODE_CBC)
        padded_data = pad(data_bytes, AES.block_size)
        encrypted_text = cipher_aes.encrypt(padded_data)

        asymmetric_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(asymmetric_key)
        encrypted_key = cipher_rsa.encrypt(symmetric_key)

        return base64.b64encode(cipher_aes.iv + encrypted_key + encrypted_text).decode('utf-8')

    @staticmethod
    def decrypt_data(cipher_text, private_key):
        cipher_data = base64.b64decode(cipher_text)

        iv = cipher_data[:16]
        encrypted_key = cipher_data[16:16 + 256]
        encrypted_text = cipher_data[16 + 256:]

        asymmetric_key = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(asymmetric_key)
        symmetric_key = cipher_rsa.decrypt(encrypted_key)

        cipher_aes = AES.new(symmetric_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_text), AES.block_size)

        return json.loads(decrypted_data.decode('utf-8'))

    def __generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open('private_key.pem', 'wb') as private_file:
            private_file.write(private_key)

        with open('public_key.pem', 'wb') as public_file:
            public_file.write(public_key)
