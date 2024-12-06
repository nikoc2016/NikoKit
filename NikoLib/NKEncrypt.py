"""
NKEncrypt - Encryption and Signature Library

This module provides an easy-to-use interface for encryption, decryption, signing, and signature verification using various cryptographic methods such as AES, RSA, and ECC.

Features:
1. AES Symmetric Encryption (Key Generation, Encrypt, Decrypt)
2. RSA Asymmetric Encryption (Key Generation, Encrypt, Decrypt, Sign, Verify)
3. ECC Asymmetric Cryptography (Key Generation, Sign, Verify)
4. Activation Key [Generate][Check]

Usage Example:
1. Generate AES, RSA, and ECC keys.
2. Encrypt and decrypt data using AES and RSA.
3. Sign data and verify signature using RSA and ECC.
4. Build or Verify activation key.

"""

import base64
import json
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


class NKEncrypt:
    def __init__(self):
        pass

    # AES 256 Key generation
    def keygen_aes(self, from_str="", length=256):
        if length not in [128, 192, 256]:
            raise ValueError("Invalid AES key length, must be 128, 192, or 256 bits")
        if from_str:
            # Hash the input string to generate a consistent key
            hash_function = hashlib.sha256()
            hash_function.update(from_str.encode('utf-8'))
            key = hash_function.digest()[:length // 8]
        else:
            key = os.urandom(length // 8)
        return key.hex()

    # AES Encryption (Symmetric)
    def encrypt_aes(self, data: str, key: str) -> str:
        data_bytes = data.encode('utf-8')
        key_bytes = bytes.fromhex(key)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
        return (iv + ciphertext).hex()

    def decrypt_aes(self, ciphertext: str, key: str) -> str:
        ciphertext_bytes = bytes.fromhex(ciphertext)
        key_bytes = bytes.fromhex(key)
        iv = ciphertext_bytes[:16]
        actual_ciphertext = ciphertext_bytes[16:]
        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
        return decrypted_data.decode('utf-8')

    # RSA Key pair generation
    def keygen_rsa(self, key_size=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        return private_pem, public_pem

    # RSA Encryption
    def encrypt_rsa(self, data: str, public_key_str: str) -> str:
        public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'), backend=default_backend())
        data_bytes = data.encode('utf-8')
        ciphertext = public_key.encrypt(
            data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext.hex()

    # RSA Decryption
    def decrypt_rsa(self, ciphertext: str, private_key_str: str) -> str:
        private_key = serialization.load_pem_private_key(private_key_str.encode('utf-8'), password=None, backend=default_backend())
        ciphertext_bytes = bytes.fromhex(ciphertext)
        decrypted_data = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode('utf-8')

    # RSA Signing
    def sign_rsa(self, data: str, private_key_str: str) -> str:
        private_key = serialization.load_pem_private_key(private_key_str.encode('utf-8'), password=None, backend=default_backend())
        data_bytes = data.encode('utf-8')
        signature = private_key.sign(
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()

    # RSA Signature Verification
    def sign_check_rsa(self, data: str, signature: str, public_key_str: str) -> bool:
        public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'), backend=default_backend())
        data_bytes = data.encode('utf-8')
        try:
            signature_bytes = bytes.fromhex(signature)
            public_key.verify(
                signature_bytes,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    # ECC Key pair generation
    def keygen_ecc(self, curve=ec.SECP256R1()):
        private_key = ec.generate_private_key(curve, default_backend())
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        return private_pem, public_pem

    # ECC Signing
    def sign_ecc(self, data: str, private_key_str: str) -> str:
        private_key = serialization.load_pem_private_key(private_key_str.encode('utf-8'), password=None, backend=default_backend())
        data_bytes = data.encode('utf-8')
        signature = private_key.sign(
            data_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    # ECC Signature Verification
    def sign_check_ecc(self, data: str, signature: str, public_key_str: str) -> bool:
        public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'), backend=default_backend())
        data_bytes = data.encode('utf-8')
        try:
            signature_bytes = bytes.fromhex(signature)
            public_key.verify(
                signature_bytes,
                data_bytes,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False
        
    # Turns your data into activation code: XXXDATAB64XXX|XXXSIGNATUREXXX
    def generate_credential_signature(self, data, private_key_str, algorithm="ecc"):
        serialized_data = json.dumps(data)
        encoded_data = base64.b64encode(serialized_data.encode()).decode()
        if algorithm == "ecc":
            signature = self.sign_ecc(encoded_data, private_key_str)
        elif algorithm == "rsa":
            signature = self.sign_rsa(encoded_data, private_key_str)
        else:
            raise Exception(f"NKEncrypt::Unexpected alogrithm <{algorithm}>.")
        return f"{encoded_data}|{signature}"

    # Throw in activation code, returns [is_legit][Data Object]
    def verify_credential_signature(self, credential, public_key_str, algorithm="ecc"):
        try:
            encoded_data, signature = credential.split('|')
            if algorithm == "ecc":
                is_valid = self.sign_check_ecc(encoded_data, signature, public_key_str)
            elif algorithm == "rsa":
                is_valid = self.sign_check_rsa(encoded_data, signature, public_key_str)
            else:
                raise Exception(f"NKEncrypt::Unexpected alogrithm <{algorithm}>.")
            if is_valid:
                decoded_data = base64.b64decode(encoded_data).decode()
                data = json.loads(decoded_data)
                return True, data
            else:
                return False, None
        except Exception as e:
            return False, None

# Example Function to Test NKEncrypt
def example():
    # Print helper to shorten output for keys and ciphertexts
    def print_short(data: str):
        data_replaced = data.replace('\n', ' ')
        if len(data_replaced) > 100:
            print(f'<{data_replaced[:50]} ... {data_replaced[-50:]}>')
        else:
            print(f'<{data_replaced}>')

    crypto = NKEncrypt()

    # AES Example
    aes_key = crypto.keygen_aes("password-text-seed")  # Here you can add password to aes key
    print("AES Key:")
    print_short(aes_key)
    aes_encrypted = crypto.encrypt_aes("Hello AES Encryption", aes_key)  # AES encrypt
    print("AES Encrypted:")
    print_short(aes_encrypted)
    aes_decrypted = crypto.decrypt_aes(aes_encrypted, aes_key)   # AES decrypt
    print("AES Decrypted:", aes_decrypted)

    # RSA Example
    private_rsa, public_rsa = crypto.keygen_rsa()   # Generate RSA keys
    print("RSA Public Key:")
    print_short(public_rsa)
    rsa_encrypted = crypto.encrypt_rsa("Hello RSA Encryption", public_rsa)   # RSA Encrypt
    print("RSA Encrypted:")
    print_short(rsa_encrypted)
    rsa_decrypted = crypto.decrypt_rsa(rsa_encrypted, private_rsa)   # RSA decrypt
    print("RSA Decrypted:", rsa_decrypted)
    rsa_signature = crypto.sign_rsa("Sign this message", private_rsa)   # RSA Sign
    print("RSA Signature:")
    print_short(rsa_signature)
    rsa_verified = crypto.sign_check_rsa("Sign this message", rsa_signature, public_rsa)  # RSA Verify Sign
    print("RSA Signature Verified:", rsa_verified)

    # ECC Example
    private_ecc, public_ecc = crypto.keygen_ecc()    # Generate ECC keys
    print("ECC Public Key:")
    print_short(public_ecc)
    ecc_signature = crypto.sign_ecc("Sign this message ECC", private_ecc)    # ECC Sign
    print("ECC Signature:")
    print_short(ecc_signature)
    ecc_verified = crypto.sign_check_ecc("Sign this message ECC", ecc_signature, public_ecc)     # ECC Verify Sign
    print("ECC Signature Verified:", ecc_verified)

    # Generate and verify credential
    credential = crypto.generate_credential_signature({"user_id": 123, "permissions": "admin"}, private_rsa, "rsa")
    print_short(f"generate_credential_signature()->{credential}")
    valid, data = crypto.verify_credential_signature(credential, public_rsa, "rsa")

    if valid:
        print("Credential VALID:", data)
    else:
        print("Credential INVALID.")

if __name__ == "__main__":
    example()
