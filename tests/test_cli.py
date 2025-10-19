"""
Tests for CLI functionality.
"""

import pytest
from commentradar.cli import create_parser


def test_parser_creation():
    """Test that the parser is created correctly."""
    parser = create_parser()
    assert parser is not None


def test_parser_required_arguments():
    """Test that required arguments are enforced."""
    parser = create_parser()
    
    # Should fail without --topic
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_with_valid_arguments():
    """Test parser with valid arguments."""
    parser = create_parser()
    
    args = parser.parse_args([
        '--topic', 'test topic',
        '--platform', 'blog',
        '--limit', '10',
        '--output', 'test.json'
    ])
    
    assert args.topic == 'test topic'
    assert args.platform == ['blog']
    assert args.limit == 10
    assert args.output == 'test.json'


def test_parser_with_filters():
    """Test parser with filtering options."""
    parser = create_parser()
    
    args = parser.parse_args([
        '--topic', 'test',
        '--filter-date-start', '2024-01-01',
        '--sentiment', 'positive',
        '--min-length', '50'
    ])
    
    assert args.filter_date_start == '2024-01-01'
    assert args.sentiment == 'positive'
    assert args.min_length == 50


def test_parser_multiple_platforms():
    """Test parser with multiple platforms."""
    parser = create_parser()
    
    args = parser.parse_args([
        '--topic', 'test',
        '--platform', 'blog', 'google'
    ])
    
    assert 'blog' in args.platform
    assert 'google' in args.platform

