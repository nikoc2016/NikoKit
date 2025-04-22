"""
NKDrm - Python Code Signing and DRM Protection Tool

Provides cryptographic signing and runtime DRM verification for Python applications.
Supports converting .py files to .pyd via Nuitka and signing those binaries.

Features:
    - Convert .py to .pyd (via Nuitka).
    - RSA sign .pyd/.json files.
    - Verify file authenticity using public key during runtime.

Usage:
    Setup:
        drm = NKDrm()
        drm.keygen()  # Save these printed keys securely
        NKDrm.to_pyd("main.py", "dist/")
        drm.sign(["main.pyd", "license.json"])
        drm.save_file()

    Runtime:
        drm = NKDrm(public_key=...)
        drm.verify_drm_integrity()
        drm.verify("other_module.pyd")

Security:
    1. Do NOT embed the private key in production code.
    2. signatures.json is NOW encrypted with Public Key use AES256.

===== Example Setup.py =====
DIST_DIR = "F:\Build"
PRI_KEY = "-----BEGIN RSA PRIVATE KEY-----XXX-----END RSA PRIVATE KEY-----"
PUB_KEY = "-----BEGIN PUBLIC KEY-----XXX-----END PUBLIC KEY-----"

os.makedirs(DIST_DIR, exist_ok=True)
shutil.copy("main.py", p.join(DIST_DIR, "main.py"))
drm = NKDrm(pri_key=PRI_KEY, pub_key=PUB_KEY, signatures_json_path=p.join(DIST_DIR, "signatures.json"))
NKDrm.to_pyd("NKDrm.py", DIST_DIR)
NKDrm.to_pyd("Encrypted.py", DIST_DIR)
drm.sign(pyd_paths)
drm.save_file()

===== Example Verification (COPY-TO-YOUR-CODE) =====
import os.path as p

public_key = "-----BEGIN PUBLIC KEY-----XXXXX-----END PUBLIC KEY-----"
signatures_json_path = "F:\Build\signatures.json"
my_path = p.abspath(__file__) + "d"           # __file__ ends with .py even when running as .pyd
if p.isfile(my_path):
    drm = NKDrm(pub_key=public_key, signatures_json_path=signatures_json_path)
    success, message = drm.verify_drm_integrity()
    if not success:
        return success, message
    success, message = drm.verify(my_path)
    return success, message
return True, "Not a PYD, continues without DRM check."

===== Example Auto-Saved signatures.json =====
{
  "signatures": {
    "HEX64_A": "a.pyd",
    "HEX64_B": "b.pyd"
  }
}
"""
import base64
import glob
import hashlib
import json
import os
import shutil
import subprocess
import warnings
from typing import Optional, Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class NKDrm:
    def __init__(
        self,
        pri_key: str = "",
        pub_key: str = "",
        signatures: Optional[dict] = None,
        signatures_json_path: str = "",
    ):
        self.pri_key = pri_key
        self.pub_key = pub_key
        self.signatures = signatures or {}
        self.signatures_json_path = signatures_json_path

        if self.pri_key:
            warnings.warn(
                "NKDrm Initialized with Private Key. DONT DO THIS IN PRODUCTION",
                stacklevel=2,
            )

        if signatures_json_path and os.path.exists(signatures_json_path):
            self.load_file()

    def keygen(self) -> Tuple[str, str]:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        pri_key_str = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ).decode()

        pub_key_str = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        self.pri_key = pri_key_str
        self.pub_key = pub_key_str

        for line in self.pri_key.split("\n"):
            print(line)
        for line in self.pub_key.split("\n"):
            print(line)

    def sign(self, file_paths: list[str]) -> list[str]:
        if not self.pri_key:
            raise RuntimeError("NKDrm::Sign() No private key, can't sign.")

        private_key = serialization.load_pem_private_key(
            self.pri_key.encode(), password=None
        )

        result = []
        for path in file_paths:
            with open(path, "rb") as f:
                file_data = f.read()

            digest = hashlib.sha256(file_data).digest()
            signature = private_key.sign(
                digest,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )

            sig_hex = signature.hex()
            self.signatures[sig_hex] = os.path.basename(path)
            result.append(f"{sig_hex}:{os.path.basename(path)}")

        return result

    def verify(self, file_path: str) -> Tuple[bool, str]:
        if not self.pub_key:
            return False, "NKDrm::Verify() No public key, can't verify."

        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()

        digest = hashlib.sha256(file_data).digest()
        public_key = serialization.load_pem_public_key(self.pub_key.encode())

        for sig_hex, fname in self.signatures.items():
            if fname != filename:
                continue
            try:
                public_key.verify(
                    bytes.fromhex(sig_hex),
                    digest,
                    padding.PKCS1v15(),
                    hashes.SHA256(),
                )
                return True, f"NKDrm::Signature Verified! {filename}."
            except Exception:
                pass

        return False, f"NKDrm::Signature Not Found! {filename}."

    def verify_drm_integrity(self, bypass: bool = False) -> Tuple[bool, str]:
        if not bypass:
            self_path = os.path.abspath(__file__)
            self_path = self_path + "d" if self_path.endswith("py") else self_path
            return self.verify(self_path)
        return True, "NKDrm Integrity Verified."

    def save_file(self):
        if not self.signatures_json_path:
            raise ValueError("signatures_json_path is not set.")
        if not self.pub_key:
            raise ValueError("pub_key is required for AES-based save_file().")

        raw_data = {
            "signatures": self.signatures,
        }
        json_data = json.dumps(raw_data, indent=2, ensure_ascii=False).encode("utf-8")
        encrypted = self._encrypt_data_aes(json_data, self.pub_key)

        with open(self.signatures_json_path, "wb") as f:
            f.write(encrypted)

    def load_file(self):
        if not self.signatures_json_path or not os.path.exists(self.signatures_json_path):
            return

        if not self.pub_key:
            raise ValueError("pub_key is required for AES-based load_file().")

        with open(self.signatures_json_path, "rb") as f:
            encrypted = f.read()

        try:
            decrypted = self._decrypt_data_aes(encrypted, self.pub_key)
            data = json.loads(decrypted.decode("utf-8"))
            self.signatures.update(data.get("signatures", {}))
        except Exception as e:
            raise RuntimeError(f"NKDrm::Invalid Signature File - Tampered Maybe? {e}")

    @classmethod
    def _derive_aes_key(cls, password_str: str, key_len: int = 32) -> bytes:
        lines = password_str.strip().splitlines()
        middle = "".join(line.strip() for line in lines if not line.startswith("-----"))
        print(middle)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(middle.encode('utf-8'))
        return digest.finalize()[:key_len]

    @classmethod
    def _encrypt_data_aes(cls, data: bytes, password_str: str) -> bytes:
        key = cls._derive_aes_key(password_str)
        iv = os.urandom(16)

        pad_len = 16 - len(data) % 16
        data += bytes([pad_len]) * pad_len

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        return base64.b64encode(iv + ciphertext)

    @classmethod
    def _decrypt_data_aes(cls, encoded_data: bytes, password_str: str) -> bytes:
        key = cls._derive_aes_key(password_str)
        payload = base64.b64decode(encoded_data)

        iv = payload[:16]
        ciphertext = payload[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        pad_len = padded[-1]
        return padded[:-pad_len]

    @staticmethod
    def to_pyd(py_path, pyd_dir):
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
        ]
        subprocess.run(cmd, check=True)

        pattern = os.path.join(pyd_dir, f"{base_name}*.pyd")
        matches = glob.glob(pattern)
        if not matches:
            raise FileNotFoundError(f"NKDrm::ToPYD No compiled .pyd found for pattern: {pattern}")
        shutil.move(matches[0], final_pyd_path)
        return final_pyd_path
