import requests
from bs4 import BeautifulSoup
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from colorama import Fore, init
init(autoreset=True)

class Recon:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Config.USER_AGENT})
    
    def check_vulnerable(self, url):
        print(f"{Fore.CYAN}[RECON] Fingerprinting {url}...")
        
        # Extended recon paths
        paths = [
            '/admin/', '/administrator/', '/wp-admin/', '/login.php',
            '/upload.php', '/filemanager/', '/images/', '/uploads/',
            '/manager/html', '/phpmyadmin/', '/config.php'
        ]
        
        for path in paths:
            test_url = url.rstrip('/') + path
            try:
                resp = self.session.head(test_url, timeout=5, allow_redirects=True)
                if resp.status_code in [200, 403, 301]:
                    print(f"{Fore.GREEN}[+] HIT: {test_url} ({resp.status_code})")
                    return test_url
            except:
                pass
        
        print(f"{Fore.YELLOW}[INFO] No obvious vectors, using root")
        return url