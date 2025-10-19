# Contributing to CommentRadar

Thank you for your interest in contributing to CommentRadar! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/commentradar.git
   cd commentradar
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## 🏗️ Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Write tests for new features

3. **Run tests**
   ```bash
   pytest
   ```

4. **Format code**
   ```bash
   black commentradar/
   ```

5. **Check linting**
   ```bash
   flake8 commentradar/
   ```

6. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🔌 Adding a New Platform Scraper

To add support for a new platform:

1. **Create a new scraper file** in `commentradar/scrapers/`

   ```python
   # commentradar/scrapers/twitter_scraper.py
   from typing import List
   from commentradar.scrapers.base import BaseScraper
   from commentradar.models import Comment
   
   class TwitterScraper(BaseScraper):
       def get_platform_name(self) -> str:
           return "twitter"
       
       def scrape(self) -> List[Comment]:
           # Your implementation
           pass
   ```

2. **Add to `scrapers/__init__.py`**

   ```python
   from commentradar.scrapers.twitter_scraper import TwitterScraper
   
   __all__ = [
       # ... existing scrapers
       'TwitterScraper',
   ]
   ```

3. **Register in `scraper_manager.py`**

   ```python
   PLATFORM_MAP = {
       # ... existing platforms
       'twitter': TwitterScraper,
   }
   ```

4. **Update CLI choices** in `cli.py`

5. **Add tests** in `tests/test_twitter_scraper.py`

6. **Update documentation** in README.md

## 📝 Commit Message Guidelines

We follow the Conventional Commits specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add Twitter scraper
fix: handle empty comment text
docs: update installation instructions
```

## 🧪 Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use pytest fixtures for common setup

## 🎨 Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write clear docstrings (Google style)
- Keep functions focused and small
- Use meaningful variable names

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions/classes
- Include examples for new features
- Update CHANGELOG.md

## 🐛 Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

## ✨ Feature Requests

When suggesting features:

- Describe the use case
- Explain why it's useful
- Provide examples if possible
- Consider implementation complexity

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## ❓ Questions?

Feel free to open an issue for discussion or reach out to the maintainers.

Thank you for contributing to CommentRadar! 🎉

