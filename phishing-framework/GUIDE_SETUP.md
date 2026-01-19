# GUIDE DE SETUP - FRAMEWORK DE PHISHING ÉDUCATIF

## SUPER IMPORTANT - LIS CETTE PARTIE EN PREMIER

**⚠️ Ce framework est UNIQUEMENT pour apprendre la cybersécurité!**

- ✅ **OUI**: Teste sur tes propres emails
- ✅ **OUI**: Utilise pour des devoirs/exercices d'école
- ✅ **OUI**: Apprends comment marche le phishing
- ❌ **NON**: N'envoie JAMAIS d'emails à de vraies personnes sans autorisation
- ❌ **NON**: Ne piège pas tes amis/famille
- ❌ **NON**: N'utilise pas pour de vraies attaques

**Tu pourrais avoir de GROS problèmes légaux si tu utilises ça mal!**

---

## C'EST QUOI CE PROJET?

C'est un framework (= un ensemble d'outils) pour faire du phishing éducatif. Le phishing, c'est quand tu crées un faux site web (genre un faux Netflix ou Gmail) pour capturer les mots de passe des gens.

**Ce que tu vas apprendre:**
1. Comment les hackers créent des faux sites web
2. Comment capturer des identifiants
3. Comment envoyer des emails qui ont l'air légitimes
4. Comment les gens se font avoir (pour mieux te protéger!)

---

## ARCHITECTURE DU PROJET

```
phishing-framework/
│
├── src/                          # Code source principal
│   ├── phishing_server.py        # Le serveur web qui héberge les fausses pages
│   └── email_sender.py           # Envoie les emails de phishing
│
├── templates/                    # Pages HTML (ce que la victime voit)
│   ├── login.html                # Fausse page de connexion
│   └── mfa.html                  # Fausse page 2FA
│
├── data/                         # Dossier où sont sauvegardés les résultats
│   └── credentials.jsonl         # Fichier avec les identifiants capturés
│
├── static/                       # Images, CSS, JavaScript (optionnel)
│
├── requirements.txt              # Liste des librairies Python nécessaires
├── README.md                     # Documentation générale
└── GUIDE_SETUP.md                # Ce fichier! (guide d'installation)
```

---

## PRÉREQUIS (CE DONT TU AS BESOIN)

### 1. Python installé

Tu dois avoir Python 3.8 ou plus récent. Pour vérifier:

```bash
python --version
```

Ou sur certains PC:

```bash
python3 --version
```

**Si tu n'as pas Python:**
- Windows: Télécharge sur https://www.python.org/downloads/
- Mac: `brew install python3` (si tu as Homebrew)
- Linux: `sudo apt install python3 python3-pip`

### 2. Un éditeur de code (optionnel mais pratique)

- **VS Code** (recommandé): https://code.visualstudio.com/
- **Sublime Text**: https://www.sublimetext.com/
- **Notepad++**: https://notepad-plus-plus.org/

### 3. Un compte email pour envoyer (optionnel)

Si tu veux envoyer des vrais emails (vers tes propres comptes!), tu auras besoin:
- Un compte Gmail OU
- Un compte Outlook OU
- N'importe quel compte email avec accès SMTP

---

## INSTALLATION ÉTAPE PAR ÉTAPE

### Étape 1: Télécharger/Cloner le projet

Si tu as Git:
```bash
git clone https://github.com/ton-username/phishing-framework.git
cd phishing-framework
```

Sinon, télécharge le ZIP et extrais-le quelque part.

### Étape 2: Créer un environnement virtuel (optionnel mais recommandé)

**Pourquoi?** Pour ne pas polluer ton Python global avec des librairies.

**Sur Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sur Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Tu verras `(venv)` apparaître dans ton terminal = c'est activé!

### Étape 3: Installer les dépendances

```bash
pip install -r requirements.txt
```

**Qu'est-ce qui s'installe?**
- `aiohttp`: Pour créer le serveur web asynchrone
- `aiofiles`: Pour lire/écrire des fichiers de manière asynchrone

**Si ça marche pas:**
- Essaie `pip3` au lieu de `pip`
- Essaie `python -m pip install -r requirements.txt`

### Étape 4: Vérifier que tout est installé

```bash
pip list
```

Tu devrais voir `aiohttp` et `aiofiles` dans la liste.

---

## UTILISATION - MODE DÉBUTANT

### Test 1: Lancer le serveur de phishing

