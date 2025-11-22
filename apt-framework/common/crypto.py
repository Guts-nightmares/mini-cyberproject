"""
APT Framework - Cryptographic Utilities
⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os


class SecureComm:
    """Handles encrypted communication between C2 and agents"""

    def __init__(self, password: str = None):
        if password:
            self.key = self._derive_key(password)
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        salt = b'apt_framework_salt_v1'  # In production, use random salt
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data"""
        return self.cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data"""
        return self.cipher.decrypt(data)

    def get_key(self) -> bytes:
        """Get encryption key"""
        return self.key


class Obfuscator:
    """Simple obfuscation techniques"""

    @staticmethod
    def xor_encode(data: bytes, key: bytes) -> bytes:
        """XOR encoding"""
        return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

    @staticmethod
    def xor_decode(data: bytes, key: bytes) -> bytes:
        """XOR decoding"""
        return Obfuscator.xor_encode(data, key)

    @staticmethod
    def add_junk(data: bytes, junk_ratio: float = 0.3) -> tuple:
        """Add junk bytes to obfuscate payload"""
        junk_positions = []
        result = bytearray()
        junk_count = int(len(data) * junk_ratio)

        for i, byte in enumerate(data):
            # Randomly insert junk
            if i % (len(data) // max(1, junk_count)) == 0 and len(junk_positions) < junk_count:
                junk_byte = os.urandom(1)[0]
                result.append(junk_byte)
                junk_positions.append(len(result) - 1)
            result.append(byte)

        return bytes(result), junk_positions

    @staticmethod
    def remove_junk(data: bytes, junk_positions: list) -> bytes:
        """Remove junk bytes"""
        result = bytearray(data)
        for pos in sorted(junk_positions, reverse=True):
            if pos < len(result):
                del result[pos]
        return bytes(result)
