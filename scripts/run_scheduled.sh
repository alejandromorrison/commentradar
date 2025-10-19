#!/bin/bash
# Linux/Mac script to run scheduled scraping
# Usage: ./run_scheduled.sh

echo "Starting CommentRadar Scheduler..."
echo "This will run every 30 minutes."
echo "Press Ctrl+C to stop."
echo ""

cd "$(dirname "$0")/.."
python -m commentradar.scheduler \
    --topic "tech news" \
    --interval 30 \
    --limit 50 \
    --analyze-sentiment

