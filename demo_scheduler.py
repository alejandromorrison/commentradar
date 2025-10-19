"""
DEMO: Scheduler with mock data to show how it works.
This generates fake comments so you can see the JSON file grow over time.
"""

import json
import os
import time
import random
from datetime import datetime
import schedule


def generate_mock_comments(topic, count=5):
    """Generate mock comments for demonstration."""
    sample_comments = [
        "Great article about {topic}! Very informative.",
        "I really enjoyed reading this post on {topic}.",
        "Thanks for sharing your insights on {topic}.",
        "This is exactly what I was looking for regarding {topic}.",
        "Excellent explanation of {topic}. Well done!",
        "I have a question about {topic}...",
        "Very helpful information on {topic}.",
        "Interesting perspective on {topic}.",
        "Could you elaborate more on {topic}?",
        "Love this content about {topic}!",
    ]
    
    comments = []
    for i in range(count):
        comment_text = random.choice(sample_comments).format(topic=topic)
        comment = {
            "source_url": f"https://example-blog.com/post-{random.randint(1, 100)}",
            "platform": "blog",
            "commenter_name": f"User{random.randint(1, 1000)}",
            "comment_text": comment_text,
            "date_posted": datetime.now().isoformat(),
            "sentiment": random.choice(["positive", "neutral", "positive"]),
            "likes": random.randint(0, 50),
            "replies": random.randint(0, 10)
        }
        comments.append(comment)
    
    return comments


def scrape_job(topic, output_file, run_count=[0]):
    """Simulated scraping job."""
    run_count[0] += 1
    print(f"\n{'='*60}")
    print(f"🔄 Run #{run_count[0]} at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    
    # Generate mock comments
    new_comments = generate_mock_comments(topic, count=random.randint(3, 8))
    
    # Load existing data if file exists
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    # Remove duplicates (in real scraper this checks URL + text)
    existing_texts = {c['comment_text'] for c in existing_data}
    unique_new = [c for c in new_comments if c['comment_text'] not in existing_texts]
    
    # Merge
    merged_data = existing_data + unique_new
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added {len(unique_new)} new comments")
    print(f"📊 Total comments in file: {len(merged_data)}")
    print(f"💾 Saved to: {output_file}")
    
    # Show a sample
    if unique_new:
        print(f"\n📝 Sample new comment:")
        sample = unique_new[0]
        print(f"   {sample['commenter_name']}: {sample['comment_text'][:60]}...")


def run_demo_scheduler(topic, interval_minutes, output_file):
    """Run the demo scheduler."""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           CommentRadar - DEMO SCHEDULER                  ║
╚═══════════════════════════════════════════════════════════╝

📌 Topic: {topic}
⏱️  Interval: Every {interval_minutes} minute(s)
💾 Output: {output_file}
🔄 Mode: Append (grows over time)

This is a DEMO using mock data to show how the scheduler works.
Watch the JSON file grow as new comments are added!

Press Ctrl+C to stop.
""")
    
    # Schedule the job
    schedule.every(interval_minutes).minutes.do(
        lambda: scrape_job(topic, output_file)
    )
    
    # Run immediately
    print("Running initial scrape...")
    scrape_job(topic, output_file)
    
    print(f"\n⏰ Next run in {interval_minutes} minute(s)...")
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✋ Scheduler stopped by user")
        print(f"📊 Final total: {len(json.load(open(output_file)))} comments")


if __name__ == '__main__':
    import os
    os.makedirs('scrape', exist_ok=True)
    
    # Run demo with 1-minute intervals for fast demonstration
    run_demo_scheduler(
        topic="dental clinics in Santo Domingo",
        interval_minutes=1,  # Change to 30 for real use
        output_file=os.path.join('scrape', "demo_comments.json")
    )

