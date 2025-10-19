# Scrape Data Folder

This folder stores all scraped data from CommentRadar.

## 📁 What Gets Saved Here

When you run:
```bash
python quick_scrape.py "your topic"
```

The results are automatically saved to:
```
scrape/your_topic_data.json
```

## 🔒 Privacy Note

**This folder is in `.gitignore`** - your scraped data stays private and won't be committed to Git.

## 📊 Sample Output Format

Scraped data looks like this:

```json
[
  {
    "source_url": "https://reddit.com/r/...",
    "platform": "reddit",
    "commenter_name": "username",
    "comment_text": "Full comment text...",
    "date_posted": "2024-01-01",
    "sentiment": "positive",
    "likes": 42,
    "replies": null
  }
]
```

## 🗑️ Cleaning Up

To delete all scraped data:

**Windows:**
```cmd
del scrape\*.json
```

**Mac/Linux:**
```bash
rm scrape/*.json
```

## 📈 Viewing Your Data

```bash
# List all scraped files
ls scrape/

# View a specific file
cat scrape/your_topic_data.json

# Analyze your data
python analyze_data.py
```

---

Keep scraping! 🚀

