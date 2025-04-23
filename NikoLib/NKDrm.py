import base64
import json
import os
import time
import hashlib
import warnings
from typing import Optional, Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

"""
NKDrm - A solution to DRM for file verification and activation key.

Vault Format:
{
  "vault_key": {                                                       # Key could be HASH to a file
    "timestamp": "UNIX timestamp as string",                           # Time of signature
    "payload": "string or JSON-serializable object",                   # META of your choice
    "signature": "RSA_SIGN(SHA256(vault_key + timestamp + payload))"   # Sign to be verified.
  }
}

Main Methods:
- keygen() → Generates and stores RSA keys
- sign(vault_key, payload) → Signs and stores a record
- get(vault_key) → Returns record (timestamp, payload, signature)
- save_vault() / load_vault() → Save/load vault (encrypted or plaintext)
- verify(vault_key, record, pubkey) → Verifies signature
- file_sha256(path) → SHA-256 of file content
- to_pyd(path, out_dir) → Compile .py to .pyd via Nuitka

WARNING:
1. Don't put private_key in your release of code.
2. Copy file_sha256() and verify() to your .pyd to verify from there and not import it from here!

EXAMPLE USAGE:
See End of the File, a example of .pyd integrity verification.
"""

##### COPY DON'T IMPORT #####
def file_sha256(file_path: str) -> str:
    prevent_ref("file_sha256")
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    return digest


def verify(vault_key: str, record: dict, pub_key: str) -> Tuple[bool, str]:
    prevent_ref("verify")
    try:
        public_key = serialization.load_pem_public_key(pub_key.encode())
        payload_str = record['payload'] if isinstance(record['payload'], str) else json.dumps(record['payload'],
                                                                                              separators=(',', ':'))
        content = vault_key + record['timestamp'] + payload_str
        digest = hashlib.sha256(content.encode()).digest()

        public_key.verify(
            bytes.fromhex(record['signature']),
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True, "Signature valid"
    except Exception as e:
        return False, f"Signature verification failed: {e}"


##### FREE TO IMPORT #####
def to_pyd(py_path, pyd_dir, nuitka_params=None):
    import glob
    import subprocess
    import shutil
    nuitka_params = nuitka_params if nuitka_params else []
    os.makedirs(pyd_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(py_path))[0]
    final_pyd_path = os.path.join(pyd_dir, f"{base_name}.pyd")
    try:
        os.remove(final_pyd_path)
    except:
        pass
    cmd = [
        "python", "-m", "nuitka",
        "--module", py_path,
        "--output-dir=" + pyd_dir,
        "--remove-output",
        "--no-pyi-file"
    ] + nuitka_params
    subprocess.run(cmd, check=True)

    pattern = os.path.join(pyd_dir, f"{base_name}*.pyd")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"NKDRM::to_pyd() -> No compiled .pyd found for pattern: {pattern}")
    shutil.move(matches[0], final_pyd_path)
    nkdrm_log("to_pyd", f"Compiled {py_path} to {final_pyd_path}")
    return final_pyd_path

class NKVault:
    def __init__(self, pri_key: str = '', pub_key: str = '', vault_path: str = '', vault_encrypt: bool = True):
        self.pri_key = pri_key
        self.pub_key = pub_key
        self.vault_path = vault_path
        self.vault_encrypt = vault_encrypt
        self.vault = {}

        if pri_key:
            warnings.warn("NKDRM::__init__() -> Do NOT include private key in production.")

        if self.vault_path and os.path.exists(self.vault_path):
            self.load_vault()

    def keygen(self) -> Tuple[str, str]:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        self.pri_key = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ).decode()

        self.pub_key = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        nkdrm_log("keygen", "Private and public keys generated.")
        print(self.pri_key)
        print(self.pub_key)
        return self.pri_key, self.pub_key

    def sign(self, vault_key: str, payload) -> dict:
        if not self.pri_key:
            raise RuntimeError("NKDRM::sign() -> No private key provided.")

        private_key = serialization.load_pem_private_key(self.pri_key.encode(), password=None)

        timestamp = str(int(time.time()))
        payload_str = payload if isinstance(payload, str) else json.dumps(payload, separators=(',', ':'))

        content = vault_key + timestamp + payload_str
        digest = hashlib.sha256(content.encode()).digest()

        signature = private_key.sign(
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        ).hex()

        self.vault[vault_key] = {
            "timestamp": timestamp,
            "payload": payload,
            "signature": signature
        }
        nkdrm_log("sign", f"Vault record added for key: {vault_key}")
        return self.vault[vault_key]

    def get(self, vault_key: str) -> Optional[dict]:
        return self.vault.get(vault_key)

    def save_vault(self):
        data = json.dumps(self.vault, indent=2).encode('utf-8')
        if not self.vault_encrypt:
            with open(self.vault_path, 'w', encoding='utf-8') as f:
                f.write(data.decode())
        else:
            encrypted = self.aes_encrypt(data, self.pub_key)
            with open(self.vault_path, 'wb') as f:
                f.write(encrypted)
        nkdrm_log("save_vault", "Vault saved to disk.")

    def load_vault(self):
        if not os.path.exists(self.vault_path):
            return
        if not self.vault_encrypt:
            with open(self.vault_path, 'r', encoding='utf-8') as f:
                self.vault = json.load(f)
        else:
            with open(self.vault_path, 'rb') as f:
                encrypted = f.read()
            decrypted = self.aes_decrypt(encrypted, self.pub_key)
            self.vault = json.loads(decrypted.decode('utf-8'))

    @staticmethod
    def aes_key_from_pubkey(pubkey: str) -> bytes:
        lines = pubkey.strip().splitlines()
        middle = ''.join(line.strip() for line in lines if not line.startswith('-----'))
        digest = hashlib.sha256(middle.encode()).digest()
        return digest[:32]

    @classmethod
    def aes_encrypt(cls, data: bytes, pubkey: str) -> bytes:
        key = cls.aes_key_from_pubkey(pubkey)
        iv = os.urandom(16)

        pad_len = 16 - len(data) % 16
        data += bytes([pad_len]) * pad_len

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        return base64.b64encode(iv + ciphertext)

    @classmethod
    def aes_decrypt(cls, encrypted: bytes, pubkey: str) -> bytes:
        key = cls.aes_key_from_pubkey(pubkey)
        data = base64.b64decode(encrypted)

        iv = data[:16]
        ciphertext = data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        pad_len = padded[-1]
        return padded[:-pad_len]


