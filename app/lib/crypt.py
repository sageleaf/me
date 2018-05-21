from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode


def decrypt(encryptedText) -> (str, str):
    try:
        from config import PRIVATE_KEY
        private_key = RSA.importKey(PRIVATE_KEY)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        decrypted_message = cipher.decrypt(b64decode(encryptedText))
        return decrypted_message, None
    except Exception as e:
        return None, e