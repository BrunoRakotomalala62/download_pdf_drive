import os
import re
import requests
import json
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
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        
        # Tentative d'extraction Moviebox : On cherche les données JSON injectées dans la page
        # Souvent dans window.__INITIAL_STATE__ ou via des regex sur les IDs
        
        # 1. Recherche directe de liens .mp4 ou .m3u8 dans le code source
        links = re.findall(r'https?://[^\s"\']+\.(?:mp4|m3u8)[^\s"\']*', html)
        if links:
            return redirect(links[0])
            
        # 2. Recherche de l'ID de ressource et appel à l'API présumée
        res_id_match = re.search(r'id=(\d+)', url)
        if res_id_match:
            res_id = res_id_match.group(1)
            # Hypothèse d'API Moviebox (basé sur les patterns courants)
            api_url = f"https://filmboom.top/api/video/getUrl?id={res_id}&type=movie"
            try:
                api_res = requests.get(api_url, headers=headers, timeout=5)
                data = api_res.json()
                if data.get('data', {}).get('url'):
                    return redirect(data['data']['url'])
            except:
                pass

        # 3. Analyse des scripts pour trouver des variables de configuration
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup.find_all('script'):
            if script.string:
                # Recherche de patterns de liens de streaming
                m = re.search(r'["\'](https?://[^\s"\']+\.mp4[^\s"\']*)["\']', script.string)
                if m:
                    return redirect(m.group(1))

        return "La vidéo est protégée ou nécessite une session active. Essayez de maintenir le doigt sur la vidéo dans votre navigateur pour utiliser l'option de téléchargement native.", 404
        
    except Exception as e:
        return f"Erreur : {str(e)}", 500

@app.route('/')
def index():
    return "API Drive & Scraper active."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
