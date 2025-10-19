# 🚀 CommentRadar - START HERE

## Quick Start - Scrape Any Topic in 10 Seconds

### **Simplest Way:**

```bash
python quick_scrape.py "your topic"
```

### **Examples:**

```bash
python quick_scrape.py "AI writing tools"
python quick_scrape.py "fitness tracking apps"
python quick_scrape.py "meal planning software"
python quick_scrape.py "dental clinic reviews"
python quick_scrape.py "nutrition SaaS platforms"
```

That's it! Results saved automatically. ✅

---

## 📊 What You Get

Real posts/comments from:
- ✅ Reddit
- ✅ Hacker News  
- ✅ GitHub
- ✅ Twitter (when available)
- ✅ With sentiment analysis
- ✅ No duplicates
- ✅ Saved as JSON

---

## 🎯 Real Example

```bash
python quick_scrape.py "fitness apps"
```

**Result:** `fitness_apps_data.json` with 28 real posts like:

```json
{
  "source_url": "https://reddit.com/r/beginnerfitness/...",
  "platform": "reddit",
  "commenter_name": "Anxious-Parking6312",
  "comment_text": "Are there any fitness apps that total newbies...",
  "sentiment": "positive",
  "likes": 9
}
```

---

## ⚡ Advanced Usage

### Get More Results
```bash
python quick_scrape.py "AI tools" --limit 30
```

### Custom Output File
```bash
python quick_scrape.py "SaaS platforms" --output my_data.json
```

### Skip Sentiment (Faster)
```bash
python quick_scrape.py "apps" --no-sentiment
```

### Auto-Scrape Every 30 Minutes
```bash
python scheduled_all_sources.py
```

---

## 📁 Your Data Files

After running, look for:
- `[topic]_data.json` - Your scraped data
- Open it in any text editor or JSON viewer

**View the data:**
```bash
# Windows
type fitness_apps_data.json

# Mac/Linux  
cat fitness_apps_data.json

# Analyze
python analyze_data.py
```

---

## 🎓 Use Cases

### Market Research
```bash
python quick_scrape.py "CRM software reviews" --limit 25
```

### Competitor Analysis  
```bash
python quick_scrape.py "Mailchimp alternatives"
```

### Product Validation
```bash
python quick_scrape.py "meal prep app problems"
```

### Trend Monitoring
```bash
python scheduled_all_sources.py 30
# Runs every 30 minutes, stops with Ctrl+C
```

---

## 💡 Pro Tips

1. **Use quotes** for multi-word topics
2. **Be specific** - "AI writing tools for marketing" is better than "AI"
3. **Check file size** - 10-50 KB is typical
4. **Run scheduled** for continuous data collection

---

## 🆘 Need Help?

**No data found?**
- Try broader topic
- Check internet connection

**Want more results?**
```bash
python quick_scrape.py "topic" --limit 30
```

**Install issues?**
```bash
pip install -r requirements.txt
```

---

## 📚 More Info

- `USAGE_GUIDE.md` - Detailed usage
- `README.md` - Full documentation
- `SCHEDULING.md` - Automated scraping
- `QUICKSTART.md` - Getting started guide

---

## ✨ You're Ready!

Just run:
```bash
python quick_scrape.py "your topic"
```

That's it! Happy scraping! 🎉

