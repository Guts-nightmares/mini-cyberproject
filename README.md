# Mini Cyber Fun - Offensive Security Toolkit

⚠️ **FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This repository contains 5 advanced offensive security projects built in Python for educational purposes, penetration testing, and security research.

## ⚠️ CRITICAL WARNING

**THESE TOOLS ARE FOR AUTHORIZED USE ONLY**

These projects demonstrate real offensive security techniques. Unauthorized use is **ILLEGAL** and can result in:
- Criminal prosecution
- Imprisonment
- Heavy fines
- Civil liability

**Only use these tools:**
- With explicit written authorization
- On systems you own or have permission to test
- In isolated lab environments
- For educational purposes
- In authorized penetration testing engagements
- In CTF competitions

## Projects Overview

### 1. 🎯 APT Simulation Framework (`apt-framework/`)
Advanced Persistent Threat simulation with Command & Control infrastructure.

**Features:**
- Encrypted C2 server with agent management
- Stealth agents with beacon jitter
- Remote command execution
- Persistence mechanisms
- Multi-agent support
- Interactive operator console

**Tech Stack:** Python, aiohttp, cryptography (Fernet encryption)

**Use Cases:**
- Red team exercises
- Defense testing
- Threat simulation
- Security training

[📖 Full Documentation](apt-framework/README.md)

---

### 2. 🔒 Educational Ransomware (`educational-ransomware/`)
Full-featured ransomware with real encryption and dedicated decryptor.

**Features:**
- AES-256-CBC encryption
- RSA-2048 key protection
- Manifest-based file tracking
- Automated encryption/decryption
- Ransom note generation
- Victim identification

**Tech Stack:** Python, cryptography

**Use Cases:**
- Ransomware behavior analysis
- Incident response training
- Understanding crypto-malware
- Defense development

[📖 Full Documentation](educational-ransomware/README.md)

---

### 3. 👻 Python Rootkit (`python-rootkit/`)
LD_PRELOAD rootkit for hiding processes and files on Linux.

**Features:**
- System call hooking (readdir, stat, fopen)
- Process hiding from `/proc`
- File/directory hiding
- Configuration-based rules
- User-space and system-wide modes
- C library with Python management

**Tech Stack:** C (shared library), Python (manager)

**Use Cases:**
- Understanding rootkit techniques
- Detection tool development
- Linux security research
- Defensive training

[📖 Full Documentation](python-rootkit/README.md)

---

### 4. ⬆️ Privilege Escalation Scanner (`privesc-scanner/`)
Automated Linux privilege escalation scanner and exploiter.

**Features:**
- **Scanner:** Detects 10+ privesc vectors
- **Exploiter:** Provides exploitation guidance
- SUID/SGID binary analysis
- Sudo misconfiguration detection
- Docker escape techniques
- Kernel vulnerability checks
- Payload generation

**Tech Stack:** Python (standard library)

**Use Cases:**
- Post-exploitation enumeration
- Security auditing
- Hardening verification
- CTF challenges

[📖 Full Documentation](privesc-scanner/README.md)

---

### 5. 🎣 Advanced Phishing Framework (`phishing-framework/`)
Professional phishing simulation with MFA capture.

**Features:**
- Realistic credential harvesting pages
- MFA/2FA bypass simulation
- Campaign management & tracking
- 5 pre-built email templates
- SMTP integration
- Admin dashboard
- Real-time analytics

**Tech Stack:** Python, aiohttp, HTML/CSS

**Use Cases:**
- Security awareness training
- Phishing simulations
- Social engineering testing
- User education

[📖 Full Documentation](phishing-framework/README.md)

---

## Quick Start

Each project is self-contained. Navigate to the project directory and follow its README.

### General Installation Pattern

```bash
# Navigate to project
cd <project-name>

# Install dependencies (if needed)
pip install -r requirements.txt

# Read documentation
cat README.md

# Run project (varies by project)
python src/main_file.py --help
```

## Project Matrix

| Project | Language | Complexity | Risk Level | Platform |
|---------|----------|------------|------------|----------|
| APT Framework | Python | High | High | Cross-platform |
| Ransomware | Python | Medium | Critical | Cross-platform |
| Rootkit | C + Python | High | Medium | Linux only |
| PrivEsc Scanner | Python | Medium | Medium | Linux |
| Phishing Framework | Python | Medium | Medium | Cross-platform |

## Dependencies Summary

### APT Framework
- aiohttp
- cryptography

### Ransomware
- cryptography

### Rootkit
- gcc (for compilation)
- Linux OS

### PrivEsc Scanner
- None (Python stdlib only)

### Phishing Framework
- aiohttp
- aiofiles

## Learning Path

### Beginner
1. Start with **PrivEsc Scanner** (reconnaissance)
2. Study **Phishing Framework** (social engineering)

### Intermediate
3. Explore **Ransomware** (cryptography & malware)
4. Build with **APT Framework** (C2 infrastructure)

### Advanced
5. Master **Rootkit** (low-level hooking)

## Common Use Cases

