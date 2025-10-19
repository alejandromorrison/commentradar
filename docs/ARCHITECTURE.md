# CommentRadar Architecture

This document describes the architecture and design decisions of CommentRadar.

## 📐 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Interface                        │
│                        (cli.py)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Scraper Manager                          │
│                  (scraper_manager.py)                       │
│  - Coordinates multiple scrapers                            │
│  - Manages comment collection                               │
│  - Applies filters and sentiment                            │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┬──────────────┐
          │              │               │              │
          ▼              ▼               ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Blog      │ │  Facebook   │ │ Instagram   │ │   Google    │
│  Scraper    │ │   Scraper   │ │  Scraper    │ │  Scraper    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
      │                │               │              │
      └────────────────┴───────────────┴──────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Base Scraper                             │
│                   (scrapers/base.py)                        │
│  - HTTP requests                                            │
│  - robots.txt checking                                      │
│  - Rate limiting                                            │
│  - Error handling                                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Utilities                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   Robots.txt │ │   Filters    │ │  Sentiment   │       │
│  │   Checker    │ │   (Date,     │ │   Analysis   │       │
│  │              │ │   Length)    │ │              │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Models                               │
│                   (models.py)                               │
│  - Comment: Individual comment                              │
│  - CommentCollection: Collection with utilities             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   JSON Output                               │
│              (comments.json)                                │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Component Breakdown

### 1. CLI Interface (`cli.py`)

**Purpose**: Entry point for command-line interaction

**Responsibilities**:
- Parse command-line arguments
- Validate user input
- Configure logging
- Coordinate scraping workflow
- Handle errors and user interruptions

**Design Pattern**: Command pattern

### 2. Scraper Manager (`scraper_manager.py`)

**Purpose**: Orchestrate multiple scrapers and manage results

**Responsibilities**:
- Initialize appropriate scrapers based on user input
- Collect results from all scrapers
- Apply post-processing (sentiment, filters)
- Save results to output file

**Design Pattern**: Facade pattern

### 3. Base Scraper (`scrapers/base.py`)

**Purpose**: Abstract base class for all platform scrapers

**Responsibilities**:
- Common HTTP request functionality
- robots.txt compliance checking
- Rate limiting
- Error handling
- Session management

**Design Pattern**: Template Method pattern

### 4. Platform Scrapers

**Purpose**: Platform-specific scraping logic

**Scrapers**:
- `BlogScraper`: Scrapes blog comments using BeautifulSoup
- `FacebookScraper`: Uses Graph API (placeholder)
- `InstagramScraper`: Uses Graph API (placeholder)
- `GoogleScraper`: Uses Places API (placeholder)

**Design Pattern**: Strategy pattern

### 5. Data Models (`models.py`)

**Purpose**: Structured data representation

**Classes**:
- `Comment`: Single comment with all metadata
- `CommentCollection`: Collection with utility methods

**Design Pattern**: Data Transfer Object (DTO)

### 6. Utilities (`utils/`)

**Purpose**: Reusable helper functions

**Modules**:
- `robots.py`: robots.txt checking
- `filters.py`: Date, sentiment, length filtering
- `sentiment.py`: Basic sentiment analysis

## 🔄 Data Flow

1. **User Input** → CLI parses arguments
2. **Initialization** → ScraperManager creates appropriate scrapers
3. **Scraping** → Each scraper collects comments
4. **Aggregation** → Comments added to CommentCollection
5. **Processing** → Sentiment analysis and filters applied
6. **Output** → Results saved to JSON file

## 🎯 Design Decisions

### Modularity

**Decision**: Separate scraper for each platform

**Rationale**:
- Easy to add new platforms
- Platform-specific logic isolated
- Easy to test independently

### robots.txt Compliance

**Decision**: Check robots.txt before scraping

**Rationale**:
- Ethical scraping
- Legal compliance
- Respect website owners

### Rate Limiting

**Decision**: Built-in delays between requests

**Rationale**:
- Prevent server overload
- Avoid being blocked
- Respectful scraping

### JSON Output

**Decision**: Use JSON as default output format

**Rationale**:
- Universal format
- Easy to parse
- Human-readable
- Structured data

### API-First for Social Media

**Decision**: Use official APIs for Facebook/Instagram/Google

**Rationale**:
- Legal compliance
- Reliable access
- Respect Terms of Service
- Better data quality

## 🔐 Security Considerations

### API Credentials

- Stored in separate config file (not in code)
- Config file in `.gitignore`
- Environment variables supported

### Rate Limiting

- Prevents DoS-like behavior
- Respects server resources
- Configurable delays

### Error Handling

- Graceful degradation
- No sensitive data in logs
- User-friendly error messages

## 🚀 Performance

### Current

- Synchronous scraping (one at a time)
- HTTP session reuse
- Conservative rate limits

### Future Optimizations

- Async/await for parallel scraping
- Connection pooling
- Caching mechanisms
- Background processing

## 🧪 Testing Strategy

### Unit Tests

- Test individual components in isolation
- Mock external dependencies
- High code coverage

### Integration Tests

- Test scraper workflows
- Test CLI commands
- Test data flow

### Manual Testing

- Test with real websites
- Verify robots.txt compliance
- Check output quality

## 📈 Scalability

### Current Limitations

- Single-threaded execution
- Memory-based collection (no streaming)
- Limited to CLI output

### Scaling Strategies

1. **Parallel Processing**: Use asyncio for concurrent scraping
2. **Streaming**: Process comments as they arrive
3. **Database**: Store results in database for large datasets
4. **Distributed**: Multiple scrapers across machines
5. **Queue System**: Use message queue for job distribution

## 🔄 Extension Points

### Adding New Platforms

1. Create new scraper class
2. Inherit from `BaseScraper`
3. Implement required methods
4. Register in `PLATFORM_MAP`

### Adding New Output Formats

1. Create formatter class
2. Implement conversion method
3. Add CLI option
4. Update documentation

### Adding New Filters

1. Add filter function to `utils/filters.py`
2. Add CLI argument
3. Integrate in `scraper_manager.py`

## 🎨 Code Style

- **PEP 8**: Python style guide
- **Type Hints**: For better IDE support
- **Docstrings**: Google style documentation
- **Logging**: Structured logging throughout

## 📚 Dependencies

### Core

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `lxml`: Fast XML/HTML parser

### Optional

- `textblob`: Sentiment analysis
- `vaderSentiment`: Social media sentiment
- API SDKs for social platforms

## 🔮 Future Architecture

### Planned Improvements

1. **Plugin System**: Dynamic scraper loading
2. **Web API**: RESTful API for remote scraping
3. **Web Dashboard**: Visualization and monitoring
4. **Database Support**: SQLite, PostgreSQL, MongoDB
5. **Cloud Integration**: AWS, GCP, Azure support
6. **Containerization**: Docker images
7. **Orchestration**: Kubernetes deployment

---

For implementation details, see the code documentation and inline comments.

