from flask import Flask, request, redirect
import re

app = Flask(__name__)

def get_drive_id(url_or_id):
    # If it's already just an ID (no slashes or equals), return it
    if url_or_id and not any(c in url_or_id for c in '/='):
        return url_or_id
        
    # Extract ID from various Google Drive URL formats
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)
    return None

@app.route('/download')
def download():
    pdf_param = request.args.get('pdf')
    if not pdf_param:
        return "Missing pdf parameter", 400
    
    file_id = get_drive_id(pdf_param)
    if not file_id:
        return "Invalid Google Drive URL or ID", 400
    
    # Direct download link for Google Drive
    direct_link = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    return redirect(direct_link)

@app.route('/')
def index():
    return "Google Drive PDF Direct Downloader API is running. Use /download?pdf=ID_OU_URL"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
