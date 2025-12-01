"""
Quick count of ALL permits in Sweden
"""

from bygglov_scraper import BygglovScraper

scraper = BygglovScraper()

print("Querying all of Sweden...")
locations = scraper.get_locations(
    lat_min=55.0,
    lat_max=69.0,
    lon_min=10.5,
    lon_max=24.5,
    window=30,
    types=[0, 1, 2, 3]
)

print(f"\nFound {len(locations)} location markers in Sweden")
print("(Note: This is clustered - actual count is higher)")
