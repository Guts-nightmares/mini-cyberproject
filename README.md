# Mini Cyber Fun - Mon Lab de Pentest

Salut! Bienvenue sur mon repo où je centralise mes projets et outils pour apprendre le pentest.

> **Disclaimer:** Tout ce qui est ici est pour l'apprentissage, les CTF et mon lab perso. Utilisez sur vos propres machines uniquement!

## Pourquoi ce repo?

Je me suis lancé dans la cybersécurité offensive et j'ai créé ce repo pour:
- Apprendre en codant mes propres outils
- Préparer l'OSCP
- Documenter ce que j'apprends
- Avoir un lab portable pour mes tests

## Structure du Projet

```
mini-cyber-fun/
├── professional-pentest-toolkit/  # Mes outils pro pour le pentest
│   ├── utilities/                # Scripts pour gérer mes engagements
│   ├── reporting/               # Auto-générer mes rapports
│   ├── physical-security/       # Tests HID et sécurité physique
│   ├── lab-educational/        # Mon lab d'apprentissage
│   └── methodologies/          # Mes notes de méthodologies
│
└── [anciens projets educatifs archivés]
```

## Mon Toolkit Professionnel

J'ai construit un vrai toolkit professionnel avec:

### Gestion d'Engagements
- **scope-manager.py** - Pour ne jamais tester hors scope (important!)
- **engagement-logger.py** - Logger toutes mes actions (CYA)
- **report-generator.py** - Générer des rapports propres pour les clients

### Physical Security
- **Scripts HID** - Pour mon Flipper Zero (tests de sécurité physique)
- **Payloads diagnostiques** - Scripts Windows/Linux pour audits
- **Méthodologie complète** - Mes notes sur le physical pentest

### Lab Éducatif
- **Reverse shells pédagogiques** - Pour comprendre comment ça marche
- **Setup de lab isolé** - Ma config Kali + Windows VMs
- **Guide Metasploit** - Mes notes sur Metasploit Framework
- **Détection et défense** - Comment détecter ce que je fais (blue team perspective)

## Quick Start

### Setup du Lab

```bash
# Installer les outils pro
cd professional-pentest-toolkit/lab-setup
sudo bash install-tools.sh

# Lire le guide de démarrage
cd ..
cat QUICK-START.md
```

### Premier Test (Lab Perso)

```bash
# Démarrer un engagement
python utilities/engagement-logger.py --start "Test-Lab-$(date +%Y%m%d)"

# Charger un scope
python utilities/scope-manager.py --load examples/scope-example.txt

# ... faire vos tests ...

# Générer le rapport
python reporting/report-generator.py --generate --format html
```

## Ce que j'ai Appris

En construisant ce toolkit, j'ai vraiment compris:

1. **L'importance du scope** - Ne JAMAIS tester sans autorisation
2. **Le logging** - Documenter tout pour les rapports clients
3. **Les outils pro** - Pourquoi Metasploit > scripts custom
4. **La détection** - Comment les blue teams nous detectent
5. **L'éthique** - Always get permission in writing!

## Mes Projets Éducatifs

J'ai aussi des projets plus anciens que j'ai créés pour apprendre:
- APT Framework (C2 simple)
- Ransomware éducatif (crypto)
- Phishing framework
- PrivEsc scanner
- Python rootkit

> **Note:** Ces projets sont purement éducatifs. Pour du vrai pentest, j'utilise maintenant des outils reconnus (Metasploit, Sliver, etc.)

## Outils que j'utilise

**Reconnaissance:**
- Nmap, Masscan
- Subfinder, Amass
- Nuclei
- Burp Suite Pro

**Exploitation:**
- Metasploit Framework
- Sliver C2
- SQLMap
- Impacket

**Physical:**
- Flipper Zero
- Bash Bunny
- USB Rubber Ducky

**Post-Exploitation:**
- Meterpreter
- BloodHound
- LinPEAS/WinPEAS

## Lab Setup

Mon lab perso:
- Kali Linux (attaquant)
- Windows 10 VM (cible)
- VulnHub machines
- HackTheBox Pro subscription

Réseau isolé, pas d'Internet pour éviter les accidents!

## Certifications Visées

- [ ] eJPT (done!)
- [ ] PNPT (en cours)
- [ ] OSCP (objectif 2024)
- [ ] CRTP (après OSCP)

## Resources que je Recommande

**Plateformes:**
- HackTheBox - Meilleure plateforme IMO
- TryHackMe - Bon pour débuter
- PortSwigger Academy - Gratuit et excellent pour le web

**Communautés:**
- r/oscp - Reddit
- IPPSec YouTube - Walkthrough HTB
- The Cyber Mentor - Formations gratuites

**Livres:**
- "The Hacker Playbook 3"
- "Penetration Testing" - Georgia Weidman
- "Red Team Field Manual"

## Contributions

Si vous trouvez des bugs ou avez des suggestions, n'hésitez pas à ouvrir une issue!

**Pas de PR pour:**
- Techniques d'evasion avancées sans contexte éducatif
- Exploits 0-day
- Outils offensifs sans disclaimers appropriés

## Licence et Disclaimers

**IMPORTANT:**

Ces outils sont pour:
- ✅ Votre lab personnel
- ✅ Machines que vous possédez
- ✅ Engagements avec autorisation ÉCRITE
- ✅ CTF et compétitions
- ✅ Apprentissage et éducation

Ces outils ne sont PAS pour:
- ❌ Systèmes sans autorisation
- ❌ Activités illégales
- ❌ Nuire à autrui

**L'accès non autorisé est un crime!** Toujours obtenir une autorisation écrite avant tout test.

## Contact

Trouvé un bug? Une question?
- Ouvrir une issue sur ce repo
- Check la documentation dans chaque dossier

## Remerciements

Merci à la communauté infosec pour le partage de connaissances:
- IppSec pour les walkthrough
- The Cyber Mentor pour les formations
- Offensive Security pour l'OSCP
- Tous les créateurs de CTF

---

**Stay curious, stay legal, stay ethical!** 🔒

*Last updated: 2024 - En constante évolution*
