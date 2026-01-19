# Advanced Phishing Framework

## Features

### Phishing Server
- **Realistic Login Pages**: Professional-looking credential capture pages
- **MFA Simulation**: Two-factor authentication bypass demonstration
- **Campaign Management**: Track multiple phishing campaigns
- **Admin Dashboard**: Real-time statistics and reporting
- **Link Tracking**: Monitor who clicks phishing links
- **Credential Logging**: Secure storage of captured data

### Email Templates
Pre-built social engineering templates:
- Password reset requests
- Account verification alerts
- Security warnings
- MFA enrollment
- Invoice/billing notifications

### Email Sender
- SMTP integration for email delivery
- Template customization
- Bulk campaign sending
- Email preview mode
- Target list management

## Installation

```bash
cd phishing-framework
pip install -r requirements.txt
```

## Usage

### 1. Start Phishing Server

```bash
python src/phishing_server.py --host 0.0.0.0 --port 8080
```

The server will start with:
- **Phishing page**: `http://localhost:8080/login`
- **Admin dashboard**: `http://localhost:8080/admin`
- **Tracking links**: `http://localhost:8080/track/{campaign_id}`

### 2. Preview Email Templates

```bash
# Preview password reset template
python src/email_sender.py --template password_reset --preview

# Preview with custom phishing URL
python src/email_sender.py --template security_alert --preview --phishing-url http://yourserver.com/track/test
```

### 3. Send Phishing Emails (requires SMTP)

```bash
# Send single test email
python src/email_sender.py \
  --template password_reset \
  --to target@example.com \
  --from security@company.com \
  --phishing-url http://yourserver.com/track/campaign1 \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your-email@gmail.com \
  --password your-app-password
```

## Architecture

```
┌─────────────────┐
│  Target User    │
└────────┬────────┘
         │ 1. Receives phishing email
         ▼
┌─────────────────┐
│ Phishing Email  │
└────────┬────────┘
         │ 2. Clicks link
         ▼
┌─────────────────┐
│  Tracking URL   │ ──► Logs click, user-agent, IP
└────────┬────────┘
         │ 3. Redirects to login
         ▼
┌─────────────────┐
│  Fake Login     │
│     Page        │
└────────┬────────┘
         │ 4. Submits credentials
         ▼
┌─────────────────┐
│ Credential      │ ──► Logs username & password
│   Capture       │
└────────┬────────┘
         │ 5. Shows MFA page
         ▼
┌─────────────────┐
│   MFA Page      │
└────────┬────────┘
         │ 6. Submits MFA code
         ▼
┌─────────────────┐
│ MFA Capture     │ ──► Logs MFA token
└────────┬────────┘
         │ 7. Redirects
         ▼
┌─────────────────┐
│ Legitimate Site │
└─────────────────┘
```

## Email Templates

### Available Templates

1. **password_reset**: Urgency-based password reset
2. **account_verification**: Account suspension threat
3. **security_alert**: Unusual activity notification
4. **mfa_setup**: Mandatory 2FA enrollment
5. **invoice**: Overdue payment notice

### Template Variables

All templates support:
- `{name}` - Recipient name
- `{company}` - Company name
- `{phishing_link}` - Tracking/phishing URL
- `{timestamp}` - Current timestamp
- Plus template-specific variables

## Admin Dashboard

Access at `http://localhost:8080/admin`

Features:
- 📊 Campaign statistics
- 👥 Victim tracking
- 🔗 Click analytics
- 🔐 Credential captures
- 📈 Real-time updates

## File Structure

```
phishing-framework/
├── src/
│   ├── phishing_server.py   # Main phishing server
│   └── email_sender.py       # Email campaign manager
├── templates/
│   ├── login.html            # Credential capture page
│   └── mfa.html              # MFA capture page
├── static/                   # Static assets (CSS, JS, images)
├── data/
│   └── credentials.jsonl     # Captured data (auto-created)
└── requirements.txt
```

## Captured Data Format

Data is stored in `data/credentials.jsonl`:

```json
{"timestamp": "2024-01-15T10:30:00", "ip": "192.168.1.100", "username": "user@example.com", "password": "captured_pass", "campaign_id": "test"}
{"timestamp": "2024-01-15T10:30:15", "ip": "192.168.1.100", "username": "user@example.com", "mfa_code": "123456", "campaign_id": "test"}
```

## SMTP Configuration

### Gmail (with App Password)

1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use these settings:
   - Server: `smtp.gmail.com`
   - Port: `587`
   - Username: your Gmail address
   - Password: generated app password

### Other SMTP Providers

- **Office 365**: `smtp.office365.com:587`
- **SendGrid**: `smtp.sendgrid.net:587`
- **Mailgun**: `smtp.mailgun.org:587`

## Security Awareness Training

This framework is ideal for:

### 1. Simulated Phishing Campaigns
- Test employee awareness
- Measure click rates
- Identify high-risk users
- Track improvement over time

