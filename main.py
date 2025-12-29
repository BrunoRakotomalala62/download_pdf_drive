import os
import re
import requests
from flask import Flask, request, redirect, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

DRIVE_DIR = 'drive'

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
            'Origin': 'https://filmboom.top'
        }
        
        # 1. Obtenir la page principale
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        
        # 2. Chercher des patterns d'API Moviebox ou des liens .mp4 dans le JS
        # On cherche des URLs qui pourraient être l'API de streaming
        api_patterns = [
            r'https?://[^\s"\']+/api/video/getUrl[^\s"\']*',
            r'https?://[^\s"\']+/get_video_info[^\s"\']*',
            r'https?://[^\s"\']+\.mp4[^\s"\']*',
            r'https?://[^\s"\']+\.m3u8[^\s"\']*'
        ]
        
        found_links = []
        for pattern in api_patterns:
            matches = re.findall(pattern, html)
            found_links.extend(matches)
            
        # 3. Chercher dans les fichiers JS externes liés
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            js_url = script['src']
            if not js_url.startswith('http'):
                # Gérer les chemins relatifs
                base_url = '/'.join(url.split('/')[:3])
                js_url = base_url + js_url if js_url.startswith('/') else '/'.join(url.split('/')[:-1]) + '/' + js_url
            
            try:
                js_res = requests.get(js_url, headers=headers, timeout=5)
                for pattern in api_patterns:
                    matches = re.findall(pattern, js_res.text)
                    found_links.extend(matches)
            except:
                continue

        # Nettoyage et priorité au .mp4
        if found_links:
            # Priorité aux liens .mp4 directs
            mp4_links = [l for l in found_links if '.mp4' in l.lower()]
            if mp4_links:
                return redirect(mp4_links[0])
            
            # Sinon le premier lien trouvé
            return redirect(found_links[0])

        return "Impossible de trouver le lien direct. Le site utilise probablement une protection avancée ou un lecteur dynamique.", 404
        
    except Exception as e:
        return f"Erreur lors de l'analyse : {str(e)}", 500

@app.route('/')
def index():
    return "API Drive & Scraper active. /recherche, /download, /scraper_video"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
