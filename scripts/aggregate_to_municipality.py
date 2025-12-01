"""
Aggregate DeSO Data to Municipality Level
=========================================
This script aggregates DeSO-level data to municipality level for analysis.

Due to data sparsity (4,242 permits across 3,363 DeSO areas), municipality-level
analysis is more appropriate.

References:
- As recommended in analysis/03_validate_data.py
- Sweden has 290 municipalities vs 3,363 DeSO areas
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
DESO_FILE = "data/deso_demographics/deso_cleaned.csv"
PERMITS_FILE = "bygglov_sweden_complete_20251201_194602.csv"
OUTPUT_DIR = "analysis"
OUTPUT_FILE = f"{OUTPUT_DIR}/permits_with_demographics_municipality.csv"

def extract_municipality(region_name):
    """
    Extract municipality name from DeSO region string.

    Format: "Municipality (DeSO Area Name)"
    Example: "Upplands Väsby (Bollstanäs)" -> "Upplands Väsby"

    Args:
        region_name: Full DeSO region string

    Returns:
        str: Municipality name
    """
    if pd.isna(region_name):
        return None

    # Split on first parenthesis
    parts = region_name.split(' (')
    if len(parts) > 0:
        return parts[0].strip()
    else:
        return region_name.strip()

def aggregate_deso_to_municipality(deso_df):
    """
    Aggregate DeSO-level data to municipality level.

    Aggregation methods:
    - Population: Sum
    - Income: Population-weighted mean
    - Foreign-born %: Recalculate from total foreign-born / total population
    - Tenure shares: Dwelling-weighted mean

    Args:
        deso_df: DeSO-level DataFrame

    Returns:
        DataFrame: Municipality-level aggregated data
    """
    print("\n" + "=" * 60)
    print("Aggregating DeSO to Municipality Level")
    print("=" * 60)

    # Extract municipality name
    deso_df['municipality'] = deso_df['region'].apply(extract_municipality)

    print(f"DeSO areas: {len(deso_df)}")
    print(f"Unique municipalities: {deso_df['municipality'].nunique()}")

    # Aggregate by municipality
    agg_dict = {
        # Population (sum)
        'total_population': 'sum',
        'inrikes_fodda': 'sum',
        'utrikes_fodda': 'sum',

        # Dwellings (sum)
        'total_dwellings': 'sum',

        # For weighted means, we'll calculate manually below
        'mean_income_sek': 'mean',  # Simple mean for now
    }

    muni_df = deso_df.groupby('municipality').agg(agg_dict).reset_index()

    # Recalculate foreign-born percentage
    muni_df['foreign_born_pct'] = muni_df['utrikes_fodda'] / muni_df['total_population']

    # Calculate population-weighted mean income
    # (More accurate than simple mean)
    income_weighted = deso_df.groupby('municipality').apply(
        lambda x: np.average(x['mean_income_sek'], weights=x['total_population'])
    ).reset_index(name='mean_income_sek_weighted')

    muni_df = muni_df.merge(income_weighted, on='municipality', how='left')
    muni_df['mean_income_sek'] = muni_df['mean_income_sek_weighted']
    muni_df = muni_df.drop(columns=['mean_income_sek_weighted'])

    # Calculate tenure shares at municipality level
    # Sum dwellings by tenure type, then calculate shares
    tenure_cols = ['hyresrätt_share', 'bostadsrätt_share', 'äganderätt_share',
                   'rental_share', 'owner_share']

    for col in tenure_cols:
        if col in deso_df.columns:
            # Dwelling-weighted mean
            weighted = deso_df.groupby('municipality').apply(
                lambda x: np.average(x[col], weights=x['total_dwellings']) if x['total_dwellings'].sum() > 0 else 0
            ).reset_index(name=col)
            muni_df = muni_df.merge(weighted, on='municipality', how='left')

    print(f"\nMunicipality-level data: {len(muni_df)} municipalities")
    print(f"Mean foreign-born %: {muni_df['foreign_born_pct'].mean():.1%}")
    print(f"Mean income: {muni_df['mean_income_sek'].mean():.0f} SEK")

    return muni_df

def match_permits_to_municipalities(permits_df, muni_df):
    """
    Match building permits to municipalities.

    Args:
        permits_df: Permit data with municipality column
        muni_df: Municipality-level demographic data

    Returns:
        DataFrame: Permits with demographics
    """
    print("\n" + "=" * 60)
    print("Matching Permits to Municipalities")
    print("=" * 60)

    print(f"Permits: {len(permits_df)}")
    print(f"Municipalities in demographic data: {len(muni_df)}")

    # Clean municipality names in permits
    permits_df['municipality_clean'] = permits_df['municipality'].str.strip()
    muni_df['municipality_clean'] = muni_df['municipality'].str.strip()

    # Merge
    merged = permits_df.merge(muni_df, left_on='municipality_clean',
                               right_on='municipality_clean', how='left',
                               suffixes=('_permit', '_demo'))

    # Check match rate
    matched = merged['foreign_born_pct'].notna().sum()
    match_rate = matched / len(merged) * 100

    print(f"\nMatched permits: {matched}/{len(merged)} ({match_rate:.1f}%)")

    if match_rate < 90:
        print("\nWARNING: Low match rate. Checking unmatched municipalities...")
        unmatched = merged[merged['foreign_born_pct'].isna()]['municipality_clean'].value_counts().head(10)
        print("\nTop unmatched municipalities:")
        print(unmatched)

    return merged

def main():
    """
    Main execution: Aggregate DeSO to municipality and merge with permits.
    """
    print("=" * 60)
    print("Municipality-Level Data Aggregation")
    print("=" * 60)

    # Load DeSO data
    print(f"\nLoading DeSO data from {DESO_FILE}...")
    deso_df = pd.read_csv(DESO_FILE)
    print(f"Loaded {len(deso_df)} DeSO areas")

    # Aggregate to municipality
    muni_df = aggregate_deso_to_municipality(deso_df)

    # Load permits
    print(f"\nLoading permits from {PERMITS_FILE}...")
    permits_df = pd.read_csv(PERMITS_FILE)
    print(f"Loaded {len(permits_df)} permits")

    # Match permits to municipalities
    merged_df = match_permits_to_municipalities(permits_df, muni_df)

    # Save
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Saved to: {OUTPUT_FILE}")
    print(f"Total records: {len(merged_df)}")

    # Summary stats
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    if 'foreign_born_pct' in merged_df.columns:
        summary_cols = ['foreign_born_pct', 'mean_income_sek', 'rental_share', 'owner_share']
        existing_cols = [col for col in summary_cols if col in merged_df.columns]
        if existing_cols:
            print(merged_df[existing_cols].describe().round(3))

if __name__ == "__main__":
    main()
