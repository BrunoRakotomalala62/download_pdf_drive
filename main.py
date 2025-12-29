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
        # Note: Scraping modern sites often requires JavaScript execution.
        # This basic scraper looks for <video> tags or mp4 links in the static HTML.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Try to find <video> tags
        video_tags = soup.find_all('video')
        for video in video_tags:
            if video.get('src'):
                return redirect(video.get('src'))
            source = video.find('source')
            if source and source.get('src'):
                return redirect(source.get('src'))
        
        # 2. Try to find links ending in .mp4
        mp4_links = soup.find_all('a', href=re.compile(r'\.mp4'))
        if mp4_links:
            return redirect(mp4_links[0].get('href'))
            
        # 3. Look inside scripts (common for hidden players)
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                match = re.search(r'(https?://[^\s"\']+\.mp4[^\s"\']*)', script.string)
                if match:
                    return redirect(match.group(1))

        return "Vidéo non trouvée sur la page (elle est peut-être chargée par JavaScript)", 404
    except Exception as e:
        return f"Erreur lors du scraping: {str(e)}", 500

@app.route('/')
def index():
    return "API active. /recherche, /download, /scraper_video"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