def nkdrm_log(function: str, message: str):
    print(f"NKDRM::{function}() -> {message}")

def prevent_ref(function_name: str):
    error_msg = f"DANGEROUS::Dont' import {function_name}()! Copy & Embed to your Code and remove line 'prevent_ref()'"
    warnings.warn(error_msg)

"""
# compile.py
import os
import shutil
import json
import sys

sys.path.append(r'F:\Codes')
from NikoKit.NikoLib import NKDrm

def main():
    DIST_DIR = "dist"
    MAIN_PY = "main.py"
    ENCRYPT_PY = "encrypt.py"
    VAULT_NAME = "vault.dll"

    vault = NKDrm.NKVault()
    PRI_KEY, PUB_KEY = vault.keygen()

    # Ensure clean build folder
    os.makedirs(DIST_DIR, exist_ok=True)
    shutil.copy(ENCRYPT_PY, os.path.join(DIST_DIR, ENCRYPT_PY))
    shutil.copy(MAIN_PY, os.path.join(DIST_DIR, MAIN_PY))

    # Replace pubkey placeholder in encrypt.py
    encrypt_path = os.path.join(DIST_DIR, ENCRYPT_PY)
    with open(encrypt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("[PUBKEY_TO_BE_FILLED]", PUB_KEY.strip().replace("\n", "\\n"))
    with open(encrypt_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Sign and generate vault
    pyd_path = NKDrm.to_pyd(encrypt_path, DIST_DIR)
    os.remove(encrypt_path)
    vault_key = NKDrm.file_sha256(pyd_path)
    vault.sign(vault_key, payload={"product": "MyApp", "feature": "DRM"})

    # Save to a misleading .dll
    vault.vault_path = os.path.join(DIST_DIR, VAULT_NAME)
    vault.save_vault()

    print ("compile", "Encryption & vault generation complete.")

if __name__ == "__main__":
    main()
"""

"""
# main.py
import os
from encrypt import verify_self_integrity

success, message = verify_self_integrity()
print("Integrity check:", message)
if not success:
    exit(1)

print("App is running...")
"""

"""
# encrypt.py
import os
import sys
from typing import Tuple
from NikoKit.NikoLib import NKDrm

sys.path.append(r'F:\Codes')

from NikoKit.NikoLib.NKDrm import file_sha256, verify  # THIS IS NOT SAFE, COPY TO YOUR CODE INSTEAD


pubkey = "[PUBKEY_TO_BE_FILLED]"
signature_file = "vault.dll"

def verify_self_integrity() -> Tuple[bool, str]:
    my_path = os.path.abspath(__file__ + "d")  # Expect .pyd at runtime
    if not os.path.isfile(my_path):
        return False, "NKDRM::verify_self_integrity() -> .pyd file not found"

    vault_key = file_sha256(my_path)
    if not os.path.exists(signature_file):
        return False, f"NKDRM::verify_self_integrity() -> Signature file not found: {signature_file}"

    vault = NKDrm.NKVault(pub_key=pubkey, vault_path=signature_file)

    record = vault.get(vault_key)
    if not record:
        return False, f"NKDRM::verify_self_integrity() -> No record found for vault key {vault_key}"

    return verify(vault_key, record, pubkey)

"""