"""
Scrape ALL of Sweden - complete dataset
"""

from bygglov_scraper import BygglovScraper
from datetime import datetime

scraper = BygglovScraper(rate_limit_seconds=1.0)

print("=" * 60)
print("Scraping ALL of Sweden")
print("=" * 60)

permits = scraper.scrape_sweden(
    window=30,
    types=[0, 1, 2, 3],  # All permit types
    grid_size=2.0,  # 2 degree cells (faster, should still capture all)
    fetch_details=True
)

# Save results
output_file = f"bygglov_sweden_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
scraper.save_to_csv(permits, output_file)

print("\n" + "=" * 60)
print(f"SUCCESS: Scraped {len(permits)} permits from all of Sweden")
print(f"Saved to: {output_file}")
print("=" * 60)