**Commande la plus simple:**
```bash
python src/phishing_server.py
```

**Tu verras:**
```
============================================================
⚠️  FRAMEWORK DE PHISHING ÉDUCATIF
⚠️  UNIQUEMENT POUR APPRENDRE
⚠️  TESTE SEULEMENT SUR TES PROPRES COMPTES
============================================================
🚀 Phishing server started on http://0.0.0.0:8080
📊 Admin dashboard: http://127.0.0.1:8080/admin
🎣 Phishing page: http://127.0.0.1:8080/login
📋 Campaign created: test - Target: test-target@example.com
```

**Maintenant, ouvre ton navigateur et va sur:**
- **Page de phishing**: http://localhost:8080/login
- **Dashboard admin**: http://localhost:8080/admin

**Teste la page de login:**
1. Entre n'importe quel email (ex: `test@test.com`)
2. Entre n'importe quel mot de passe (ex: `password123`)
3. Clique sur "Sign In"
4. Tu verras une page MFA, entre un code (ex: `123456`)
5. Tu seras redirigé vers Google

**Regarde les résultats:**
- Va sur http://localhost:8080/admin
- Tu verras les stats: clics, identifiants capturés
- Les données sont aussi dans `data/credentials.jsonl`

**Pour arrêter le serveur:**
- Appuie sur `Ctrl+C` dans le terminal

### Test 2: Prévisualiser un email (sans l'envoyer)

```bash
python src/email_sender.py --template password_reset --preview
```

**Tu verras l'email s'afficher dans le terminal.**

**Essaye d'autres templates:**
```bash
python src/email_sender.py --template security_alert --preview
python src/email_sender.py --template account_verification --preview
python src/email_sender.py --template mfa_setup --preview
python src/email_sender.py --template invoice --preview
```

---

## UTILISATION AVANCÉE

### Personnaliser l'hôte et le port

Par défaut, le serveur écoute sur `0.0.0.0:8080`. Tu peux changer:

```bash
# Écouter seulement sur localhost (plus sécurisé pour les tests)
python src/phishing_server.py --host 127.0.0.1 --port 8080

# Changer le port
python src/phishing_server.py --host 0.0.0.0 --port 5000
```

**Différence entre les hôtes:**
- `127.0.0.1`: Seulement accessible depuis TON PC
- `0.0.0.0`: Accessible depuis n'importe quel appareil sur ton réseau local
  (par exemple, ton téléphone peut accéder via `http://192.168.1.X:8080`)

### Envoyer un vrai email (vers ton propre compte!)

**ATTENTION: Envoie SEULEMENT vers tes propres emails pour tester!**

#### Configuration Gmail (le plus simple)

1. **Active la 2FA sur ton compte Gmail:**
   - Va sur https://myaccount.google.com/security
   - Active "Validation en deux étapes"

2. **Crée un mot de passe d'application:**
   - Va sur https://myaccount.google.com/apppasswords
   - Crée un mot de passe pour "Autre"
   - **Copie ce mot de passe** (tu le reverras plus!)

3. **Envoie un email de test:**

```bash
python src/email_sender.py \
  --template password_reset \
  --to TON-EMAIL@gmail.com \
  --from security@company.com \
  --phishing-url http://localhost:8080/track/test \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username TON-EMAIL@gmail.com \
  --password LE-MOT-DE-PASSE-APP
```

**Remplace:**
- `TON-EMAIL@gmail.com`: ton vrai email Gmail
- `LE-MOT-DE-PASSE-APP`: le mot de passe d'application que tu as créé

4. **Vérifie ton email:**
   - Tu devrais recevoir un faux email de "sécurité"
   - Clique sur le lien
   - Tu seras redirigé vers ton serveur local
   - Entre n'importe quoi et regarde le dashboard admin

#### Configuration Outlook/Hotmail

```bash
python src/email_sender.py \
  --template password_reset \
  --to TON-EMAIL@outlook.com \
  --from security@company.com \
  --phishing-url http://localhost:8080/track/test \
  --smtp-server smtp-mail.outlook.com \
  --smtp-port 587 \
  --username TON-EMAIL@outlook.com \
  --password TON-MOT-DE-PASSE
```

---

## PERSONNALISATION

### Modifier les pages HTML

Les pages HTML sont dans `templates/`:

**Pour modifier la page de login:**
1. Ouvre `templates/login.html` dans ton éditeur
2. Change les couleurs, le logo, le texte
3. Sauvegarde
4. Redémarre le serveur

