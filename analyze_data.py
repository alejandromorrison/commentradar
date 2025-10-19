"""
Analyze the collected nutrition SaaS data.
Shows statistics, sentiment breakdown, top sources, etc.
"""

import json
from collections import Counter
from datetime import datetime


def analyze_file(filename):
    """Analyze a JSON data file."""
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 Analysis: {filename}")
    print(f"{'='*60}\n")
    
    # Basic stats
    print(f"📝 Total Posts: {len(data)}")
    
    # Platform breakdown
    platforms = Counter(item['platform'] for item in data)
    print(f"\n🌐 By Platform:")
    for platform, count in platforms.most_common():
        print(f"   {platform.capitalize():.<20} {count} posts")
    
    # Sentiment breakdown
    sentiments = Counter(item.get('sentiment', 'unknown') for item in data)
    print(f"\n😊 By Sentiment:")
    for sentiment, count in sentiments.most_common():
        print(f"   {sentiment.capitalize():.<20} {count} posts")
    
    # Top contributors
    authors = Counter(item['commenter_name'] for item in data)
    print(f"\n👥 Top Contributors:")
    for author, count in authors.most_common(5):
        print(f"   {author[:30]:.<32} {count} posts")
    
    # Most liked
    with_likes = [item for item in data if item.get('likes')]
    if with_likes:
        top_liked = sorted(with_likes, key=lambda x: x.get('likes', 0), reverse=True)[:3]
        print(f"\n❤️  Most Liked Posts:")
        for i, item in enumerate(top_liked, 1):
            print(f"   {i}. {item['likes']} likes - {item['comment_text'][:50]}...")
    
    # Recent posts
    with_dates = [item for item in data if item.get('date_posted')]
    if with_dates:
        print(f"\n📅 Latest Posts:")
        recent = sorted(with_dates, key=lambda x: x.get('date_posted', ''), reverse=True)[:3]
        for i, item in enumerate(recent, 1):
            print(f"   {i}. [{item['platform'].upper()}] {item['commenter_name']}")
            print(f"      {item['comment_text'][:60]}...")
    
    print()


def main():
    """Analyze all data files."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║           CommentRadar Data Analyzer                     ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    import os
    import glob
    
    # Find all JSON files in scrape folder
    scrape_folder = "scrape"
    if os.path.exists(scrape_folder):
        files = glob.glob(os.path.join(scrape_folder, "*.json"))
        
        if not files:
            print("❌ No JSON files found in scrape/ folder")
            return
        
        print(f"📊 Found {len(files)} data files\n")
        
        for filename in files:
            analyze_file(filename)
    else:
        print("❌ scrape/ folder not found")
        return
    
    print("="*60)
    print("\n✅ Analysis complete!\n")


if __name__ == '__main__':
    main()

