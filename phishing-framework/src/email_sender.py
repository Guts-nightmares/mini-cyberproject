"""
Advanced Phishing Framework - Email Sender
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This module handles phishing email generation and sending.
NEVER use this on real targets without explicit authorization.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailTemplate:
    """Email template for phishing campaigns"""

    # Pre-built templates
    TEMPLATES = {
        "password_reset": {
            "subject": "Password Reset Required - Action Needed",
            "body": """
Dear {name},

We have detected unusual activity on your account. For security reasons, we require you to reset your password immediately.

Click here to reset your password:
{phishing_link}

This link will expire in 24 hours.

If you did not request this password reset, please contact our security team immediately.

Best regards,
Security Team
{company}

---
This is an automated message. Please do not reply to this email.
            """
        },
        "account_verification": {
            "subject": "Verify Your Account - Urgent",
            "body": """
Hello {name},

Your account verification is incomplete. Please verify your account to avoid suspension.

Verify your account here:
{phishing_link}

Failure to verify within 48 hours will result in account suspension.

Thank you,
Account Security Team
{company}
            """
        },
        "security_alert": {
            "subject": "Security Alert: Unusual Sign-in Activity",
            "body": """
Hi {name},

We detected a sign-in attempt from an unrecognized device:

Location: {fake_location}
Device: {fake_device}
Time: {timestamp}

If this was you, please verify your identity:
{phishing_link}

If this wasn't you, secure your account immediately.

Security Team
{company}
            """
        },
        "mfa_setup": {
            "subject": "Action Required: Enable Two-Factor Authentication",
            "body": """
Dear {name},

As part of our enhanced security measures, all accounts must enable two-factor authentication by {deadline}.

Enable 2FA now:
{phishing_link}

Accounts without 2FA will be temporarily suspended after the deadline.

Thank you for your cooperation,
IT Security
{company}
            """
        },
        "invoice": {
            "subject": "Invoice #{invoice_number} - Payment Overdue",
            "body": """
Hello {name},

Your invoice #{invoice_number} is now overdue. Please review and make payment immediately to avoid service interruption.

View Invoice:
{phishing_link}

Amount Due: ${amount}
Due Date: {due_date}

Questions? Contact our billing department.

Accounts Receivable
{company}
            """
        }
    }

    @classmethod
    def get_template(cls, template_name: str) -> dict:
        """Get email template by name"""
        return cls.TEMPLATES.get(template_name, cls.TEMPLATES["password_reset"])

    @classmethod
    def format_email(cls, template_name: str, **kwargs) -> tuple:
        """Format email with provided variables"""
        template = cls.get_template(template_name)

        # Default values
        defaults = {
            'name': 'User',
            'company': 'Company Inc.',
            'phishing_link': 'http://example.com/phishing',
            'fake_location': 'Unknown Location',
            'fake_device': 'Unknown Device',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'deadline': '2024-01-31',
            'invoice_number': '12345',
            'amount': '99.99',
            'due_date': '2024-01-15'
        }

        # Merge with provided kwargs
        defaults.update(kwargs)

        subject = template['subject'].format(**defaults)
        body = template['body'].format(**defaults)

        return subject, body


class PhishingEmailSender:
    """Send phishing emails (for authorized testing)"""

    def __init__(self, smtp_server: str = None, smtp_port: int = 587,
                 username: str = None, password: str = None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

        logger.warning("=" * 60)
        logger.warning("⚠️  PHISHING EMAIL SENDER")
        logger.warning("⚠️  FOR AUTHORIZED TESTING ONLY")
        logger.warning("=" * 60)

    def create_email(self, from_addr: str, to_addr: str, subject: str,
                    body: str, html: bool = False) -> MIMEMultipart:
        """Create email message"""
        msg = MIMEMultipart('alternative')
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        return msg

    def send_email(self, from_addr: str, to_addr: str, subject: str,
                  body: str, html: bool = False) -> bool:
        """Send single email"""
        if not self.smtp_server:
            logger.error("SMTP server not configured")
            return False

        try:
            msg = self.create_email(from_addr, to_addr, subject, body, html)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"📧 Email sent to {to_addr}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False

    def send_campaign(self, campaign_id: str, template_name: str,
                     targets: List[dict], phishing_url: str,
                     from_addr: str = "security@company.com") -> dict:
        """Send phishing campaign to multiple targets"""
        results = {
            'sent': 0,
            'failed': 0,
            'targets': []
        }

        for target in targets:
            # Format email with target-specific variables
            target_vars = {
                'name': target.get('name', 'User'),
                'phishing_link': f"{phishing_url}?c={campaign_id}&t={target.get('email')}",
                'company': target.get('company', 'Company Inc.')
            }

            subject, body = EmailTemplate.format_email(template_name, **target_vars)

            # Send email
            success = self.send_email(from_addr, target['email'], subject, body)

            results['targets'].append({
                'email': target['email'],
                'sent': success,
                'timestamp': datetime.now().isoformat()
            })

            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1

        logger.info(f"📊 Campaign complete: {results['sent']} sent, {results['failed']} failed")
        return results

    def preview_email(self, template_name: str, **kwargs):
        """Preview email without sending"""
        subject, body = EmailTemplate.format_email(template_name, **kwargs)

        print("\n" + "=" * 60)
        print("EMAIL PREVIEW")
        print("=" * 60)
        print(f"Template: {template_name}")
        print(f"Subject: {subject}")
        print("\nBody:")
        print("-" * 60)
        print(body)
        print("-" * 60 + "\n")


def main():
    """Main function for testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Phishing Email Sender")
    parser.add_argument("--template", default="password_reset",
                       choices=list(EmailTemplate.TEMPLATES.keys()),
                       help="Email template to use")
    parser.add_argument("--preview", action="store_true",
                       help="Preview email without sending")
    parser.add_argument("--to", help="Target email address")
    parser.add_argument("--from", dest="from_addr",
                       default="security@company.com",
                       help="Sender email address")
    parser.add_argument("--phishing-url",
                       default="http://localhost:8080/track/test",
                       help="Phishing link URL")
    parser.add_argument("--smtp-server", help="SMTP server")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP port")
    parser.add_argument("--username", help="SMTP username")
    parser.add_argument("--password", help="SMTP password")

    args = parser.parse_args()

    sender = PhishingEmailSender(
        smtp_server=args.smtp_server,
        smtp_port=args.smtp_port,
        username=args.username,
        password=args.password
    )

    # Preview mode
    if args.preview:
        sender.preview_email(
            args.template,
            phishing_link=args.phishing_url
        )
        return

    # Send mode
    if not args.to:
        print("Error: --to email address required")
        return

    subject, body = EmailTemplate.format_email(
        args.template,
        phishing_link=args.phishing_url
    )

    sender.send_email(args.from_addr, args.to, subject, body)


if __name__ == "__main__":
    main()