**Idées de personnalisation:**
- Changer le logo (🔐 → 🌟 ou une vraie image)
- Changer les couleurs (imiter Netflix, Facebook, etc.)
- Changer le nom "Company Portal" → "Netflix", "Gmail", etc.

**Variables disponibles dans les templates:**
- `{{campaign_id}}`: L'ID de la campagne
- `{{username}}`: L'email de la victime (dans mfa.html)

### Créer un nouveau template d'email

Ouvre `src/email_sender.py` et ajoute dans `TEMPLATES`:

```python
"mon_template": {
    "subject": "Ton sujet d'email ici",
    "body": """
Bonjour {name},

Ton message personnalisé ici.

Clique ici: {phishing_link}

Merci!
    """
}
```

**Variables disponibles:**
- `{name}`: Nom de la victime
- `{phishing_link}`: Le lien de phishing
- `{company}`: Nom de l'entreprise
- `{timestamp}`: Date/heure actuelle

**Pour l'utiliser:**
```bash
python src/email_sender.py --template mon_template --preview
```

---

## STRUCTURE DES DONNÉES CAPTURÉES

Les identifiants sont sauvegardés dans `data/credentials.jsonl`.

**Format:**
```json
{"timestamp": "2026-01-19T10:30:00", "ip": "127.0.0.1", "username": "test@test.com", "password": "secret123", "campaign_id": "test"}
{"timestamp": "2026-01-19T10:30:15", "ip": "127.0.0.1", "username": "test@test.com", "mfa_code": "123456", "campaign_id": "test"}
```

**Chaque ligne = une capture:**
- Première ligne: identifiants (email + password)
- Deuxième ligne: code MFA

---

## DÉPANNAGE (SI ÇA MARCHE PAS)

### Problème: "Port already in use" (port déjà utilisé)

**Cause:** Un autre programme utilise le port 8080.

**Solution:**
```bash
# Utilise un autre port
python src/phishing_server.py --port 5000
```

### Problème: "Module not found: aiohttp"

**Cause:** Les dépendances ne sont pas installées.

**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: "Permission denied" sur le port 80 ou 443

**Cause:** Les ports < 1024 nécessitent des droits admin.

**Solution:**
- Utilise un port > 1024 (comme 8080)
- Ou lance avec `sudo` (Linux/Mac):
  ```bash
  sudo python3 src/phishing_server.py --port 80
  ```

### Problème: L'email ne s'envoie pas

**Vérifications:**
1. Le serveur SMTP est correct? (`smtp.gmail.com` pour Gmail)
2. Le port est correct? (587 pour la plupart)
3. Le mot de passe d'application est correct? (pas ton mot de passe normal!)
4. Ton compte Gmail a la 2FA activée?
5. Tu as créé un mot de passe d'application?

**Teste la connexion SMTP:**
```bash
python src/email_sender.py --preview  # Juste pour voir l'email
```

### Problème: Le serveur ne démarre pas

**Erreur: "Address already in use"**
- Un autre serveur utilise le port
- Solution: Change le port avec `--port 9000`

**Erreur: "Permission denied"**
- Tu n'as pas les droits
- Solution: Utilise un port > 1024

---

## EXEMPLES D'UTILISATION

### Scénario 1: Test basique en local

**Objectif:** Tester comment marche le phishing sur ton propre PC.

1. **Lance le serveur:**
   ```bash
   python src/phishing_server.py --host 127.0.0.1
   ```

2. **Ouvre ton navigateur:**
   - Va sur http://localhost:8080/login
   - Entre des faux identifiants
   - Regarde le dashboard sur http://localhost:8080/admin

3. **Résultats:**
   - Tu vois les stats en temps réel
   - Les données sont dans `data/credentials.jsonl`

### Scénario 2: Envoyer un email de test à toi-même

**Objectif:** Tester le processus complet email → clic → capture.

1. **Configure Gmail (vois section ci-dessus)**

2. **Lance le serveur:**
   ```bash
   python src/phishing_server.py
   ```

3. **Envoie l'email:**
   ```bash
   python src/email_sender.py \
     --template password_reset \
     --to ton-email@gmail.com \
     --from security@company.com \
     --phishing-url http://localhost:8080/track/test \
     --smtp-server smtp.gmail.com \
     --smtp-port 587 \
     --username ton-email@gmail.com \
     --password ton-mot-de-passe-app
   ```

