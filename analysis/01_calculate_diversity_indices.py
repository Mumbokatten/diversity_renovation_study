"""
Calculate Diversity Indices for DeSO Areas
===========================================
This script calculates multiple diversity indices commonly used in social science research.

Methods used:
- Simpson Diversity Index (Simpson, 1949)
- Shannon Entropy Index (Shannon, 1948)
- Fractionalization Index (Alesina et al., 2003)
- Herfindahl-Hirschman Index (HHI)

References:
-----------
Simpson, E. H. (1949). Measurement of diversity. Nature, 163(4148), 688.
    https://doi.org/10.1038/163688a0

Shannon, C. E. (1948). A mathematical theory of communication. The Bell System
    Technical Journal, 27(3), 379-423. https://doi.org/10.1002/j.1538-7305.1948.tb01338.x

Alesina, A., Devleeschauwer, A., Easterly, W., Kurlat, S., & Wacziarg, R. (2003).
    Fractionalization. Journal of Economic Growth, 8(2), 155-194.
    https://doi.org/10.1023/A:1024471506938
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
INPUT_FILE = "permits_with_demographics.csv"
OUTPUT_FILE = "analysis/diversity_indices.csv"

def calculate_simpson_index(populations):
    """
    Calculate Simpson Diversity Index.

    Formula: D = 1 - Σ(p_i²)
    where p_i is the proportion of group i

    Higher values indicate more diversity (range 0-1)

    Args:
        populations: Dict or Series with population counts by group

    Returns:
        float: Simpson diversity index

    Reference:
        Simpson (1949). "Measurement of diversity"
    """
    total = sum(populations.values())
    if total == 0:
        return np.nan

    proportions = {k: v/total for k, v in populations.items()}
    simpson = 1 - sum(p**2 for p in proportions.values())

    return simpson

def calculate_shannon_index(populations):
    """
    Calculate Shannon Entropy Index (also called Shannon-Wiener index).

    Formula: H = -Σ(p_i × ln(p_i))
    where p_i is the proportion of group i

    Higher values indicate more diversity

    Args:
        populations: Dict or Series with population counts by group

    Returns:
        float: Shannon entropy index

    Reference:
        Shannon (1948). "A mathematical theory of communication"
    """
    total = sum(populations.values())
    if total == 0:
        return np.nan

    proportions = {k: v/total for k, v in populations.items() if v > 0}
    shannon = -sum(p * np.log(p) for p in proportions.values())

    return shannon

def calculate_fractionalization(populations):
    """
    Calculate Ethnic Fractionalization Index (Alesina et al., 2003).

    Formula: FRAC = 1 - Σ(p_i²)
    (Note: Same formula as Simpson, but interpretation focuses on
     probability that two randomly selected individuals are from different groups)

    Args:
        populations: Dict or Series with population counts by group

    Returns:
        float: Fractionalization index

    Reference:
        Alesina et al. (2003). "Fractionalization"
    """
    return calculate_simpson_index(populations)

def calculate_herfindahl_index(populations):
    """
    Calculate Herfindahl-Hirschman Index (HHI).

    Formula: HHI = Σ(p_i²)
    where p_i is the proportion of group i

    Higher values indicate LESS diversity (more concentration)
    Often used in economics for market concentration

    Args:
        populations: Dict or Series with population counts by group

    Returns:
        float: HHI (range 0-1, or 0-10000 if multiplied by 10000)
    """
    total = sum(populations.values())
    if total == 0:
        return np.nan

    proportions = {k: v/total for k, v in populations.items()}
    hhi = sum(p**2 for p in proportions.values())

    return hhi

def calculate_all_indices(row, swedish_col='inrikes_fodda', foreign_col='utrikes_fodda'):
    """
    Calculate all diversity indices for a DeSO area.

    Assumes data has Swedish-born and foreign-born populations.
    For more detailed analysis, would need breakdown by specific countries.

    Args:
        row: DataFrame row with population columns
        swedish_col: Column name for Swedish-born population
        foreign_col: Column name for foreign-born population

    Returns:
        dict: All calculated indices
    """
    populations = {
        'swedish_born': row[swedish_col],
        'foreign_born': row[foreign_col]
    }

    # Calculate indices
    indices = {
        'simpson_index': calculate_simpson_index(populations),
        'shannon_index': calculate_shannon_index(populations),
        'fractionalization': calculate_fractionalization(populations),
        'hhi': calculate_herfindahl_index(populations),
        # Also calculate simple proportion
        'foreign_born_pct': populations['foreign_born'] / (populations['swedish_born'] + populations['foreign_born'])
                            if (populations['swedish_born'] + populations['foreign_born']) > 0 else np.nan
    }

    return indices

def main():
    """
    Main execution: Calculate diversity indices for all DeSO areas.
    """
    print("=" * 60)
    print("Calculating Diversity Indices")
    print("=" * 60)

    # Load data
    print(f"\nLoading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    # Check required columns exist
    # ADJUST THESE based on your actual column names from SCB data
    swedish_col = 'inrikes_fodda'  # CHANGE IF NEEDED
    foreign_col = 'utrikes_fodda'  # CHANGE IF NEEDED

    if swedish_col not in df.columns or foreign_col not in df.columns:
        print(f"\nWARNING: Expected columns '{swedish_col}' and '{foreign_col}' not found!")
        print(f"Available columns: {list(df.columns)}")
        print("\nPlease edit this script and update column names.")
        return

    print(f"Data loaded: {len(df)} permits")

    # Calculate indices for each DeSO area
    print("\nCalculating diversity indices...")

    # Group by DeSO to get unique areas
    deso_stats = df.groupby('deso').agg({
        swedish_col: 'first',  # Take first value (should be same for all permits in DeSO)
        foreign_col: 'first'
    }).reset_index()

    # Calculate indices
    indices_list = []
    for idx, row in deso_stats.iterrows():
        indices = calculate_all_indices(row, swedish_col, foreign_col)
        indices['deso'] = row['deso']
        indices_list.append(indices)

    indices_df = pd.DataFrame(indices_list)

    # Merge back to original data
    df_with_indices = df.merge(indices_df, on='deso', how='left')

    # Save result
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    df_with_indices.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✓ Saved data with diversity indices to: {OUTPUT_FILE}")

    # Print summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics - Diversity Indices")
    print("=" * 60)
    print(indices_df[['simpson_index', 'shannon_index', 'foreign_born_pct']].describe())

    print("\n" + "=" * 60)
    print("Interpretation Guide")
    print("=" * 60)
    print("Simpson Index (0-1): Higher = more diverse")
    print("  - 0 = completely homogeneous")
    print("  - 0.5 = evenly split between two groups")
    print("  - Values approach 1 as diversity increases")
    print("\nShannon Index (0-ln(n)): Higher = more diverse")
    print("  - 0 = completely homogeneous")
    print("  - ln(2)≈0.69 = evenly split between two groups")
    print("\nForeign-born %: Proportion of foreign-born residents")

if __name__ == "__main__":
    main()
