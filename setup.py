"""
Setup script for CommentRadar.
"""

from setuptools import setup, find_packages
import os


# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


setup(
    name='commentradar',
    version='0.1.0',
    author='CommentRadar Team',
    description='CLI tool for scraping public comments from various platforms',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/commentradar/commentradar',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'lxml>=4.9.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'sentiment': [
            'textblob>=0.17.0',
            'vaderSentiment>=3.3.2',
        ],
    },
    entry_points={
        'console_scripts': [
            'commentradar=commentradar.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

