# Educational Ransomware

⚠️ **FOR EDUCATIONAL PURPOSES ONLY**

This is an educational demonstration of ransomware encryption/decryption mechanisms. It is designed to help security professionals understand how ransomware works.

## ⚠️ WARNING

**NEVER use this tool on systems you don't own or without explicit written authorization.**

This tool is intended ONLY for:
- Educational purposes in controlled environments
- Security research in isolated VMs
- Authorized penetration testing with written permission
- Understanding ransomware mechanics for defensive purposes

## Features

### Encryption (Encryptor)
- **AES-256-CBC**: Industry-standard symmetric encryption
- **RSA-2048**: Asymmetric encryption for key protection
- **File targeting**: Configurable file extensions
- **Manifest tracking**: JSON manifest of encrypted files
- **Victim identification**: Unique victim ID generation

### Decryption (Decryptor)
- **RSA private key**: Required for AES key recovery
- **Batch decryption**: Decrypts all files from manifest
- **Error handling**: Continues on individual file errors
- **Statistics**: Reports success/failure counts

## How It Works

### Encryption Process

1. **Key Generation**:
   - Generate RSA-2048 key pair (public/private)
   - Generate random AES-256 key

2. **File Encryption**:
   - Find target files by extension
   - For each file:
     - Generate random IV
     - Encrypt with AES-256-CBC
     - Save as `filename.ext.encrypted`
     - Delete original

3. **Key Protection**:
   - Encrypt AES key with RSA public key
   - Store in manifest file

4. **Manifest**:
   - List of encrypted files
   - Encrypted AES key
   - Victim ID and timestamp

### Decryption Process

1. Load private key from file
2. Load encryption manifest
3. Decrypt AES key using RSA private key
4. Decrypt each file using AES key
5. Restore original files

## Installation

```bash
cd educational-ransomware
pip install -r requirements.txt
```

## Usage

### Encrypt Files (⚠️ USE WITH CAUTION)

```bash
# Dry run (simulation only)
python src/encryptor.py /path/to/test/directory --dry-run

# Actual encryption (use only on test data!)
python src/encryptor.py /path/to/test/directory
```

When prompted, type `ENCRYPT` to confirm.

### Decrypt Files

```bash
python src/decryptor.py --key PRIVATE_KEY_xxxxxx.pem
```

Or with custom manifest location:

```bash
python src/decryptor.py --key PRIVATE_KEY_xxxxxx.pem --manifest /path/to/manifest.json
```

## File Structure

```
educational-ransomware/
├── src/
│   ├── crypto_engine.py   # Cryptographic operations
│   ├── encryptor.py        # Main encryption tool
│   └── decryptor.py        # Main decryption tool
├── requirements.txt
└── README.md
```

## Target File Extensions

By default, the tool targets common file types:
- Documents: `.txt`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`
- Archives: `.zip`, `.rar`, `.7z`
- Media: `.mp3`, `.mp4`, `.avi`

## Technical Details

### Encryption Algorithm
- **Symmetric**: AES-256 in CBC mode
- **Asymmetric**: RSA-2048 with OAEP padding
- **Padding**: PKCS7 for AES
- **IV**: Random 16-byte IV per file

### Security Considerations

This implementation demonstrates:
1. ✅ Strong encryption (AES-256 + RSA-2048)
2. ✅ Proper key derivation
3. ✅ Random IV generation
4. ✅ Secure padding (PKCS7)

For educational clarity, it includes:
1. ⚠️ Private key saved locally (real ransomware keeps this secret)
2. ⚠️ Limited file scope (for safety)
3. ⚠️ Manifest with all details (for learning)

## Testing Safely

1. **Create test directory**:
```bash
mkdir ~/ransomware_test
echo "This is a test file" > ~/ransomware_test/test.txt
```

2. **Encrypt (dry-run first)**:
```bash
python src/encryptor.py ~/ransomware_test --dry-run
python src/encryptor.py ~/ransomware_test
```

3. **Decrypt**:
```bash
python src/decryptor.py --key ~/ransomware_test/PRIVATE_KEY_*.pem
```

## Legal Notice

**UNAUTHORIZED USE IS ILLEGAL**

This tool is for educational purposes only. Deploying ransomware on systems you don't own or without authorization is a serious crime in most jurisdictions.

Use responsibly and ethically.

## Learning Objectives

This project demonstrates:
- Hybrid encryption (RSA + AES)
- File system traversal
- Cryptographic best practices
- Error handling in encryption
- Manifest-based file tracking
- Ransom note generation

## Defensive Countermeasures

Understanding this helps defend against real ransomware:
1. **Backups**: Regular, offline backups are critical
2. **Detection**: Monitor for suspicious file operations
3. **Prevention**: Application whitelisting, least privilege
4. **Response**: Incident response procedures
5. **Recovery**: Tested backup restoration procedures
