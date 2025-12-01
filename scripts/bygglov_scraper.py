"""
Bygglovskartan Scraper for Research
====================================
Purpose: Collect building permit data for academic research on housing and neighborhood effects
Author: Research project on ethnic diversity and housing investment
Date: 2025-12-01

IMPORTANT: This script includes rate limiting (1 request/second) to avoid overloading servers.
For research purposes only - not for commercial use.
"""

import requests
import json
import time
import csv
from datetime import datetime
from typing import List, Dict, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Permit type mapping
PERMIT_TYPES = {
    0: "Bygglov",
    1: "Rivningslov",
    2: "Marklov",
    3: "Förhandsbesked"
}


class BygglovScraper:
    """
    Scraper for Bygglovskartan (geoplan.se) with respectful rate limiting.

    The API works in two steps:
    1. get_locations: Returns permit IDs within a bounding box
    2. get_details/{id}: Returns full details for each permit
    """

    BASE_URL = "https://geoplan.se"

    def __init__(self, rate_limit_seconds: float = 1.0):
        """
        Initialize scraper with rate limiting.

        Args:
            rate_limit_seconds: Seconds to wait between requests (default: 1 second)
        """
        self.rate_limit = rate_limit_seconds
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Academic Research Scraper (Housing Study)',
            'Accept': 'application/json'
        })
        self.last_request_time = 0

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            wait_time = self.rate_limit - elapsed
            time.sleep(wait_time)
        self.last_request_time = time.time()

    def get_locations(self,
                     lat_min: float,
                     lat_max: float,
                     lon_min: float,
                     lon_max: float,
                     window: int = 30,
                     types: List[int] = [0, 1, 2, 3]) -> List[Dict]:
        """
        Get permit locations within a bounding box.

        Args:
            lat_min: Minimum latitude
            lat_max: Maximum latitude
            lon_min: Minimum longitude
            lon_max: Maximum longitude
            window: Time window in months (default: 30)
            types: Permit types to include (0=Bygglov, 1=Rivningslov, 2=Marklov, 3=Förhandsbesked)

        Returns:
            List of location features with permit IDs
        """
        self._rate_limit_wait()

        params = {
            'lat_min': lat_min,
            'lat_max': lat_max,
            'lon_min': lon_min,
            'lon_max': lon_max,
            'window': window,
            'types': ','.join(map(str, types))
        }

        try:
            url = f"{self.BASE_URL}/get_locations"
            logger.info(f"Fetching locations for bbox: ({lon_min:.3f}, {lat_min:.3f}) to ({lon_max:.3f}, {lat_max:.3f})")

            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            count = data.get('count', 0)
            features = data.get('data', {}).get('features', [])

            logger.info(f"Found {count} permits, retrieved {len(features)} location markers")
            return features

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return []

    def get_permit_details(self, permit_id: int) -> Dict:
        """
        Get detailed information for a specific permit.

        Args:
            permit_id: The permit ID

        Returns:
            Permit detail dictionary (GeoJSON Feature)
        """
        self._rate_limit_wait()

        try:
            url = f"{self.BASE_URL}/get_details/{permit_id}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch details for permit {permit_id}: {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for permit {permit_id}: {e}")
            return {}

    def scrape_bounding_box(self,
                           lat_min: float,
                           lat_max: float,
                           lon_min: float,
                           lon_max: float,
                           window: int = 30,
                           types: List[int] = [0, 1, 2, 3],
                           fetch_details: bool = True) -> List[Dict]:
        """
        Scrape all permits within a bounding box.

        Args:
            lat_min: Minimum latitude
            lat_max: Maximum latitude
            lon_min: Minimum longitude
            lon_max: Maximum longitude
            window: Time window in months (default: 30)
            types: Permit types to include
            fetch_details: If True, fetch full details for each permit (slower but more data)

        Returns:
            List of permit dictionaries
        """
        # Step 1: Get all permit locations
        locations = self.get_locations(lat_min, lat_max, lon_min, lon_max, window, types)

        if not locations:
            logger.warning("No locations found in bounding box")
            return []

        if not fetch_details:
            return locations

        # Step 2: Fetch details for each permit
        logger.info(f"Fetching details for {len(locations)} permits...")
        detailed_permits = []

        for i, location in enumerate(locations, 1):
            permit_id = location.get('properties', {}).get('id')
            if not permit_id:
                continue

            if i % 100 == 0:
                logger.info(f"Progress: {i}/{len(locations)} permits fetched")

            details = self.get_permit_details(permit_id)
            if details:
                detailed_permits.append(details)

        logger.info(f"Successfully fetched details for {len(detailed_permits)} permits")
        return detailed_permits

    def scrape_sweden(self,
                     window: int = 30,
                     types: List[int] = [0, 1, 2, 3],
                     grid_size: float = 2.0,
                     fetch_details: bool = True) -> List[Dict]:
        """
        Scrape all of Sweden by dividing it into a grid.

        Args:
            window: Time window in months
            types: Permit types to include
            grid_size: Size of each grid cell in degrees (smaller = more requests but less data per request)
            fetch_details: Whether to fetch full details (recommended)

        Returns:
            List of all permits across Sweden
        """
        # Sweden bounding box (approximate)
        sweden_bbox = {
            'lat_min': 55.0,
            'lat_max': 69.0,
            'lon_min': 10.5,
            'lon_max': 24.5
        }

        logger.info(f"Scraping all of Sweden with grid size {grid_size}°")

        all_permits = []

        # Create grid
        lat = sweden_bbox['lat_min']
        grid_count = 0

        while lat < sweden_bbox['lat_max']:
            lon = sweden_bbox['lon_min']

            while lon < sweden_bbox['lon_max']:
                grid_count += 1
                lat_max = min(lat + grid_size, sweden_bbox['lat_max'])
                lon_max = min(lon + grid_size, sweden_bbox['lon_max'])

                logger.info(f"Grid cell {grid_count}: lat {lat:.2f}-{lat_max:.2f}, lon {lon:.2f}-{lon_max:.2f}")

                permits = self.scrape_bounding_box(
                    lat, lat_max, lon, lon_max,
                    window=window,
                    types=types,
                    fetch_details=fetch_details
                )

                all_permits.extend(permits)
                logger.info(f"Total permits collected so far: {len(all_permits)}")

                lon += grid_size

            lat += grid_size

        logger.info(f"Completed scraping Sweden: {len(all_permits)} total permits")
        return all_permits

    @staticmethod
    def extract_permit_data(permit: Dict) -> Dict:
        """
        Extract relevant fields from permit object.

        Args:
            permit: Raw permit object from get_details API

        Returns:
            Cleaned dictionary with relevant fields
        """
        properties = permit.get('properties', {})
        geometry = permit.get('geometry', {})

        # Get coordinates - handle both Point and Polygon geometries
        coords = geometry.get('coordinates', [])
        if geometry.get('type') == 'Polygon' and coords:
            # For polygon, get centroid (simple average of vertices)
            vertices = coords[0] if coords else []
            if vertices:
                lon = sum(v[0] for v in vertices) / len(vertices)
                lat = sum(v[1] for v in vertices) / len(vertices)
            else:
                lon, lat = None, None
        elif geometry.get('type') == 'Point' and len(coords) >= 2:
            lon, lat = coords[0], coords[1]
        else:
            lon, lat = None, None

        typ_num = properties.get('typ_num', -1)

        return {
            'permit_id': properties.get('id', ''),
            'property_name': properties.get('fastighet', ''),
            'municipal_case_id': properties.get('kun_id', ''),
            'publication_date': properties.get('pubdate', ''),
            'municipality': properties.get('subtext', ''),
            'permit_type_num': typ_num,
            'permit_type': PERMIT_TYPES.get(typ_num, 'Unknown'),
            'longitude': lon,
            'latitude': lat,
        }

    def save_to_csv(self, permits: List[Dict], output_file: str):
        """Save permits to CSV file."""
        if not permits:
            logger.warning("No permits to save")
            return

        cleaned_permits = [self.extract_permit_data(p) for p in permits]

        # Remove duplicates by permit_id
        seen_ids = set()
        unique_permits = []
        for p in cleaned_permits:
            if p['permit_id'] not in seen_ids:
                seen_ids.add(p['permit_id'])
                unique_permits.append(p)

        logger.info(f"Removed {len(cleaned_permits) - len(unique_permits)} duplicate permits")

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=unique_permits[0].keys())
            writer.writeheader()
            writer.writerows(unique_permits)

        logger.info(f"Saved {len(unique_permits)} permits to {output_file}")


