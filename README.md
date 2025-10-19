# CommentRadar – CLI Insight Scraper

**CommentRadar** is a technical CLI tool that scrapes public comments, reviews, and discussions from blogs, Google-linked pages, and social media platforms (e.g., Instagram, Facebook), based on a user-defined topic. It outputs structured JSON containing source URL, platform name, commenter name, comment text, and date posted.

## 🎯 Purpose

Designed for developers, analysts, and business owners who want to monitor public sentiment, competitor feedback, or user discussions around specific industries (e.g., dental clinics, construction firms, travel apps).

## ✨ Features

- **Topic-based scraping** via CLI (`--topic "dental clinics in Santo Domingo"`)
- **Platform targeting** (`--platform blog|facebook|instagram|google`)
- **JSON output** (`--output comments.json`)
- **Optional filters** (`--limit`, `--filter-date`, `--sentiment`)
- **Modular architecture** for adding new scrapers
- **Respects robots.txt** and platform-specific scraping policies

## 🚀 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/commentradar/commentradar.git
cd commentradar

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install commentradar
```

## 📖 Usage

### Basic Usage

```bash
# Scrape blog comments about nutrition
commentradar --topic "nutrition blogs" --platform blog --limit 20 --output nutrition_comments.json

# Scrape from multiple platforms
commentradar --topic "dental clinics in Santo Domingo" --platform blog google --limit 50

# Scrape from all platforms
commentradar --topic "travel apps" --platform all --output travel_comments.json
```

### Advanced Usage

```bash
# With sentiment analysis
commentradar --topic "restaurant reviews" --platform blog --analyze-sentiment --output reviews.json

# With date filtering
commentradar --topic "tech products" --platform all --filter-date-start 2024-01-01 --filter-date-end 2024-12-31

# Filter by sentiment
commentradar --topic "customer service" --platform blog --analyze-sentiment --sentiment positive

# With length filters
commentradar --topic "product feedback" --platform all --min-length 50 --max-length 500

# Verbose mode for debugging
commentradar --topic "market research" --platform blog --verbose
```

### Command-Line Options

```
Required Arguments:
  --topic TOPIC             Topic to search for (e.g., "dental clinics in Santo Domingo")

Optional Arguments:
  --platform {blog,facebook,instagram,google,all}
                            Platform(s) to scrape (default: all)
  --limit LIMIT             Maximum number of comments to collect per platform
  --output OUTPUT           Output JSON file path (default: comments.json)
  --analyze-sentiment       Add sentiment analysis to comments
  --verbose, -v             Enable verbose logging

Filtering Options:
  --filter-date-start DATE  Filter comments after this date (ISO format: YYYY-MM-DD)
  --filter-date-end DATE    Filter comments before this date (ISO format: YYYY-MM-DD)
  --sentiment {positive,negative,neutral}
                            Filter by sentiment
  --min-length LENGTH       Minimum comment text length
  --max-length LENGTH       Maximum comment text length
```

## 📊 Output Format

CommentRadar outputs JSON with the following structure:

```json
[
  {
    "source_url": "https://example.com/blog/post",
    "platform": "blog",
    "commenter_name": "John Doe",
    "comment_text": "Great article! Very informative.",
    "date_posted": "2024-01-15T10:30:00",
    "sentiment": "positive",
    "likes": 5,
    "replies": 2
  },
  {
    "source_url": "https://example.com/another-post",
    "platform": "blog",
    "commenter_name": "Jane Smith",
    "comment_text": "Thanks for sharing this information.",
    "date_posted": "2024-01-16T14:20:00",
    "sentiment": "positive",
    "likes": 3,
    "replies": 0
  }
]
```

## 🏗️ Architecture

```
commentradar/
├── __init__.py           # Package initialization
├── __main__.py           # Entry point for python -m commentradar
├── cli.py                # CLI interface and argument parsing
├── models.py             # Data models (Comment, CommentCollection)
├── scraper_manager.py    # Coordinates multiple scrapers
├── scrapers/             # Platform-specific scrapers
│   ├── __init__.py
│   ├── base.py           # Base scraper class
│   ├── blog_scraper.py   # Blog scraper
│   ├── facebook_scraper.py
│   ├── instagram_scraper.py
│   └── google_scraper.py
└── utils/                # Utility functions
    ├── __init__.py
    ├── robots.py         # robots.txt checker
    ├── filters.py        # Comment filtering
    └── sentiment.py      # Sentiment analysis
```

## 🛠️ Tech Stack

- **Python 3.8+** - Core language
- **Requests** - HTTP requests
- **BeautifulSoup4** - HTML parsing
- **argparse** - CLI interface
- **Optional: TextBlob/VADER** - Sentiment analysis
- **Optional: C++** modules for performance-critical parsing

## 🔒 Legal & Ethical Considerations

**Important**: CommentRadar is designed for educational and research purposes. Please use responsibly:

- ✅ **Respects robots.txt** - Automatically checks and follows robots.txt rules
- ✅ **Public content only** - Does not scrape private or login-protected content
- ✅ **Rate limiting** - Implements delays between requests to avoid overwhelming servers
- ✅ **API-first approach** - For social media, uses public APIs or post URLs when available
- ⚠️ **Terms of Service** - Always review and comply with each platform's Terms of Service
- ⚠️ **Data usage** - Ensure compliance with GDPR, CCPA, and other data protection regulations

### Platform-Specific Notes

- **Blogs**: Uses public RSS feeds and HTML parsing where permitted
- **Facebook**: Requires Graph API access token (public posts only)
- **Instagram**: Requires Graph API access for Business/Creator accounts
- **Google**: Uses Places API for reviews (requires API key)

## 🚧 Current Limitations

- Social media scrapers (Facebook, Instagram) require API credentials
- Sentiment analysis is basic (keyword-based); install TextBlob or VADER for better results
- Blog scraper works best with standard comment formats
- Rate limiting is conservative to respect server resources

## 🔮 Future Enhancements

- [ ] Twitter/X integration
- [ ] Reddit scraper
- [ ] YouTube comments scraper
- [ ] Advanced sentiment analysis with transformers
- [ ] SQLite/PostgreSQL output option
- [ ] Web dashboard for visualization
- [ ] Scheduled scraping with cron support
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 🤝 Contributing

Contributions are welcome! To add a new platform scraper:

1. Create a new file in `commentradar/scrapers/`
2. Inherit from `BaseScraper`
3. Implement `scrape()` and `get_platform_name()` methods
4. Add the scraper to `PLATFORM_MAP` in `scraper_manager.py`
5. Update the CLI `--platform` choices

Example:

```python
from commentradar.scrapers.base import BaseScraper
from commentradar.models import Comment

class RedditScraper(BaseScraper):
    def get_platform_name(self) -> str:
        return "reddit"
    
    def scrape(self) -> List[Comment]:
        # Your scraping logic here
        pass
```

## 📝 Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black commentradar/

# Linting
flake8 commentradar/

# Type checking
mypy commentradar/
```

## 📄 License

This project is **open-source** and licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Open Source Contribution
Feel free to:
- ⭐ Star this repository
- 🍴 Fork and modify
- 🐛 Report issues
- 🚀 Submit pull requests
- 📖 Improve documentation

## 🙏 Acknowledgments

- BeautifulSoup4 for HTML parsing
- Requests library for HTTP functionality
- All contributors and users of CommentRadar

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/commentradar/commentradar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/commentradar/commentradar/discussions)
- **Email**: support@commentradar.dev

---

**Disclaimer**: This tool is for educational and research purposes. Always respect website terms of service, robots.txt files, and applicable laws. The maintainers are not responsible for misuse of this tool.

