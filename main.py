import os
import re
import requests
from flask import Flask, request, redirect, jsonify, render_template_string
from bs4 import BeautifulSoup

app = Flask(__name__)

DRIVE_DIR = 'drive'

# Template HTML pour la page d'accueil
HTML_GUIDE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drive & Video Downloader API</title>
    <style>
        :root {
            --primary: #00f2fe;
            --secondary: #4facfe;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .container {
            background: var(--card);
            padding: 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            max-width: 700px;
            width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        h1 {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
        }
        .feature {
            background: rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            text-align: left;
            border-left: 4px solid var(--primary);
        }
        .feature h2 {
            margin-top: 0;
            color: var(--primary);
            font-size: 1.2rem;
        }
        code {
            background: #000;
            padding: 0.2rem 0.5rem;
            border-radius: 0.3rem;
            color: #ec4899;
            font-family: monospace;
        }
        .example-link {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.8rem 1.5rem;
            background: linear-gradient(to right, #00f2fe, #4facfe);
            color: white;
            text-decoration: none;
            border-radius: 0.75rem;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .example-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(79, 172, 254, 0.4);
        }
        .badge {
            background: #22c55e;
            padding: 0.2rem 0.6rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 API Downloader Pro</h1>
        
        <div class="feature">
            <h2>📁 Recherche PDF Drive <span class="badge">Actif</span></h2>
            <p>Recherchez vos fichiers par nom dans la base de données locale.</p>
            <code>/recherche?pdf=math</code>
        </div>

        <div class="feature">
            <h2>📥 Téléchargement PDF <span class="badge">Direct</span></h2>
            <p>Téléchargez via le numéro d'index ou l'URL complète.</p>
            <code>/download?pdf=1</code>
        </div>

        <div class="feature">
            <h2>🎬 Scraper Vidéo Moviebox <span class="badge">Beta</span></h2>
            <p>Récupérez le lien direct d'une vidéo Filmboom/Moviebox.</p>
            <code>/scraper_video?url=[URL]</code>
        </div>

        <a href="/recherche?pdf=math" class="example-link">Tester un exemple de recherche 🔍</a>
        <br>
        <a href="/download?pdf=1" class="example-link" style="margin-top: 10px; background: linear-gradient(to right, #f472b6, #db2777);">Tester le téléchargement direct 📥</a>
    </div>
</body>
</html>
"""

def get_drive_files():
    files = []
    if not os.path.exists(DRIVE_DIR):
        return files
    
    filenames = sorted([f for f in os.listdir(DRIVE_DIR) if f.endswith('.txt')])
    
    for filename in filenames:
        path = os.path.join(DRIVE_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                entries = re.findall(r'nom\s*:\s*(.*?)\s*uid\s*:\s*"(.*?)"', content, re.DOTALL)
                for name, uid in entries:
                    files.append({
                        'nom': name.strip(),
                        'uid': uid.strip()
                    })
        except Exception:
            continue
    return files

@app.route('/recherche')
def recherche():
    query = request.args.get('pdf', '').lower()
    all_files = get_drive_files()
    
    results = []
    for i, f in enumerate(all_files, 1):
        if query in f['nom'].lower():
            results.append(f"{i}-{f['nom']}")
            
    return jsonify(results)

@app.route('/download')
def download():
    pdf_param = request.args.get('pdf')
    if not pdf_param:
        return "Missing pdf parameter", 400
    
    file_id = None
    
    if pdf_param.isdigit():
        all_files = get_drive_files()
        idx = int(pdf_param) - 1
        if 0 <= idx < len(all_files):
            file_id = all_files[idx]['uid']
        else:
            return "Numéro de fichier invalide", 404
    else:
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', pdf_param)
        if match:
            file_id = match.group(1)
        else:
            match = re.search(r'id=([a-zA-Z0-9_-]+)', pdf_param)
            if match:
                file_id = match.group(1)
            elif not any(c in pdf_param for c in '/='):
                file_id = pdf_param

    if not file_id:
        return "Fichier non trouvé ou ID invalide", 400
    
    direct_link = f'https://drive.google.com/uc?export=download&id={file_id}'
    return redirect(direct_link)

@app.route('/scraper_video')
def scraper_video():
    url = request.args.get('url')
    if not url:
        return "Missing url parameter", 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
            'Referer': 'https://filmboom.top/',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        
        links = re.findall(r'https?://[^\s"\']+\.(?:mp4|m3u8)[^\s"\']*', html)
        if links:
            return redirect(links[0])
            
        res_id_match = re.search(r'id=(\d+)', url)
        if res_id_match:
            res_id = res_id_match.group(1)
            api_url = f"https://filmboom.top/api/video/getUrl?id={res_id}&type=movie"
            try:
                api_res = requests.get(api_url, headers=headers, timeout=5)
                data = api_res.json()
                if data.get('data', {}).get('url'):
                    return redirect(data['data']['url'])
            except:
                pass

        soup = BeautifulSoup(html, 'html.parser')
        for script in soup.find_all('script'):
            if script.string:
                m = re.search(r'["\'](https?://[^\s"\']+\.mp4[^\s"\']*)["\']', script.string)
                if m:
                    return redirect(m.group(1))

        return "La vidéo est protégée ou nécessite une session active.", 404
        
    except Exception as e:
        return f"Erreur : {str(e)}", 500

@app.route('/')
def index():
    return render_template_string(HTML_GUIDE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
