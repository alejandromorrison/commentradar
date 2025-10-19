"""Quick test: Run every 2 minutes to see it work fast."""
from scheduled_nutrition_scraper import NutritionSaaSScheduler

scheduler = NutritionSaaSScheduler(output_file="nutrition_saas_feed_test.json")
scheduler.run(interval_minutes=2)  # Every 2 minutes for testing

