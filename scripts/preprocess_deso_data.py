"""
Preprocess DeSO Demographic Data
================================
This script cleans and prepares DeSO-level demographic data from SCB for
merging with building permit data.

Input files (from C:/Users/Hampu/housing_study/):
- deso_foreign_born.csv: Population by birth region
- deso_income.csv: Mean wage income
- deso_housing_tenure.csv: Housing tenure distribution

Output:
- data/deso_demographics/deso_cleaned.csv: Ready for merging with permits
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
INPUT_DIR = "data/deso_demographics"
OUTPUT_FILE = "data/deso_demographics/deso_cleaned.csv"

def process_foreign_born_data():
    """
    Process foreign-born population data.

    Calculate:
    - Swedish-born count
    - Total population
    - Foreign-born count = Total - Swedish-born
    - Foreign-born percentage

    Returns:
        DataFrame with DeSO-level population and diversity measures
    """
    print("\n" + "=" * 60)
    print("Processing Foreign-Born Data")
    print("=" * 60)

    df = pd.read_csv(f"{INPUT_DIR}/deso_foreign_born.csv")
    print(f"Loaded {len(df)} rows")

    # Filter to "totalt" (all genders combined)
    df = df[df['kön'] == 'totalt'].copy()
    print(f"After filtering to totalt gender: {len(df)} rows")

    # Reshape: separate rows for Sverige vs totalt
    sweden = df[df['födelseregion'] == 'Sverige'].copy()
    total = df[df['födelseregion'] == 'totalt'].copy()

    # Use most recent year (2023)
    sweden = sweden[['region', 'Antal 2023']].rename(columns={'Antal 2023': 'inrikes_fodda'})
    total = total[['region', 'Antal 2023']].rename(columns={'Antal 2023': 'total_population'})

    # Merge
    result = total.merge(sweden, on='region', how='left')

    # Calculate foreign-born
    result['utrikes_fodda'] = result['total_population'] - result['inrikes_fodda']
    result['foreign_born_pct'] = result['utrikes_fodda'] / result['total_population']

    # Clean up
    result = result[result['total_population'] > 0]  # Remove empty areas

    print(f"\nProcessed {len(result)} DeSO areas")
    print(f"Mean foreign-born %: {result['foreign_born_pct'].mean():.1%}")
    print(f"Range: {result['foreign_born_pct'].min():.1%} to {result['foreign_born_pct'].max():.1%}")

    return result

def process_income_data():
    """
    Process income data.

    Extract mean wage income (löneinkomst) for each DeSO area.

    Returns:
        DataFrame with DeSO-level income
    """
    print("\n" + "=" * 60)
    print("Processing Income Data")
    print("=" * 60)

    df = pd.read_csv(f"{INPUT_DIR}/deso_income.csv")
    print(f"Loaded {len(df)} rows")

    # Filter to wage income ("löneinkomst") and totalt gender
    df = df[(df['inkomstkomponent'] == 'löneinkomst ') & (df['kön'] == 'totalt')].copy()

    # Use most recent year (2023)
    result = df[['region', 'Medelvärde för samtliga, tkr 2023']].copy()
    result = result.rename(columns={'Medelvärde för samtliga, tkr 2023': 'mean_income_tkr'})

    # Convert to SEK (from thousands)
    result['mean_income_sek'] = result['mean_income_tkr'] * 1000

    print(f"\nProcessed {len(result)} DeSO areas")
    print(f"Mean income: {result['mean_income_tkr'].mean():.1f} tkr ({result['mean_income_sek'].mean():.0f} SEK)")

    return result

def process_tenure_data():
    """
    Process housing tenure data.

    Calculate:
    - Total dwellings
    - Rental share (hyresrätt)
    - Cooperative share (bostadsrätt)
    - Ownership share (äganderätt)
    - Owner-occupied share (bostadsrätt + äganderätt)

    Returns:
        DataFrame with DeSO-level tenure composition
    """
    print("\n" + "=" * 60)
    print("Processing Tenure Data")
    print("=" * 60)

    df = pd.read_csv(f"{INPUT_DIR}/deso_housing_tenure.csv", encoding='utf-8-sig')
    print(f"Loaded {len(df)} rows")

    # Use most recent year (2023)
    df = df[['region', 'upplåtelseform', 'Antal 2023']].copy()
    df = df.rename(columns={'Antal 2023': 'dwellings'})

    # Pivot to wide format
    pivot = df.pivot(index='region', columns='upplåtelseform', values='dwellings').reset_index()
    pivot = pivot.fillna(0)

    # Calculate total dwellings
    pivot['total_dwellings'] = pivot.iloc[:, 1:].sum(axis=1)

    # Calculate shares (handle division by zero)
    for col in ['hyresrätt', 'bostadsrätt', 'äganderätt']:
        if col in pivot.columns:
            pivot[f'{col}_share'] = pivot[col] / pivot['total_dwellings']
            pivot[f'{col}_share'] = pivot[f'{col}_share'].fillna(0)

    # Calculate owner-occupied share (bostadsrätt + äganderätt)
    if 'bostadsrätt' in pivot.columns and 'äganderätt' in pivot.columns:
        pivot['owner_share'] = (pivot['bostadsrätt'] + pivot['äganderätt']) / pivot['total_dwellings']
        pivot['owner_share'] = pivot['owner_share'].fillna(0)

    # Rental share
    if 'hyresrätt' in pivot.columns:
        pivot['rental_share'] = pivot['hyresrätt'] / pivot['total_dwellings']
        pivot['rental_share'] = pivot['rental_share'].fillna(0)

    print(f"\nProcessed {len(pivot)} DeSO areas")
    if 'rental_share' in pivot.columns:
        print(f"Mean rental share: {pivot['rental_share'].mean():.1%}")
    if 'owner_share' in pivot.columns:
        print(f"Mean owner share: {pivot['owner_share'].mean():.1%}")

    # Keep only necessary columns
    keep_cols = ['region', 'total_dwellings']
    for col in ['hyresrätt_share', 'bostadsrätt_share', 'äganderätt_share',
                'rental_share', 'owner_share']:
        if col in pivot.columns:
            keep_cols.append(col)

    result = pivot[keep_cols].copy()

    return result

def merge_all_data(population_df, income_df, tenure_df):
    """
    Merge all DeSO-level datasets.

    Args:
        population_df: Population and diversity data
        income_df: Income data
        tenure_df: Tenure data

    Returns:
        DataFrame: Complete DeSO-level dataset
    """
    print("\n" + "=" * 60)
    print("Merging All Data")
    print("=" * 60)

    # Merge population + income
    merged = population_df.merge(income_df, on='region', how='left')
    print(f"After merging population + income: {len(merged)} DeSO areas")

    # Merge + tenure
    merged = merged.merge(tenure_df, on='region', how='left')
    print(f"After merging + tenure: {len(merged)} DeSO areas")

    # Extract DeSO code from region name
    # Format: "Municipality (DeSO Name)" -> we want the municipality + name
    merged['deso_name'] = merged['region']

    # Clean up
    merged = merged.dropna(subset=['total_population', 'foreign_born_pct'])

    print(f"\nFinal dataset: {len(merged)} DeSO areas")
    print("\nColumns:", merged.columns.tolist())

    return merged

def main():
    """
    Main execution: Process and merge all DeSO data.
    """
    print("=" * 60)
    print("DeSO Data Preprocessing")
    print("=" * 60)

    # Process each dataset
    population_df = process_foreign_born_data()
    income_df = process_income_data()
    tenure_df = process_tenure_data()

    # Merge all
    final_df = merge_all_data(population_df, income_df, tenure_df)

    # Save
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "=" * 60)
    print("✓ COMPLETE")
    print("=" * 60)
    print(f"Saved cleaned DeSO data to: {OUTPUT_FILE}")
    print(f"Total DeSO areas: {len(final_df)}")

    # Summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(final_df[['total_population', 'foreign_born_pct', 'mean_income_tkr',
                     'rental_share', 'owner_share']].describe().round(2))

if __name__ == "__main__":
    main()
