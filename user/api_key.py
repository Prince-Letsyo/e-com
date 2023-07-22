import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_dict(password, data):
    # Serialize the dictionary to JSON
    serialized_data = json.dumps(data).encode()

    # Generate a new random salt for each encryption operation
    salt = os.urandom(16)

    # Prepare the encryption key using PBKDF2 with the provided password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password)

    # Encrypt data using AES in CFB mode
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(serialized_data) + encryptor.finalize()

    # Return the ciphertext, salt, and IV (you can store the salt and IV with the encrypted data)
    return ct, salt, iv


def decrypt_dict(password, salt, ct, iv):
    # Prepare the encryption key using PBKDF2 with the provided password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password)

    # Decrypt data using AES in CFB mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    serialized_data = decryptor.update(ct) + decryptor.finalize()

    # Deserialize the JSON data back to a dictionary
    data = json.loads(serialized_data.decode())

    return data
