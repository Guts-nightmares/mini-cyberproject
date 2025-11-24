#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReconOSINT - Outil de Reconnaissance Passive de Domaine
Auteur: Gemini
Version: 1.0
"""

import argparse
import json
import datetime
import sys
from pathlib import Path

try:
    import whois
    import dns.resolver
    import requests
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError as e:
    print(f"Erreur d'importation: {e}. Veuillez installer les dépendances requises.")
    print("Essayez: pip install requests dnspython python-whois jinja2")
    sys.exit(1)

# --- Template HTML intégré pour un script autonome ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Reconnaissance OSINT pour {{ data.domain }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; margin-top: 30px; }
        .section { margin-bottom: 25px; }
        .key { font-weight: bold; color: #34495e; min-width: 180px; display: inline-block; }
        .value { color: #555; }
        ul { list-style-type: none; padding-left: 0; }
        li { background: #ecf0f1; padding: 10px; border-radius: 4px; margin-bottom: 8px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #ddd; }
        th { background-color: #3498db; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .footer { text-align: center; margin-top: 30px; font-size: 0.9em; color: #7f8c8d; }
        .badge { background-color: #e74c3c; color: white; padding: 3px 8px; font-size: 0.8em; border-radius: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rapport OSINT pour <span class="value">{{ data.domain }}</span></h1>
        <p class="footer">Rapport généré le {{ data.report_date }}</p>

        <!-- Section WHOIS -->
        <div class="section">
            <h2><a id="whois"></a>Informations WHOIS</h2>
            {% if data.whois %}
                <ul>
                {% for key, value in data.whois.items() %}
                    <li><span class="key">{{ key }}:</span> <span class="value">{{ value | join(', ') if value is iterable and value is not string else value }}</span></li>
                {% endfor %}
                </ul>
            {% else %}
                <p>Aucune information WHOIS n'a pu être récupérée.</p>
            {% endif %}
        </div>

        <!-- Section DNS -->
        <div class="section">
            <h2><a id="dns"></a>Enregistrements DNS</h2>
            {% if data.dns_records %}
                <table id="dns-table">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Valeur</th>
                        </tr>
                    </thead>
                    <tbody>
                    {% for type, records in data.dns_records.items() %}
                        {% for record in records %}
                        <tr>
                            <td><span class="badge">{{ type }}</span></td>
                            <td>{{ record }}</td>
                        </tr>
                        {% endfor %}
                    {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <p>Aucun enregistrement DNS trouvé.</p>
            {% endif %}
        </div>

        <!-- Section Subdomains -->
        <div class="section">
            <h2><a id="subdomains"></a>Sous-domaines découverts</h2>
            {% if data.subdomains %}
                <ul>
                {% for sub in data.subdomains %}
                    <li>{{ sub }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>Aucun sous-domaine trouvé via les sources publiques.</p>
            {% endif %}
        </div>

        <!-- Section Web Technologies -->
        <div class="section">
            <h2><a id="tech"></a>Technologies Web (via en-têtes HTTP)</h2>
            {% if data.web_technologies %}
                 <ul>
                {% for key, value in data.web_technologies.items() %}
                    <li><span class="key">{{ key }}:</span> <span class="value">{{ value }}</span></li>
                {% endfor %}
                </ul>
            {% else %}
                <p>Impossible d'identifier les technologies web (le site est peut-être inaccessible ou ne retourne pas d'en-têtes pertinents).</p>
            {% endif %}
        </div>

        <div class="footer">
            Fin du rapport.
        </div>
    </div>
</body>
</html>
"

def get_whois_info(domain: str) -> dict:
    """
    #Récupère les informations WHOIS pour un domaine donné.
    """
    print(f"[*] Récupération des informations WHOIS pour {domain}...")
    try:
        w = whois.whois(domain)
        # Conversion des objets datetime en string pour la sérialisation JSON
        whois_data = {key: (val.isoformat() if isinstance(val, datetime.datetime) else val) 
                      for key, val in w.items()}
        return whois_data
    except Exception as e:
        print(f"[!] Erreur lors de la récupération du WHOIS: {e}")
        return {}

def get_dns_records(domain: str) -> dict:
    """
    #Résout les enregistrements DNS (A, MX, NS, TXT) pour un domaine.
    """
    records = {"A": [], "MX": [], "NS": [], "TXT": []}
    record_types = ["A", "MX", "NS", "TXT"]

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                if record_type == "MX":
                    records[record_type].append(f"{rdata.preference} {rdata.exchange}")
                else:
                    # Pour les enregistrements TXT, les données peuvent être en plusieurs parties
                    if record_type == 'TXT':
                         records[record_type].append("".join(s.decode() for s in rdata.strings))
                    else:
                         records[record_type].append(rdata.to_text())
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            print(f"[-] Aucun enregistrement {record_type} trouvé.")
        except Exception as e:
            print(f"[!] Erreur lors de la résolution DNS pour {record_type}: {e}")
    return records

def find_subdomains(domain: str) -> list:
    """
    #Trouve les sous-domaines en utilisant des sources publiques (crt.sh, AlienVault OTX).
    """
    print(f"[*] Recherche de sous-domaines pour {domain}...")
    subdomains = set()

    # Source 1: crt.sh
    try:
        response = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=20)
        if response.ok:
            data = response.json()
            for entry in data:
                name = entry.get("name_value")
                if name and domain in name:
                    # Ajoute les sous-domaines trouvés, en ignorant les doublons et le domaine principal
                    subdomains.update(s.strip() for s in name.split('\n') if s.strip().endswith(f".{domain}"))
    except requests.RequestException as e:
        print(f"[!] Erreur lors de la connexion à crt.sh: {e}")

    # Source 2: AlienVault OTX
    try:
        response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=20)
        if response.ok:
            data = response.json()
            for record in data.get("passive_dns", []):
                hostname = record.get("hostname")
                if hostname and hostname.endswith(f".{domain}"):
                    subdomains.add(hostname)
    except requests.RequestException as e:
        print(f"[!] Erreur lors de la connexion à AlienVault OTX: {e}")

    print(f"[+] {len(subdomains)} sous-domaines uniques trouvés.")
    return sorted(list(subdomains))

def get_web_technologies(domain: str) -> dict:
    """
    #Identifie les technologies web à partir des en-têtes HTTP.
    """
    print(f"[*] Identification des technologies web pour https://{domain}...")
    tech = {}
    headers_to_check = ["Server", "X-Powered-By", "Set-Cookie", "Content-Type", "X-AspNet-Version"]

    try:
        # Tente une connexion en HTTPS d'abord
        response = requests.get(f"https://{domain}", timeout=10, allow_redirects=True, headers={'User-Agent': 'ReconOSINT-Tool/1.0'})
    except requests.RequestException:
        try:
            # Si HTTPS échoue, tente en HTTP
            print(f"[-] HTTPS a échoué, tentative en HTTP pour http://{domain}...")
            response = requests.get(f"http://{domain}", timeout=10, allow_redirects=True, headers={'User-Agent': 'ReconOSINT-Tool/1.0'})
        except requests.RequestException as e:
            print(f"[!] Impossible de se connecter à {domain} (HTTP/HTTPS): {e}")
            return {}

    for header, value in response.headers.items():
        if header in headers_to_check:
            tech[header] = value

    return tech

def display_results(data: dict):
    """#Affiche les résultats formatés dans la console.
 """
    print("\n" + "="*50)
    print(f"RAPPORT DE RECONNAISSANCE POUR: {data['domain']}")
    print("="*50 + "\n")

    # WHOIS
    print("--- INFORMATIONS WHOIS ---")
    if data['whois']:
        for key, value in data['whois'].items():
            print(f"{key:<20}: {value}")
    else:
        print("Non disponibles.")
    print("\n")

    # DNS
    print("--- ENREGISTREMENTS DNS ---")
    if any(data['dns_records'].values()):
        for type, records in data['dns_records'].items():
            if records:
                print(f"  {type}:")
                for record in records:
                    print(f"    - {record}")
    else:
        print("Aucun trouvé.")
    print("\n")

    # Subdomains
    print("--- SOUS-DOMAINES ---")
    if data['subdomains']:
        for sub in data['subdomains']:
            print(f"  - {sub}")
    else:
        print("Aucun trouvé.")
    print("\n")

    # Web Tech
    print("--- TECHNOLOGIES WEB (En-têtes HTTP) ---")
    if data['web_technologies']:
        for key, value in data['web_technologies'].items():
            print(f"  {key:<20}: {value}")
    else:
        print("Non disponibles.")
    print("\n")


def main():
    """#Fonction principale du script.
 """
    parser = argparse.ArgumentParser(
        description="ReconOSINT - Un outil de reconnaissance passive sur un domaine.",
        epilog="Utilisation éthique uniquement. N'utilisez cet outil que sur des domaines pour lesquels vous avez une autorisation explicite."
    )
    parser.add_argument("-t", "--target", required=True, help="Le domaine cible à analyser (ex: exemple.com)")
    parser.add_argument("-o", "--output", help="Nom de base pour les fichiers de sortie (sans extension)")
    args = parser.parse_args()

    domain = args.target
    
    # Vérification simple pour éviter les "http://"
    if '://' in domain:
        print("[!] Veuillez fournir un nom de domaine et non une URL (ex: exemple.com).")
        sys.exit(1)

    results = {
        "domain": domain,
        "report_date": datetime.datetime.now().isoformat(),
        "whois": get_whois_info(domain),
        "dns_records": get_dns_records(domain),
        "subdomains": find_subdomains(domain),
        "web_technologies": get_web_technologies(domain),
    }

    display_results(results)

    # Génération des rapports si un nom de sortie est spécifié
    if args.output:
        output_base = Path(args.output)
        
        # Sauvegarde JSON
        json_file = output_base.with_suffix('.json')
        print(f"[*] Enregistrement du rapport JSON dans {json_file}...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        # Sauvegarde HTML
        html_file = output_base.with_suffix('.html')
        print(f"[*] Enregistrement du rapport HTML dans {html_file}...")
        try:
            # Utilise le template intégré comme une chaîne
            env = Environment(loader=None, autoescape=select_autoescape(['html', 'xml']))
            template = env.from_string(HTML_TEMPLATE)
            html_content = template.render(data=results)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except Exception as e:
            print(f"[!] Erreur lors de la génération du rapport HTML: {e}")

    print("\n[+] Reconnaissance terminée.")

if __name__ == "__main__":
    main()