def main():
    """
    Example usage - customize as needed.
    """
    # Initialize scraper with 1 second between requests
    scraper = BygglovScraper(rate_limit_seconds=1.0)

    # Example 1: Scrape Stockholm region
    logger.info("=" * 60)
    logger.info("Example: Scraping Stockholm region")
    logger.info("=" * 60)

    permits = scraper.scrape_bounding_box(
        lat_min=59.2,
        lat_max=59.5,
        lon_min=17.8,
        lon_max=18.2,
        window=30,  # Last 30 months
        types=[0, 1, 2, 3],  # All permit types
        fetch_details=True
    )

    # Example 2: Scrape ALL of Sweden (WARNING: This will take HOURS!)
    # Uncomment to use:
    # logger.info("=" * 60)
    # logger.info("Example: Scraping ALL of Sweden")
    # logger.info("=" * 60)
    #
    # permits = scraper.scrape_sweden(
    #     window=30,
    #     types=[0],  # Only building permits to reduce time
    #     grid_size=1.0,  # Smaller grid = more requests but better coverage
    #     fetch_details=True
    # )

    # Save to CSV
    if permits:
        output_file = f"bygglov_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        scraper.save_to_csv(permits, output_file)
        print(f"\n{'='*60}")
        print(f"✓ Successfully scraped {len(permits)} permits")
        print(f"✓ Saved to: {output_file}")
        print(f"{'='*60}\n")
    else:
        print("\n✗ No permits found - check bounding box coordinates")


if __name__ == "__main__":
    main()