4. **Vérifie ton email:**
   - Tu reçois un email
   - Clique sur le lien
   - Entre des identifiants
   - Regarde le dashboard admin

### Scénario 3: Tester sur ton téléphone (même réseau WiFi)

**Objectif:** Voir comment ça marche sur mobile.

1. **Trouve ton IP locale:**
   - Windows: `ipconfig` (cherche "IPv4")
   - Mac/Linux: `ifconfig` ou `ip addr`
   - Exemple: `192.168.1.50`

2. **Lance le serveur:**
   ```bash
   python src/phishing_server.py --host 0.0.0.0
   ```

3. **Sur ton téléphone:**
   - Connecte-toi au même WiFi
   - Ouvre le navigateur
   - Va sur `http://192.168.1.50:8080/login` (remplace par ton IP)
   - Teste!

---

## COMMANDES UTILES

### Lancer le serveur
```bash
# Basique
python src/phishing_server.py

# Local uniquement (plus sûr)
python src/phishing_server.py --host 127.0.0.1

# Port personnalisé
python src/phishing_server.py --port 5000

# Combiné
python src/phishing_server.py --host 127.0.0.1 --port 9000
```

### Prévisualiser les emails
```bash
# Tous les templates disponibles
python src/email_sender.py --template password_reset --preview
python src/email_sender.py --template security_alert --preview
python src/email_sender.py --template account_verification --preview
python src/email_sender.py --template mfa_setup --preview
python src/email_sender.py --template invoice --preview

# Avec URL personnalisée
python src/email_sender.py --template password_reset --preview --phishing-url http://mon-site.com/track/abc
```

### Envoyer un email
```bash
python src/email_sender.py \
  --template password_reset \
  --to cible@example.com \
  --from expediteur@company.com \
  --phishing-url http://localhost:8080/track/campagne1 \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username ton-email@gmail.com \
  --password ton-mot-de-passe
```

---

## SÉCURITÉ ET ÉTHIQUE

### Règles d'or

1. **Teste SEULEMENT sur tes propres comptes**
2. **Ne piège JAMAIS quelqu'un sans son autorisation**
3. **Garde les données capturées privées**
4. **Supprime les données après tes tests**
5. **N'utilise pas en production**

### Pourquoi c'est important?

**Légalement:**
- Le phishing est ILLÉGAL dans presque tous les pays
- Tu peux aller en prison
- Tu peux avoir une amende énorme
- Ton dossier sera taché à vie

**Éthiquement:**
- C'est pas cool de piéger les gens
- Tu peux causer du stress/perte d'argent
- Ça détruit la confiance

### Utilisation autorisée

✅ **OK:**
- Tests sur tes propres emails
- Devoir d'école avec supervision
- CTF (Capture The Flag) competitions
- Recherche académique approuvée
- Tests d'intrusion avec contrat signé

❌ **PAS OK:**
- Piéger tes amis/famille
- Tester sur de vraies personnes
- Utiliser les données capturées
- Partager sans autorisation

---

## FAQ (QUESTIONS FRÉQUENTES)

### Q: Est-ce que c'est légal?

**R:** OUI, si tu l'utilises SEULEMENT pour apprendre et tester sur tes propres comptes. NON si tu l'utilises sur de vraies personnes sans autorisation.

### Q: Ça marche vraiment?

**R:** Oui! C'est exactement comment marchent les vraies attaques de phishing. C'est pour ça que c'est important de l'apprendre (pour te protéger).

### Q: Puis-je capturer de vrais identifiants?

**R:** Techniquement oui, mais MORALEMENT et LÉGALEMENT non. N'utilise ça que pour des tests éducatifs.

### Q: Comment me protéger du phishing?

**R:** Maintenant que tu sais comment ça marche:
- Vérifie TOUJOURS l'URL (le vrai domaine)
- Ne clique jamais sur des liens dans les emails
- Utilise la 2FA partout
- Tape les URLs manuellement
- Méfie-toi des emails urgents

### Q: Puis-je modifier le code?

**R:** Absolument! C'est même encouragé. Apprends en modifiant:
- Change les couleurs des pages
- Ajoute de nouveaux templates d'email
- Améliore le dashboard
- Ajoute des statistiques

### Q: Puis-je partager ce projet?

**R:** Oui, mais avec les avertissements! Ne partage jamais:
- Des identifiants capturés
- Des vraies campagnes
- Avec quelqu'un qui pourrait mal l'utiliser

