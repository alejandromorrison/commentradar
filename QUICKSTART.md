# CommentRadar Quick Start Guide

Get up and running with CommentRadar in under 5 minutes!

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/commentradar/commentradar.git
cd commentradar

# Install dependencies
pip install -r requirements.txt

# Install CommentRadar
pip install -e .
```

## 🚀 Basic Usage

### 1. Your First Scrape

```bash
commentradar --topic "coffee shops" --platform blog --limit 10 --output coffee.json
```

This will:
- Search for blog posts about "coffee shops"
- Collect up to 10 comments
- Save results to `coffee.json`

### 2. View the Results

```bash
# On Windows
type coffee.json

# On Linux/Mac
cat coffee.json
```

You'll see JSON output like this:

```json
[
  {
    "source_url": "https://example.com/blog/coffee",
    "platform": "blog",
    "commenter_name": "John Doe",
    "comment_text": "Great article about coffee!",
    "date_posted": "2024-01-15",
    "sentiment": null,
    "likes": null,
    "replies": null
  }
]
```

### 3. Add Sentiment Analysis

```bash
commentradar --topic "restaurant reviews" --platform blog --analyze-sentiment --limit 15 --output reviews.json
```

Now each comment will include sentiment:

```json
{
  "sentiment": "positive"
}
```

## 🎯 Common Use Cases

### Business Intelligence

Monitor competitor mentions:

```bash
commentradar --topic "competitor brand name" --platform all --limit 100 --output competitor_mentions.json
```

### Market Research

Gather product feedback:

```bash
commentradar --topic "product reviews fitness trackers" --platform blog google --analyze-sentiment --sentiment positive --output positive_feedback.json
```

### Trend Analysis

Track industry discussions:

```bash
commentradar --topic "artificial intelligence trends" --platform blog --filter-date-start 2024-01-01 --limit 200 --output ai_trends.json
```

## 🔧 Using as a Python Library

```python
from commentradar.scraper_manager import ScraperManager

# Create scraper
manager = ScraperManager(
    topic="nutrition advice",
    platforms=["blog"],
    limit=20
)

# Scrape comments
collection = manager.scrape_all()

# Add sentiment
manager.add_sentiment_analysis()

# Apply filters
manager.apply_filters(sentiment="positive")

# Save results
manager.save_results("nutrition.json")

# Access comments
for comment in collection:
    print(f"{comment.commenter_name}: {comment.comment_text}")
```

## ⚙️ Configuration

### Setting Up API Credentials

For social media platforms, you'll need API credentials:

1. Copy the example config:
   ```bash
   cp config.example.ini config.ini
   ```

2. Edit `config.ini` with your credentials:
   ```ini
   [api]
   facebook_access_token = YOUR_TOKEN
   instagram_access_token = YOUR_TOKEN
   google_api_key = YOUR_API_KEY
   ```

### Getting API Keys

- **Facebook**: [developers.facebook.com](https://developers.facebook.com)
- **Instagram**: Requires Facebook Business account
- **Google Places**: [console.cloud.google.com](https://console.cloud.google.com)

## 📊 Output Formats

### Current: JSON

```json
[
  {
    "source_url": "...",
    "platform": "...",
    "commenter_name": "...",
    "comment_text": "...",
    "date_posted": "...",
    "sentiment": "...",
    "likes": 0,
    "replies": 0
  }
]
```

### Future: CSV, SQL, etc.

Coming in future releases!

## 🐛 Troubleshooting

### Issue: No comments found

**Solution**: 
- Check your topic is specific enough
- Try different platforms
- Remove limits to see if any results exist

### Issue: API errors

**Solution**:
- Verify API credentials in `config.ini`
- Check API quotas and rate limits
- Ensure API keys have correct permissions

### Issue: robots.txt blocking

**Solution**:
- This is expected behavior (respecting website rules)
- Try different URLs or platforms
- Use official APIs when available

## 📚 Next Steps

- Read the [full README](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to add new features
- See [examples/](examples/) for more code samples
- Visit [documentation](https://commentradar.dev/docs) for guides

## 💡 Pro Tips

1. **Start small**: Use `--limit 10` while testing
2. **Be specific**: More specific topics yield better results
3. **Use sentiment**: `--analyze-sentiment` adds valuable insights
4. **Respect limits**: Don't overwhelm servers with large scrapes
5. **Check robots.txt**: Some sites may block scraping

## ❓ Getting Help

- **Issues**: [GitHub Issues](https://github.com/commentradar/commentradar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/commentradar/commentradar/discussions)
- **Email**: support@commentradar.dev

Happy scraping! 🎉

