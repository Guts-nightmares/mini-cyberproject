"""
Educational Ransomware - File Decryptor
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This is the decryption tool for files encrypted by the educational ransomware.
"""

import os
import sys
from pathlib import Path
import argparse

from crypto_engine import CryptoEngine, EncryptionManifest


class RansomwareDecryptor:
    """Educational ransomware decryptor"""

    def __init__(self, private_key_path: Path, manifest_path: Path = None):
        self.private_key_path = private_key_path
        self.crypto = CryptoEngine()
        self.manifest = EncryptionManifest(manifest_path)

        # Statistics
        self.files_decrypted = 0
        self.files_failed = 0

        print("=" * 60)
        print("🔓 EDUCATIONAL RANSOMWARE DECRYPTOR")
        print("=" * 60)
        print()

    def load_private_key(self):
        """Load private key from file"""
        try:
            with open(self.private_key_path, 'rb') as f:
                pem = f.read()

            self.crypto.private_key = CryptoEngine.import_private_key(pem)
            self.crypto.public_key = self.crypto.private_key.public_key()
            print(f"✅ Private key loaded: {self.private_key_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading private key: {e}")
            return False

    def load_manifest(self):
        """Load encryption manifest"""
        if self.manifest.load():
            print(f"✅ Manifest loaded: {self.manifest.manifest_path}")
            print(f"   Victim ID: {self.manifest.manifest['victim_id']}")
            print(f"   Timestamp: {self.manifest.manifest['timestamp']}")
            print(f"   Encrypted files: {len(self.manifest.get_encrypted_files())}")
            return True
        else:
            print(f"❌ Error loading manifest: {self.manifest.manifest_path}")
            return False

    def decrypt_aes_key(self) -> bytes:
        """Decrypt the AES key using private key"""
        try:
            encrypted_key = self.manifest.get_encrypted_key()
            aes_key = self.crypto.decrypt_key_with_rsa(encrypted_key)
            print(f"✅ AES key decrypted: {aes_key.hex()[:32]}...")
            return aes_key
        except Exception as e:
            print(f"❌ Error decrypting AES key: {e}")
            return None

    def decrypt_files(self, aes_key: bytes):
        """Decrypt all files in manifest"""
        encrypted_files = self.manifest.get_encrypted_files()

        if not encrypted_files:
            print("\n⚠️  No files to decrypt")
            return

        print(f"\n🔓 Decrypting {len(encrypted_files)} files...\n")

        for i, file_path_str in enumerate(encrypted_files, 1):
            encrypted_path = Path(file_path_str + self.crypto.ENCRYPTED_EXTENSION)

            if not encrypted_path.exists():
                print(f"[{i}/{len(encrypted_files)}] {encrypted_path.name}... ⚠️  NOT FOUND")
                self.files_failed += 1
                continue

            print(f"[{i}/{len(encrypted_files)}] {encrypted_path.name}...", end=" ")

            try:
                if self.crypto.decrypt_file(encrypted_path, aes_key):
                    self.files_decrypted += 1
                    print("✅ DECRYPTED")
                else:
                    self.files_failed += 1
                    print("❌ FAILED")
            except Exception as e:
                print(f"❌ ERROR: {e}")
                self.files_failed += 1

    def run(self):
        """Execute decryption"""
        # Load private key
        if not self.load_private_key():
            return False

        print()

        # Load manifest
        if not self.load_manifest():
            return False

        print()

        # Decrypt AES key
        aes_key = self.decrypt_aes_key()
        if not aes_key:
            return False

        # Decrypt files
        self.decrypt_files(aes_key)

        # Print statistics
        print("\n📊 Decryption Statistics:")
        print(f"   Files decrypted: {self.files_decrypted}")
        print(f"   Files failed: {self.files_failed}")
        print(f"   Total: {self.files_decrypted + self.files_failed}")

        if self.files_failed == 0:
            print("\n✅ All files successfully decrypted!\n")
        else:
            print(f"\n⚠️  {self.files_failed} files could not be decrypted\n")

        return True


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Educational Ransomware Decryptor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This tool decrypts files encrypted by the educational ransomware.
You need the private key file to decrypt.
        """
    )

    parser.add_argument(
        "--key",
        required=True,
        type=str,
        help="Path to private key file (.pem)"
    )
    parser.add_argument(
        "--manifest",
        type=str,
        help="Path to manifest file (default: ~/.ransom_manifest.json)"
    )

    args = parser.parse_args()

    key_path = Path(args.key)
    if not key_path.exists():
        print(f"Error: Private key file not found: {key_path}")
        sys.exit(1)

    manifest_path = Path(args.manifest) if args.manifest else None

    # Run decryptor
    decryptor = RansomwareDecryptor(key_path, manifest_path)
    success = decryptor.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
