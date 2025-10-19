# CommentRadar - Quick Usage Guide

## 🚀 Easiest Way to Use

### Windows Users:

**Option 1: Double-click the batch file**
```
1. Double-click scrape.bat
2. Type your topic when prompted
3. Press Enter
4. Results saved automatically!
```

**Option 2: Command line with topic**
```cmd
scrape.bat "AI writing tools"
scrape.bat "fitness tracking apps"
scrape.bat "meal planning SaaS"
```

### All Platforms:

**Simple command:**
```bash
python quick_scrape.py "your topic here"
```

**Examples:**
```bash
python quick_scrape.py "dental clinic reviews"
python quick_scrape.py "nutrition SaaS platforms"
python quick_scrape.py "AI productivity tools"
python quick_scrape.py "project management software"
```

**With options:**
```bash
# Get more results (20 per source instead of 15)
python quick_scrape.py "AI tools" --limit 20

# Skip sentiment analysis (faster)
python quick_scrape.py "fitness apps" --no-sentiment

# Custom output filename
python quick_scrape.py "meal planning" --output my_data.json

# All options together
python quick_scrape.py "SaaS tools" --limit 25 --output saas.json
```

---

## 📊 What You Get

After scraping, you'll get a JSON file with:

```json
[
  {
    "source_url": "https://reddit.com/...",
    "platform": "reddit",
    "commenter_name": "username",
    "comment_text": "Full comment text...",
    "date_posted": "2024-01-01",
    "sentiment": "positive",
    "likes": 42
  }
]
```

---

## 🔄 Scheduled Scraping (Auto-Update Every 30 Minutes)

**Setup once:**
```bash
python scheduled_all_sources.py
```

This will:
- Scrape every 30 minutes
- Add new posts to the JSON file
- Remove duplicates automatically
- Run until you stop it (Ctrl+C)

**Custom interval:**
```bash
# Every 10 minutes
python scheduled_all_sources.py 10

# Every hour
python scheduled_all_sources.py 60
```

---

## 📁 Where is My Data?

Look for files named:
- `[your_topic]_data.json` - From quick scraper
- `nutrition_saas_complete_feed.json` - From scheduled scraper
- `nutrition_saas_all_sources.json` - From multi-source scraper

---

## 🌐 Data Sources

Your scraper collects from:
- ✅ **Reddit** - Posts and discussions
- ✅ **Hacker News** - Tech discussions
- ✅ **GitHub** - Issues and discussions
- ⏳ **Twitter/X** - Tweets (when available)
- ⏳ **Quora** - Questions (when accessible)
- ⏳ **Medium** - Articles (when accessible)

---

## 💡 Pro Tips

1. **Be specific with topics:**
   - Good: "AI writing tools for marketing"
   - Better: "GPT-3 content generation SaaS"

2. **Use quotes for multi-word topics:**
   ```bash
   python quick_scrape.py "machine learning platforms"
   ```

3. **Check the file size:**
   - Typical: 10-50 KB
   - Large: 100+ KB (lots of data!)

4. **View your data:**
   ```bash
   # Windows
   type your_topic_data.json
   
   # Mac/Linux
   cat your_topic_data.json
   
   # Pretty print
   python -m json.tool your_topic_data.json
   ```

5. **Analyze your data:**
   ```bash
   python analyze_data.py
   ```

---

## 🆘 Troubleshooting

**"No data found"**
- Topic might be too specific
- Try broader terms
- Check internet connection

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Want more results?**
```bash
python quick_scrape.py "your topic" --limit 30
```

**Script running too long?**
- Normal: 30-60 seconds
- Some sources timeout
- Results saved regardless

---

## 🎯 Real-World Examples

### Example 1: Market Research
```bash
python quick_scrape.py "CRM software for small business" --limit 20
# Get customer opinions about CRM tools
```

### Example 2: Competitor Analysis
```bash
python quick_scrape.py "Mailchimp alternatives" --limit 25 --output competitors.json
# See what people say about alternatives
```

### Example 3: Trend Monitoring
```bash
python scheduled_all_sources.py 30
# Keep collecting data every 30 minutes
# Stop with Ctrl+C when done
```

### Example 4: Product Validation
```bash
python quick_scrape.py "meal prep app reviews" --limit 30
python analyze_data.py
# See sentiment breakdown and top concerns
```

---

## 📞 Need Help?

Check the README.md for full documentation!

