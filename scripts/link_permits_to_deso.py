"""
Link Building Permits to DeSO Areas and Merge with Demographics
================================================================
This script:
1. Loads building permit data (with coordinates)
2. Loads DeSO boundary polygons
3. Spatially joins permits to DeSO areas
4. Merges with DeSO demographic statistics
5. Calculates diversity indices
6. Exports final analysis dataset
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
import numpy as np

# Configuration
DATA_DIR = Path("data")
PERMITS_FILE = "bygglov_sweden_complete_20251201_194602.csv"
DESO_BOUNDARIES = DATA_DIR / "deso_boundaries" / "deso_2025.gpkg"  # Or .shp
DESO_DEMOGRAPHICS = DATA_DIR / "deso_demographics" / "deso_country_of_birth_2024.csv"
OUTPUT_FILE = "permits_with_demographics.csv"

def load_permits(filepath):
    """Load building permit data and convert to GeoDataFrame."""
    print(f"Loading permits from {filepath}...")
    df = pd.read_csv(filepath)

    # Remove rows with missing coordinates
    df = df.dropna(subset=['longitude', 'latitude'])

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"  # WGS84 (standard lat/lon)
    )

    # Convert to Swedish coordinate system (SWEREF99 TM)
    gdf = gdf.to_crs("EPSG:3006")

    print(f"Loaded {len(gdf)} permits with valid coordinates")
    return gdf

def load_deso_boundaries(filepath):
    """Load DeSO boundary polygons."""
    print(f"Loading DeSO boundaries from {filepath}...")

    # Try different formats
    if filepath.suffix == '.gpkg':
        gdf = gpd.read_file(filepath)
    elif filepath.suffix == '.shp':
        gdf = gpd.read_file(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    # Ensure correct CRS
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:3006")
    elif gdf.crs != "EPSG:3006":
        gdf = gdf.to_crs("EPSG:3006")

    print(f"Loaded {len(gdf)} DeSO areas")

    # Print column names to help user identify DeSO code column
    print(f"DeSO boundary columns: {list(gdf.columns)}")

    return gdf

def spatial_join_permits_to_deso(permits_gdf, deso_gdf, deso_code_col='deso'):
    """Spatially join permits to DeSO areas."""
    print("Performing spatial join (this may take a minute)...")

    # Spatial join: find which DeSO polygon each permit falls into
    joined = gpd.sjoin(
        permits_gdf,
        deso_gdf[[deso_code_col, 'geometry']],
        how='left',
        predicate='within'
    )

    # Count how many permits didn't match a DeSO area
    unmatched = joined[deso_code_col].isna().sum()
    if unmatched > 0:
        print(f"WARNING: {unmatched} permits could not be matched to a DeSO area")
        print("(They might be outside DeSO boundaries or have coordinate errors)")

    print(f"Successfully matched {len(joined) - unmatched} permits to DeSO areas")

    # Drop the geometry column for easier manipulation
    result = pd.DataFrame(joined.drop(columns='geometry'))

    return result

def load_demographics(filepath):
    """Load DeSO demographic statistics."""
    print(f"Loading demographics from {filepath}...")

    df = pd.read_csv(filepath)

    print(f"Loaded demographics for {len(df)} DeSO areas")
    print(f"Demographic columns: {list(df.columns)}")

    return df

def calculate_diversity_index(df, swedish_col, foreign_col):
    """
    Calculate Simpson diversity index.

    Higher values = more diverse
    Formula: 1 - sum(p_i^2) where p_i is proportion of group i
    """
    total = df[swedish_col] + df[foreign_col]

    # Avoid division by zero
    total = total.replace(0, np.nan)

    p_swedish = df[swedish_col] / total
    p_foreign = df[foreign_col] / total

    simpson = 1 - (p_swedish**2 + p_foreign**2)

    return simpson

def merge_and_analyze(permits_df, demographics_df, deso_code_col='deso'):
    """Merge permits with demographics and calculate diversity measures."""
    print("Merging permits with demographics...")

    # Merge on DeSO code
    merged = permits_df.merge(
        demographics_df,
        left_on=deso_code_col,
        right_on=deso_code_col,  # Adjust if demographics has different column name
        how='left'
    )

    # Check for missing demographic data
    missing = merged[demographics_df.columns[1]].isna().sum()  # Check first data column
    if missing > 0:
        print(f"WARNING: {missing} permits have no demographic data")

    # Calculate diversity indices (adjust column names based on your data)
    # Example assuming columns: 'inrikes_fodda' (Swedish-born), 'utrikes_fodda' (foreign-born)
    # ADJUST THESE COLUMN NAMES BASED ON YOUR ACTUAL DATA!

    # Uncomment and adjust when you know the actual column names:
    # merged['diversity_index'] = calculate_diversity_index(
    #     merged,
    #     'inrikes_fodda',  # Swedish-born column name
    #     'utrikes_fodda'   # Foreign-born column name
    # )
    # merged['foreign_born_pct'] = merged['utrikes_fodda'] / (merged['inrikes_fodda'] + merged['utrikes_fodda'])

    print(f"Final dataset: {len(merged)} permits with demographics")

    return merged

def main():
    """Main execution function."""
    print("=" * 60)
    print("Building Permits + DeSO Demographics Linkage")
    print("=" * 60)

    # Check if files exist
    if not Path(PERMITS_FILE).exists():
        print(f"ERROR: Permits file not found: {PERMITS_FILE}")
        return

    if not DESO_BOUNDARIES.exists():
        print(f"ERROR: DeSO boundaries not found: {DESO_BOUNDARIES}")
        print("Please download DeSO boundaries first (see GET_DESO_DATA.md)")
        return

    if not DESO_DEMOGRAPHICS.exists():
        print(f"ERROR: DeSO demographics not found: {DESO_DEMOGRAPHICS}")
        print("Please download DeSO demographics first (see GET_DESO_DATA.md)")
        return

    try:
        # Load data
        permits_gdf = load_permits(PERMITS_FILE)
        deso_gdf = load_deso_boundaries(DESO_BOUNDARIES)

        # IMPORTANT: Check the column name for DeSO code in your boundary file!
        # Common names: 'deso', 'DeSO', 'deso_code', 'DESO_CODE'
        # Adjust this based on what you see in the printed columns above:
        deso_code_column = 'deso'  # CHANGE THIS IF NEEDED

        # Spatial join
        permits_with_deso = spatial_join_permits_to_deso(
            permits_gdf,
            deso_gdf,
            deso_code_col=deso_code_column
        )

        # Load and merge demographics
        demographics_df = load_demographics(DESO_DEMOGRAPHICS)

        final_data = merge_and_analyze(
            permits_with_deso,
            demographics_df,
            deso_code_col=deso_code_column
        )

        # Save result
        final_data.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✓ Success! Saved merged data to: {OUTPUT_FILE}")

        # Print summary statistics
        print("\n" + "=" * 60)
        print("Summary Statistics")
        print("=" * 60)
        print(f"Total permits: {len(final_data)}")
        print(f"Unique DeSO areas: {final_data[deso_code_column].nunique()}")
        print(f"Permits per DeSO (mean): {len(final_data) / final_data[deso_code_column].nunique():.2f}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
