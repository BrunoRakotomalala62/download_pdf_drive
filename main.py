from flask import Flask, request, redirect
import re

app = Flask(__name__)

def get_drive_id(url):
    # Extract ID from various Google Drive URL formats
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

@app.route('/download')
def download():
    pdf_url = request.args.get('pdf')
    if not pdf_url:
        return "Missing pdf parameter", 400
    
    file_id = get_drive_id(pdf_url)
    if not file_id:
        return "Invalid Google Drive URL", 400
    
    # Direct download link for Google Drive
    # The 'uc' endpoint triggers a direct download
    direct_link = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    return redirect(direct_link)

@app.route('/')
def index():
    return "Google Drive PDF Direct Downloader API is running. Use /download?pdf=URL"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