### 2. Training Scenarios
- Demonstrate social engineering tactics
- Show credential harvesting techniques
- Illustrate MFA bypass methods
- Teach red flags to watch for

### 3. Red Team Exercises
- Authorized penetration testing
- Security control validation
- Incident response practice
- Defense testing

## Detection & Prevention

### How to Detect Phishing

1. **Check URL carefully**
   - Look for misspellings
   - Verify HTTPS and certificate
   - Check domain ownership

2. **Examine email headers**
   - Sender's actual email address
   - SPF/DKIM/DMARC validation
   - Reply-to address

3. **Look for red flags**
   - Urgency and threats
   - Generic greetings
   - Poor grammar/spelling
   - Suspicious attachments/links

4. **Hover before clicking**
   - Check link destination
   - Use link scanners
   - Type URLs manually

### Defense Mechanisms

1. **Email Security**
   - SPF, DKIM, DMARC implementation
   - Anti-phishing filters
   - Link rewriting/sandboxing
   - Attachment scanning

2. **User Training**
   - Regular awareness training
   - Simulated phishing tests
   - Reporting mechanisms
   - Security culture

3. **Technical Controls**
   - Multi-factor authentication
   - Password managers
   - Browser extensions (anti-phishing)
   - Network security (DNS filtering)

4. **Organizational**
   - Security policies
   - Incident response procedures
   - Reporting channels
   - Regular audits

## Customization

### Create Custom Templates

Edit `src/email_sender.py` and add to `EmailTemplate.TEMPLATES`:

```python
"custom_template": {
    "subject": "Your Subject Here",
    "body": """
Your email body with {variables}

{phishing_link}
    """
}
```

### Modify Login Pages

Edit `templates/login.html` and `templates/mfa.html` to match:
- Corporate branding
- Specific services (Office 365, Gmail, etc.)
- Custom workflows

## Testing Safely

### Internal Test Environment

```bash
# 1. Start server on internal network only
python src/phishing_server.py --host 127.0.0.1 --port 8080

# 2. Send test email to yourself
python src/email_sender.py --template password_reset --to your-email@company.com --preview

# 3. Monitor admin dashboard
# Visit http://localhost:8080/admin
```

### Best Practices

1. ✅ Get written authorization
2. ✅ Define clear scope
3. ✅ Use isolated test environment
4. ✅ Notify stakeholders
5. ✅ Have incident response ready
6. ✅ Conduct post-exercise debriefs
7. ✅ Secure all captured data
8. ✅ Delete data after exercise

## Legal Considerations

### Required Authorizations

- **Penetration Testing**: Written scope and authorization
- **Security Training**: Organizational approval
- **Research**: Ethical review board approval
- **Red Team Exercise**: Formal engagement letter

### Laws to Consider

- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK
- Similar laws in your jurisdiction
- Privacy regulations (GDPR, CCPA, etc.)
- Industry-specific regulations

## Ethical Guidelines

1. **Only test authorized targets**
2. **Respect privacy and data protection**
3. **Secure all captured information**
4. **Provide educational value**
5. **Report findings responsibly**
6. **Delete data after completion**
7. **Don't cause harm or disruption**

## Reporting

After a campaign, generate reports showing:
- Click-through rates
- Credential submission rates
- MFA bypass rates
- User awareness levels
- Improvement recommendations
- Training effectiveness

## Limitations

This framework:
- ✅ Demonstrates phishing techniques
- ✅ Captures credentials and MFA codes
- ✅ Tracks campaign effectiveness
- ❌ Does NOT provide actual MFA bypass
- ❌ Does NOT access real accounts
- ❌ Does NOT include malware/exploits

## Alternatives

For production use, consider:
- [GoPhish](https://getgophish.com/) - Open-source phishing framework
- [King Phisher](https://github.com/securestate/king-phisher) - Phishing campaign toolkit
- [Social-Engineer Toolkit](https://github.com/trustedsec/social-engineer-toolkit) - SET framework
- Commercial solutions (KnowBe4, Proofpoint, etc.)

## Learning Objectives

This project teaches:
- Social engineering tactics
- Credential harvesting techniques
- MFA limitations
- Email spoofing
- Web application design for phishing
- Campaign management
- Security awareness importance

## Contributing

Focus on:
- New email templates
- Additional login page designs
- Improved tracking features
- Better reporting
- Enhanced stealth techniques (educational)

## References

- [OWASP Phishing](https://owasp.org/www-community/attacks/Phishing)
- [SANS Security Awareness](https://www.sans.org/security-awareness-training/)
- [Anti-Phishing Working Group](https://apwg.org/)
- [Social Engineering Framework](https://www.social-engineer.org/)

## Legal Notice

**UNAUTHORIZED USE IS ILLEGAL**

This tool is for educational and authorized testing only. Phishing attacks without authorization are illegal in most jurisdictions and can result in:
- Criminal prosecution
- Civil lawsuits
- Financial penalties
- Imprisonment

Always obtain explicit written permission before conducting any phishing simulation.

---

**Remember**: The goal is to improve security, not to harm. Use responsibly and ethically.
