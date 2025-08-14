# Hostinger Deployment Guide

## Option 1: VPS Hosting (Full-Stack)

### Prerequisites
- Hostinger VPS plan
- SSH access to server
- Domain name (optional)

### Step 1: Prepare Files for Upload
```bash
# Create deployment package
zip -r housing-app.zip . -x "__pycache__/*" "*.pyc" ".git/*"
```

### Step 2: Server Setup
1. Connect to VPS via SSH
2. Install Python and pip:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

3. Create application directory:
```bash
sudo mkdir /var/www/housing-app
sudo chown $USER:$USER /var/www/housing-app
cd /var/www/housing-app
```

4. Upload and extract files:
```bash
# Upload housing-app.zip to server, then:
unzip housing-app.zip
```

5. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Set environment variables:
```bash
nano .env
# Add: CENSUS_API_KEY=your_key_here
```

### Step 3: Configure Nginx
Create `/etc/nginx/sites-available/housing-app`:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or server IP

    # Serve static files
    location / {
        root /var/www/housing-app;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/housing-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Setup Systemd Service
Create `/etc/systemd/system/housing-app.service`:
```ini
[Unit]
Description=Housing Data API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/housing-app
Environment=PATH=/var/www/housing-app/venv/bin
ExecStart=/var/www/housing-app/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable housing-app
sudo systemctl start housing-app
```

---

## Option 2: Web Hosting + External API

### Step 1: Deploy API to Render.com (Free)
1. Push code to GitHub
2. Create Render account
3. Connect GitHub repository
4. Deploy as Web Service

### Step 2: Update Frontend for Production
Update API endpoint in index.html:
```javascript
const API_ENDPOINT = "https://your-app.onrender.com/api/housing-data/";
```

### Step 3: Upload to Hostinger Web Hosting
1. Use File Manager or FTP
2. Upload these files to public_html:
   - index.html
   - Any CSS/JS files
   - Images/assets

### Step 4: Access Your App
Visit: https://yourdomain.com

---

## SSL Certificate (Optional)
For HTTPS, use Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Monitoring
- Check logs: `sudo journalctl -u housing-app -f`
- Monitor API: `curl http://localhost:8000/`
- Nginx logs: `/var/log/nginx/access.log`
