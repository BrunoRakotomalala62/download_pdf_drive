import os
import re
from flask import Flask, request, redirect, jsonify

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
                # On cherche toutes les paires nom/uid dans le fichier
                # On utilise multiline pour gérer les formats variés
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

@app.route('/')
def index():
    return "API Drive active. Utilisez /recherche?pdf=... ou /download?pdf=NUMERO"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
