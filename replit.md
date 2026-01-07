# PDF Drive Downloader

## Overview

This is a Flask-based web application that provides an API for downloading files from Google Drive and potentially other sources. The application serves as a download proxy/helper service, allowing users to fetch PDFs and other documents via a simple web interface or API endpoints. It's configured for deployment on Vercel as a serverless Python application.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask** serves as the core web framework
- Single-file application architecture (`main.py`) suitable for small-scale API services
- Serverless deployment target (Vercel) with `gunicorn` as the WSGI server for production

### Core Functionality
- **Web Scraping**: Uses `BeautifulSoup4` for parsing HTML content from external sources
- **HTTP Requests**: `requests` library handles external API calls and file downloads
- **File Storage**: Local `drive/` directory stores reference data (UIDs and file mappings)

### Data Storage
- **Flat File System**: Uses simple text files (`uid_pdf.txt`) to store Google Drive file mappings
- **Format**: Each entry contains a filename and corresponding Google Drive UID
- No database is currently implemented

### Image Generation (Secondary Feature)
- `matplotlib` and `Pillow` are available for generating mathematical content images
- `generate_image.py` contains logic for rendering LaTeX-style mathematical expressions
- This appears to be a supplementary feature, not the main application focus

### Deployment Configuration
- **Vercel**: Configured via `vercel.json` for serverless deployment
- All routes are directed to `main.py` as the single entry point
- Uses `@vercel/python` build system

## External Dependencies

### Python Packages
| Package | Purpose |
|---------|---------|
| Flask | Web framework and routing |
| requests | HTTP client for external downloads |
| gunicorn | Production WSGI server |
| beautifulsoup4 | HTML parsing and web scraping |
| Pillow | Image manipulation |
| matplotlib | Mathematical plotting and image generation |

### External Services
- **Google Drive**: Primary source for PDF file downloads (files referenced by UID)
- Files are accessed using Google Drive's file ID system

### Deployment Platform
- **Vercel**: Serverless hosting platform with Python runtime support