### 1. Penetration Testing
- APT Framework: Post-exploitation C2
- PrivEsc Scanner: Local privilege escalation
- Phishing: Initial access simulation

### 2. Security Training
- Ransomware: Incident response drills
- Phishing: Awareness training
- All projects: Understanding attacker TTPs

### 3. CTF Competitions
- PrivEsc Scanner: Quick enumeration
- Rootkit: Stealth techniques
- All projects: Tool development skills

### 4. Research & Development
- All projects: Understanding offensive techniques
- Defensive tool development
- Security product testing

## Legal & Ethical Guidelines

### ✅ AUTHORIZED Use
- Written penetration testing agreements
- Your own systems/VMs
- Authorized red team engagements
- Security research with permission
- Educational environments (labs, VMs)
- CTF competitions

### ❌ UNAUTHORIZED Use
- Any system you don't own
- Without explicit written permission
- Production environments (without approval)
- Third-party systems
- "Testing" without authorization
- Any malicious intent

## Responsible Disclosure

If you discover vulnerabilities using these tools:

1. **Document findings** professionally
2. **Notify stakeholders** immediately
3. **Provide remediation** guidance
4. **Don't disclose publicly** until patched
5. **Follow responsible disclosure** timelines

## Educational Value

These projects teach:

- **Cryptography**: Encryption, key management
- **Networking**: C2 protocols, HTTP/HTTPS
- **Systems Programming**: System calls, hooking
- **Web Development**: Phishing pages, dashboards
- **Social Engineering**: Email templates, persuasion
- **Python Programming**: Async, file I/O, subprocess
- **Linux Internals**: LD_PRELOAD, /proc, capabilities
- **Security Concepts**: Attack vectors, defense evasion

## Defense & Detection

Each project includes:
- Detection methods
- Defensive countermeasures
- Mitigation strategies
- Security best practices

**Remember:** The goal is to improve security, not to harm.

## Repository Structure

```
mini-cyber-fun/
├── apt-framework/              # APT C2 simulation
│   ├── server/                 # C2 server
│   ├── agent/                  # Stealth agents
│   ├── common/                 # Shared utilities
│   └── README.md
├── educational-ransomware/     # Ransomware demo
│   ├── src/                    # Encryptor & decryptor
│   └── README.md
├── python-rootkit/             # LD_PRELOAD rootkit
│   ├── lib/                    # C library
│   ├── src/                    # Python manager
│   └── README.md
├── privesc-scanner/            # PrivEsc toolkit
│   ├── src/                    # Scanner & exploiter
│   └── README.md
├── phishing-framework/         # Phishing simulation
│   ├── src/                    # Server & email sender
│   ├── templates/              # HTML templates
│   └── README.md
└── README.md                   # This file
```

## Testing Environment Setup

### Recommended Setup

```bash
# Create isolated VMs
1. Kali Linux (attacker)
2. Ubuntu Server (target)
3. Windows 10 (target - optional)

# Network: Internal/NAT only
# Snapshots: Before testing
# Monitoring: Wireshark, syslog
```

### Virtual Lab Tools
- VirtualBox / VMware
- Docker containers
- Vagrant
- Cloud sandbox (AWS, Azure with proper isolation)

## Security Checklist

Before running any project:

- [ ] Have written authorization
- [ ] Isolated environment (VM/lab)
- [ ] Network segmentation
- [ ] No production data
- [ ] Backup/snapshots created
- [ ] Monitoring enabled
- [ ] Incident response ready
- [ ] Legal review completed

## Contributing

Contributions welcome for:
- Bug fixes
- Documentation improvements
- New features (educational value)
- Detection methods
- Defense techniques

**Not accepted:**
- 0-day exploits
- Malicious payloads
- Detection evasion (without educational value)
- Anything promoting illegal activity

## References & Resources

### Learning Resources
- [MITRE ATT&CK](https://attack.mitre.org/)
- [OWASP](https://owasp.org/)
- [Offensive Security](https://www.offensive-security.com/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

### Books
- "The Hacker Playbook" series
- "Penetration Testing" by Georgia Weidman
- "Red Team Field Manual"
- "Black Hat Python"

### Certifications
- OSCP (Offensive Security Certified Professional)
- CEH (Certified Ethical Hacker)
- GPEN (GIAC Penetration Tester)

## License

These projects are provided for educational purposes. Check individual project READMEs for specific licenses.

**Disclaimer:** The authors are not responsible for misuse of these tools. Users are solely responsible for ensuring legal and authorized use.

## Support

For educational questions or issues:
- Open an issue (no illegal activity questions)
- Check project-specific READMEs
- Review documentation thoroughly

## Acknowledgments

Built for educational purposes to help security professionals understand offensive techniques and build better defenses.

---

## Final Warning

🚨 **THESE ARE REAL OFFENSIVE SECURITY TOOLS** 🚨

- Use responsibly and ethically
- Obtain proper authorization
- Respect privacy and laws
- Focus on improving security
- Don't harm others

**Remember: With great power comes great responsibility.**

Stay legal. Stay ethical. Stay curious. 🔒