### Q: Ça marche sur un vrai domaine?

**R:** Oui, tu pourrais l'héberger sur un VPS (serveur), mais c'est dangereux et probablement illégal si tu captures de vraies données.

### Q: Puis-je contourner la 2FA?

**R:** Ce framework SIMULE un contournement en capturant le code 2FA quand l'utilisateur l'entre. Mais:
- Les vrais codes 2FA expirent en 30-60 secondes
- Tu ne peux pas te connecter automatiquement
- C'est juste pour montrer la technique

### Q: Quelle est la prochaine étape pour apprendre?

**R:**
1. Apprends plus de Python
2. Étudie le HTML/CSS/JavaScript
3. Apprends les bases de réseau (TCP/IP, HTTP)
4. Étudie la sécurité offensive et défensive
5. Participe à des CTF (Capture The Flag)
6. Prends des cours de cybersécurité
7. Obtiens des certifications (CEH, OSCP, etc.)

---

## RESSOURCES POUR APPRENDRE

### Cybersécurité générale
- **TryHackMe**: https://tryhackme.com (super pour débutants!)
- **HackTheBox**: https://hackthebox.com (un peu plus difficile)
- **OverTheWire**: https://overthewire.org (wargames gratuits)
- **PicoCTF**: https://picoctf.org (CTF pour étudiants)

### Python
- **Python.org tutoriel**: https://docs.python.org/3/tutorial/
- **Automate the Boring Stuff**: https://automatetheboringstuff.com/
- **Real Python**: https://realpython.com/

### Social Engineering
- **The Art of Deception** par Kevin Mitnick (livre)
- **Social Engineering: The Science of Human Hacking** (livre)

### Éthique
- **EC-Council CEH**: Certified Ethical Hacker
- **Code of Ethics**: Comprends les lois locales

---

## SUPPORT ET AIDE

### Si tu es bloqué:

1. **Relis ce guide** (sérieusement, la solution est probablement là)
2. **Vérifie les erreurs** dans le terminal
3. **Google l'erreur** (copie-colle le message d'erreur)
4. **Demande à ton prof** (il t'a donné ce devoir après tout!)

### Problèmes communs et solutions rapides:

| Problème | Solution Rapide |
|----------|----------------|
| Port déjà utilisé | Utilise `--port 9000` |
| Module introuvable | Lance `pip install -r requirements.txt` |
| Email ne s'envoie pas | Vérifie mot de passe d'application Gmail |
| Serveur ne démarre pas | Vérifie que tu es dans le bon dossier |
| Page blanche dans le navigateur | Vérifie l'URL: `http://localhost:8080/login` |

---

## CHECKLIST AVANT DE COMMENCER

Coche chaque étape:

- [ ] J'ai lu TOUTE la section "SUPER IMPORTANT"
- [ ] Je comprends que c'est UNIQUEMENT éducatif
- [ ] J'ai Python 3.8+ installé
- [ ] J'ai installé les dépendances (`pip install -r requirements.txt`)
- [ ] J'ai testé le serveur en local
- [ ] Je vais tester SEULEMENT sur mes propres comptes
- [ ] Je ne vais PAS piéger de vraies personnes
- [ ] Je vais supprimer les données après mes tests
- [ ] Je comprends les risques légaux

---

## CONCLUSION

Félicitations! Tu as maintenant un framework de phishing éducatif complet.

**Ce que tu as appris:**
- Comment fonctionne le phishing
- Comment créer un serveur web avec Python
- Comment envoyer des emails avec SMTP
- Les bases du social engineering
- Comment te protéger contre ces attaques

**Prochaines étapes:**
1. Teste le framework
2. Modifie le code
3. Crée tes propres templates
4. Partage avec ton prof/classe (avec supervision!)
5. Continue d'apprendre la cybersécurité

**N'oublie jamais:**
> "With great power comes great responsibility"
> (Avec un grand pouvoir vient une grande responsabilité)

Tu as maintenant les connaissances pour pirater. Utilise-les pour:
- Apprendre
- Te protéger
- Protéger les autres
- Améliorer la sécurité

**PAS pour:**
- Faire du mal
- Voler
- Piéger les gens

Bonne chance dans ton apprentissage de la cybersécurité! 🚀

---

**Créé avec ❤️ pour les étudiants en cybersécurité**
**Version 2.0 - Janvier 2026**
