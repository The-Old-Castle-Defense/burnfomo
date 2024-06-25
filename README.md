# $FOMO is the first fully transparent & on-chain MEME and Community token on Base powered by TOCD Studio ([https://theoldcastle.xyz](https://theoldcastle.xyz))

<code>[burnfomo.theoldcastle.xyz](https://burnfomo.theoldcastle.xyz/) - Find out how many FOMO tokens have already been burned! See how many FOMO boughtback and are waiting to get burned. We're inspired by the Best - copied and redesigned from burnbeam.com by the Merit Circle & Beam blockchain.</code>

# BURN $FOMO Tracker Deployment

This repository contains the code for tracking BURN $FOMO transactions and serving statistics via a FastAPI application.

## Crontab Script Deployment

To deploy the `burnfomo_tracker.py` script with `crontab`, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-repo/burnfomo-tracker.git](https://github.com/The-Old-Castle-Defense/burnfomo.git)
   cd burnfomo-tracker
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Crontab:**
   Open the crontab editor:
   ```bash
   crontab -e
   ```

   Add the following line to run the script every 30 minutes:
   ```bash
   */30 * * * * /usr/bin/python3 /path/to/burnfomo_tracker.py
   ```

4. **Save and Exit:**
   Save the changes and exit the editor. The script will now run every 30 minutes.

## FastAPI with NGINX Deployment

To deploy the FastAPI application using NGINX, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/burnfomo-tracker.git
   cd burnfomo-tracker
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run FastAPI with Uvicorn:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 9999
   ```

4. **Set Up NGINX:**
   Edit your NGINX configuration to include:
   ```nginx
   server {
       listen 443 ssl;
       listen [::]:443 ssl;

       ssl_certificate /etc/nginx/ssl/ssl.pem;
       ssl_certificate_key /etc/nginx/ssl/ssl.key;
       server_name burnfomo.theoldcastle.xyz;

       location /api/ {
           proxy_pass http://127.0.0.1:9999;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **Restart NGINX:**
   ```bash
   sudo systemctl restart nginx
   ```
