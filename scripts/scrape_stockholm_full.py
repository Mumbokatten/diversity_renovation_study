"""
Scrape ALL Stockholm permits using a grid approach
"""

from bygglov_scraper import BygglovScraper
from datetime import datetime

def scrape_stockholm_complete():
    """
    Scrape all Stockholm region permits by dividing into a fine grid.
    """
    scraper = BygglovScraper(rate_limit_seconds=1.0)

    # Stockholm region - divided into smaller grid cells
    # Each cell is 0.1 degrees (~10km)
    stockholm_bbox = {
        'lat_min': 59.2,
        'lat_max': 59.5,
        'lon_min': 17.8,
        'lon_max': 18.2
    }

    grid_size = 0.1  # Degrees (smaller = more complete, but more requests)

    print("=" * 60)
    print("Scraping ALL Stockholm permits with fine grid")
    print(f"Grid size: {grid_size}° (~10km cells)")
    print("=" * 60)

    all_permits = []
    grid_count = 0

    lat = stockholm_bbox['lat_min']
    while lat < stockholm_bbox['lat_max']:
        lon = stockholm_bbox['lon_min']

        while lon < stockholm_bbox['lon_max']:
            grid_count += 1
            lat_max = min(lat + grid_size, stockholm_bbox['lat_max'])
            lon_max = min(lon + grid_size, stockholm_bbox['lon_max'])

            print(f"\nGrid cell {grid_count}: lat {lat:.2f}-{lat_max:.2f}, lon {lon:.2f}-{lon_max:.2f}")

            permits = scraper.scrape_bounding_box(
                lat, lat_max, lon, lon_max,
                window=30,
                types=[0, 1, 2, 3],
                fetch_details=True
            )

            all_permits.extend(permits)
            print(f"Total permits collected so far: {len(all_permits)}")

            lon += grid_size

        lat += grid_size

    # Save results
    output_file = f"bygglov_stockholm_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    scraper.save_to_csv(all_permits, output_file)

    print("\n" + "=" * 60)
    print(f"SUCCESS: Scraped {len(all_permits)} permits")
    print(f"Saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    scrape_stockholm_complete()
