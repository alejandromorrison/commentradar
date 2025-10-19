# CommentRadar Scheduling Guide

Run CommentRadar automatically every 30 minutes (or any interval) to continuously collect comments.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Built-in Scheduler](#built-in-scheduler)
3. [System Schedulers](#system-schedulers)
4. [Cloud Deployment](#cloud-deployment)
5. [Docker Setup](#docker-setup)

---

## Quick Start

### Option 1: Built-in Python Scheduler (Recommended for Development)

CommentRadar includes a built-in scheduler using the `schedule` library.

**Install the dependency:**
```bash
pip install schedule
```

**Run scheduled scraping:**
```bash
# Every 30 minutes
python -m commentradar.scheduler --topic "tech news" --interval 30 --limit 50 --analyze-sentiment

# Every hour
python -m commentradar.scheduler --topic "product reviews" --interval 60 --platform blog
```

**Using the Python API:**
```python
from commentradar.scheduler import ScheduledScraper

scheduler = ScheduledScraper(
    topic="dental clinics",
    platforms=["blog", "google"],
    output_file="dental_comments.json",
    limit=100,
    analyze_sentiment=True,
    append_mode=True  # Keeps adding to the file
)

# Run every 30 minutes
scheduler.run_every(minutes=30)
```

### Option 2: Windows Batch Script

**Quick start:**
```bash
cd batavia\scripts
run_scheduled.bat
```

**Customize:**
Edit `scripts/run_scheduled.bat` to change settings.

### Option 3: Linux/Mac Shell Script

**Make executable:**
```bash
chmod +x scripts/run_scheduled.sh
```

**Run:**
```bash
./scripts/run_scheduled.sh
```

---

## Built-in Scheduler Features

### Append Mode (Default)

Automatically merges new comments with existing data:

```python
scheduler = ScheduledScraper(
    topic="restaurant reviews",
    output_file="reviews.json",
    append_mode=True  # Adds new comments without duplicates
)
```

**Benefits:**
- ✓ Removes duplicates automatically
- ✓ Grows your dataset over time
- ✓ Preserves historical data

### Overwrite Mode

Replace the file each time:

```python
scheduler = ScheduledScraper(
    topic="latest news",
    output_file="latest.json",
    append_mode=False  # Replaces file each run
)
```

### Logging

All runs are logged with timestamps:

```
2024-01-20 10:00:00 - Starting scheduled scrape #1
2024-01-20 10:05:23 - ✓ Added 15 new comments (Total: 15)
2024-01-20 10:30:00 - Starting scheduled scrape #2
2024-01-20 10:35:11 - ✓ Added 8 new comments (Total: 23)
```

---

## System Schedulers

For production use, system schedulers are more reliable.

### Windows Task Scheduler

**1. Create a batch file** (`C:\scrapers\run_commentradar.bat`):
```batch
@echo off
cd C:\Users\nihil\OneDrive\Documents\batavia
python -m commentradar --topic "tech news" --platform blog --limit 50 --output C:\scrapers\comments.json
```

**2. Open Task Scheduler:**
- Press `Win + R`, type `taskschd.msc`
- Create Basic Task
- Name: "CommentRadar Scraper"
- Trigger: Daily, repeat every 30 minutes
- Action: Start a program
- Program: `C:\scrapers\run_commentradar.bat`

**3. Advanced settings:**
- Run whether user is logged on or not
- Run with highest privileges (if needed)
- Repeat task every: 30 minutes
- Duration: Indefinitely

### Linux/Mac Cron

**1. Edit crontab:**
```bash
crontab -e
```

**2. Add cron job (every 30 minutes):**
```cron
*/30 * * * * cd /path/to/batavia && /usr/bin/python3 -m commentradar --topic "tech news" --platform blog --limit 50 --output /path/to/comments.json >> /path/to/scraper.log 2>&1
```

**Cron syntax:**
```
*/30 * * * *  # Every 30 minutes
0 * * * *     # Every hour
0 */2 * * *   # Every 2 hours
0 9-17 * * *  # Every hour from 9 AM to 5 PM
```

**3. Verify cron job:**
```bash
crontab -l
```

**4. View logs:**
```bash
tail -f /path/to/scraper.log
```

### Systemd Service (Linux)

**1. Create service file** (`/etc/systemd/system/commentradar.service`):
```ini
[Unit]
Description=CommentRadar Scheduled Scraper
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/batavia
ExecStart=/usr/bin/python3 -m commentradar.scheduler --topic "tech news" --interval 30
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

**2. Enable and start:**
```bash
sudo systemctl enable commentradar
sudo systemctl start commentradar
sudo systemctl status commentradar
```

**3. View logs:**
```bash
journalctl -u commentradar -f
```

---

## Cloud Deployment

### AWS Lambda (Serverless)

**1. Package your code:**
```bash
pip install -t package/ -r requirements.txt
cd package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip commentradar/*
```

**2. Create Lambda function:**
```python
# lambda_handler.py
import json
from commentradar.scraper_manager import ScraperManager

def lambda_handler(event, context):
    manager = ScraperManager(
        topic=event.get('topic', 'tech news'),
        platforms=['blog'],
        limit=50
    )
    
    collection = manager.scrape_all()
    
    # Save to S3 or return
    return {
        'statusCode': 200,
        'body': json.dumps({
            'comments_found': len(collection),
            'data': collection.to_dict()
        })
    }
```

**3. Set up EventBridge trigger:**
- Rate: `rate(30 minutes)`
- Target: Your Lambda function

### Google Cloud Functions

**Deploy:**
```bash
gcloud functions deploy commentradar_scraper \
    --runtime python39 \
    --trigger-topic scrape-schedule \
    --entry-point scrape_comments
```

**Schedule with Cloud Scheduler:**
```bash
gcloud scheduler jobs create pubsub scrape-job \
    --schedule="*/30 * * * *" \
    --topic=scrape-schedule \
    --message-body='{"topic":"tech news"}'
```

### Heroku

**1. Create Procfile:**
```
worker: python -m commentradar.scheduler --topic "$TOPIC" --interval 30
```

**2. Deploy:**
```bash
git push heroku main
heroku ps:scale worker=1
```

---

## Docker Setup

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install schedule

# Copy application
COPY commentradar/ ./commentradar/
COPY setup.py .

# Install application
RUN pip install -e .

# Run scheduler
CMD ["python", "-m", "commentradar.scheduler", \
     "--topic", "${SCRAPE_TOPIC}", \
     "--interval", "30", \
     "--limit", "50", \
     "--analyze-sentiment"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  commentradar:
    build: .
    environment:
      - SCRAPE_TOPIC=tech news
      - OUTPUT_FILE=/data/comments.json
    volumes:
      - ./data:/data
    restart: unless-stopped
```

**Run:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f commentradar
```

---

## Advanced Patterns

### Multiple Topics

Scrape different topics on different schedules:

```python
import schedule
from commentradar.scraper_manager import ScraperManager

def scrape_tech():
    manager = ScraperManager(topic="tech news", platforms=["blog"], limit=30)
    manager.scrape_all()
    manager.save_results("tech_comments.json")

def scrape_health():
    manager = ScraperManager(topic="health tips", platforms=["blog"], limit=30)
    manager.scrape_all()
    manager.save_results("health_comments.json")

# Different schedules
schedule.every(30).minutes.do(scrape_tech)
schedule.every(60).minutes.do(scrape_health)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Database Integration

Store in database instead of JSON:

```python
import sqlite3
from commentradar.scheduler import ScheduledScraper

class DatabaseScraper(ScheduledScraper):
    def __init__(self, *args, db_path="comments.db", **kwargs):
        super().__init__(*args, **kwargs)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                source_url TEXT,
                platform TEXT,
                commenter_name TEXT,
                comment_text TEXT,
                date_posted TEXT,
                sentiment TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def scrape_job(self):
        # ... scrape comments ...
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        for comment in collection:
            conn.execute('''
                INSERT INTO comments (source_url, platform, commenter_name, comment_text, date_posted, sentiment)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (comment.source_url, comment.platform, comment.commenter_name, 
                  comment.comment_text, comment.date_posted, comment.sentiment))
        conn.commit()
        conn.close()
```

### Monitoring & Alerts

Send notifications when scraping is done:

```python
import smtplib
from email.mime.text import MIMEText

class MonitoredScraper(ScheduledScraper):
    def scrape_job(self):
        try:
            super().scrape_job()
            self.send_notification("✓ Scraping completed successfully")
        except Exception as e:
            self.send_notification(f"✗ Scraping failed: {e}")
            raise
    
    def send_notification(self, message):
        # Send email, Slack message, etc.
        pass
```

---

## Troubleshooting

### Issue: Process stops after a while

**Solution:** Use system scheduler or Docker with restart policy

### Issue: Rate limiting / getting blocked

**Solution:** Increase interval, add random jitter:
```python
import random
interval = 30 + random.randint(0, 10)  # 30-40 minutes
```

### Issue: Memory usage grows over time

**Solution:** Use overwrite mode or database instead of append mode

### Issue: Logs getting too large

**Solution:** Implement log rotation:
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'scraper.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

---

## Best Practices

1. **Start with longer intervals** (60+ minutes) and adjust down
2. **Monitor for duplicates** - use append mode with deduplication
3. **Log everything** - helps debug issues
4. **Set resource limits** - limit memory/CPU in production
5. **Handle errors gracefully** - don't let one failure stop the scheduler
6. **Test locally first** - run for a few cycles before deploying
7. **Respect robots.txt** - already built-in to CommentRadar
8. **Use environment variables** for sensitive config

---

## Quick Reference

| Method | Best For | Setup Difficulty |
|--------|----------|------------------|
| Built-in Scheduler | Development, testing | ⭐ Easy |
| Windows Task Scheduler | Windows production | ⭐⭐ Medium |
| Linux Cron | Linux/Mac production | ⭐⭐ Medium |
| Systemd | Linux servers | ⭐⭐⭐ Advanced |
| Docker | Cross-platform, scalable | ⭐⭐⭐ Advanced |
| Cloud (Lambda/GCF) | Serverless, auto-scale | ⭐⭐⭐⭐ Expert |

---

Need help? Open an issue on GitHub!

