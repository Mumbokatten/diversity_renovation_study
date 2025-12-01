"""
Data Validation and Quality Checks
===================================
This script performs comprehensive data validation and quality checks for the
diversity and renovation study. It also addresses data sparsity issues.

Key Checks:
- Missing data patterns
- Geographic coverage
- Data sparsity analysis (permits per DeSO)
- Outlier detection
- Logical consistency checks

Sparsity Solutions:
- Aggregate DeSO areas to larger units (municipalities, counties)
- Time aggregation (use full 30-month window)
- Binary outcome models (any renovation vs. none)
- Zero-inflated models for count data

References:
-----------
King, G., & Zeng, L. (2001). Logistic regression in rare events data.
    Political Analysis, 9(2), 137-163. https://doi.org/10.1093/oxfordjournals.pan.a004868

Cameron, A. C., & Trivedi, P. K. (2013). Regression analysis of count data
    (2nd ed.). Cambridge University Press.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

# File paths
INPUT_FILE = "analysis/diversity_indices.csv"
OUTPUT_DIR = "analysis/validation"

def check_missing_data(df):
    """
    Analyze missing data patterns.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame: Missing data summary
    """
    print("\n" + "=" * 60)
    print("Missing Data Analysis")
    print("=" * 60)

    missing = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percent': (df.isnull().sum() / len(df) * 100).round(2)
    })

    missing = missing[missing['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

    if len(missing) == 0:
        print("\n✓ No missing data found!")
    else:
        print("\nColumns with missing data:")
        print(missing.to_string(index=False))

    return missing

def analyze_sparsity(df):
    """
    Analyze data sparsity - critical for this study.

    With ~4,200 permits and ~6,160 DeSO areas, most areas will have zero permits.
    This requires special handling in regression analysis.

    Args:
        df: DataFrame with permits and DeSO linkages

    Returns:
        dict: Sparsity statistics and recommendations
    """
    print("\n" + "=" * 60)
    print("Data Sparsity Analysis")
    print("=" * 60)

    results = {}

    # Count permits per DeSO
    if 'deso' in df.columns:
        permits_per_deso = df.groupby('deso').size()
        results['permits_per_deso'] = permits_per_deso

        total_deso = len(permits_per_deso)
        total_permits = len(df)

        print(f"\nTotal DeSO areas with permits: {total_deso:,}")
        print(f"Total permits: {total_permits:,}")
        print(f"Average permits per DeSO: {total_permits/total_deso:.2f}")

        # Distribution of permits
        print("\nPermit distribution:")
        print(f"  Min: {permits_per_deso.min()}")
        print(f"  Median: {permits_per_deso.median():.1f}")
        print(f"  Mean: {permits_per_deso.mean():.2f}")
        print(f"  Max: {permits_per_deso.max()}")
        print(f"  Std Dev: {permits_per_deso.std():.2f}")

        # Concentration analysis
        deso_1_permit = (permits_per_deso == 1).sum()
        deso_2_5_permits = ((permits_per_deso >= 2) & (permits_per_deso <= 5)).sum()
        deso_6plus_permits = (permits_per_deso >= 6).sum()

        print(f"\nConcentration:")
        print(f"  DeSO areas with 1 permit: {deso_1_permit} ({deso_1_permit/total_deso*100:.1f}%)")
        print(f"  DeSO areas with 2-5 permits: {deso_2_5_permits} ({deso_2_5_permits/total_deso*100:.1f}%)")
        print(f"  DeSO areas with 6+ permits: {deso_6plus_permits} ({deso_6plus_permits/total_deso*100:.1f}%)")

        # Estimate total DeSO in Sweden (if we had full dataset)
        print("\n" + "=" * 60)
        print("Sparsity Problem Assessment")
        print("=" * 60)
        print("\nEstimated total DeSO areas in Sweden: ~6,160")
        print(f"DeSO areas with permits in our data: {total_deso}")
        print(f"DeSO areas with NO permits: ~{6160 - total_deso:,} (estimated)")
        coverage_pct = (total_deso / 6160) * 100
        print(f"Coverage: {coverage_pct:.1f}% of all DeSO areas")

        results['sparsity_stats'] = {
            'total_deso_with_permits': total_deso,
            'total_permits': total_permits,
            'avg_permits_per_deso': total_permits/total_deso,
            'estimated_coverage_pct': coverage_pct
        }

    return results

def recommend_aggregation_strategies(sparsity_stats):
    """
    Recommend aggregation strategies to handle sparsity.

    Args:
        sparsity_stats: Dictionary with sparsity statistics

    Returns:
        dict: Recommended strategies
    """
    print("\n" + "=" * 60)
    print("RECOMMENDED STRATEGIES for Data Sparsity")
    print("=" * 60)

    strategies = {}

    # Strategy 1: Municipality aggregation
    print("\n1. AGGREGATE TO MUNICIPALITY LEVEL")
    print("   - Sweden has 290 municipalities vs 6,160 DeSO areas")
    print("   - Each municipality would have ~14 permits on average")
    print("   - Pro: Better statistical power, meaningful administrative unit")
    print("   - Con: Loses fine-grained neighborhood variation")
    print("   - RECOMMENDATION: PRIMARY ANALYSIS")
    strategies['municipality'] = {
        'unit': 'Municipality',
        'n_units': 290,
        'recommendation': 'PRIMARY ANALYSIS',
        'implementation': 'Group DeSO areas by municipality code'
    }

    # Strategy 2: County aggregation
    print("\n2. AGGREGATE TO COUNTY LEVEL (Län)")
    print("   - Sweden has 21 counties")
    print("   - Each county would have ~200 permits on average")
    print("   - Pro: Excellent statistical power")
    print("   - Con: Loses local neighborhood effects (too coarse)")
    print("   - RECOMMENDATION: ROBUSTNESS CHECK")
    strategies['county'] = {
        'unit': 'County (Län)',
        'n_units': 21,
        'recommendation': 'ROBUSTNESS CHECK',
        'implementation': 'Group municipalities by län code'
    }

    # Strategy 3: Binary outcome
    print("\n3. BINARY OUTCOME MODEL")
    print("   - Dependent variable: Any renovation (1) vs. None (0)")
    print("   - Use logistic regression instead of OLS")
    print("   - Pro: Handles zeros naturally, interprets as probability")
    print("   - Con: Loses information about renovation intensity")
    print("   - RECOMMENDATION: ALTERNATIVE SPECIFICATION")
    strategies['binary'] = {
        'model': 'Logistic regression',
        'dependent_var': 'any_renovation (0/1)',
        'recommendation': 'ALTERNATIVE SPECIFICATION',
        'reference': 'King & Zeng (2001) for rare events'
    }

    # Strategy 4: Count models
    print("\n4. COUNT DATA MODELS")
    print("   - Dependent variable: Number of permits (0, 1, 2, ...)")
    print("   - Use Poisson or Negative Binomial regression")
    print("   - Pro: Designed for count data with many zeros")
    print("   - Con: Requires additional assumptions")
    print("   - RECOMMENDATION: ALTERNATIVE SPECIFICATION")
    strategies['count'] = {
        'models': ['Poisson', 'Negative Binomial', 'Zero-Inflated'],
        'dependent_var': 'permit_count',
        'recommendation': 'ALTERNATIVE SPECIFICATION',
        'reference': 'Cameron & Trivedi (2013)'
    }

    # Strategy 5: Focus on urban areas
    print("\n5. SUBSET TO URBAN AREAS")
    print("   - Focus on Stockholm, Gothenburg, Malmö regions")
    print("   - These areas likely have higher permit density")
    print("   - Pro: Better coverage in areas of interest")
    print("   - Con: Generalizability to rural areas unclear")
    print("   - RECOMMENDATION: SENSITIVITY ANALYSIS")
    strategies['urban_subset'] = {
        'areas': ['Stockholm', 'Gothenburg', 'Malmö'],
        'recommendation': 'SENSITIVITY ANALYSIS',
        'note': 'Compare results: urban vs. all Sweden'
    }

    return strategies

def check_geographic_coverage(df):
    """
    Analyze geographic coverage across Sweden.

    Args:
        df: DataFrame with municipality information

    Returns:
        DataFrame: Summary by municipality
    """
    print("\n" + "=" * 60)
    print("Geographic Coverage Analysis")
    print("=" * 60)

    if 'municipality' not in df.columns:
        print("\nWARNING: 'municipality' column not found")
        print("Cannot perform geographic coverage analysis")
        return None

    # Permits by municipality
    muni_summary = df.groupby('municipality').agg({
        'permit_id': 'count',
        'deso': 'nunique'
    }).rename(columns={
        'permit_id': 'n_permits',
        'deso': 'n_deso_areas'
    })

    muni_summary = muni_summary.sort_values('n_permits', ascending=False)

    print(f"\nTotal municipalities represented: {len(muni_summary)}")
    print(f"\nTop 10 municipalities by permit count:")
    print(muni_summary.head(10))

    print(f"\nBottom 10 municipalities by permit count:")
    print(muni_summary.tail(10))

    return muni_summary

def check_diversity_indices(df):
    """
    Validate diversity index calculations.

    Args:
        df: DataFrame with diversity indices

    Returns:
        dict: Validation results
    """
    print("\n" + "=" * 60)
    print("Diversity Index Validation")
    print("=" * 60)

    results = {}

    # Check Simpson index range (should be 0-1)
    if 'simpson_index' in df.columns:
        simpson_min = df['simpson_index'].min()
        simpson_max = df['simpson_index'].max()
        print(f"\nSimpson Index range: [{simpson_min:.4f}, {simpson_max:.4f}]")

        if simpson_min < 0 or simpson_max > 1:
            print("  ⚠ WARNING: Simpson index outside valid range [0,1]")
            results['simpson_valid'] = False
        else:
            print("  ✓ Simpson index in valid range [0,1]")
            results['simpson_valid'] = True

    # Check Shannon index (should be >= 0)
    if 'shannon_index' in df.columns:
        shannon_min = df['shannon_index'].min()
        shannon_max = df['shannon_index'].max()
        print(f"\nShannon Index range: [{shannon_min:.4f}, {shannon_max:.4f}]")

        if shannon_min < 0:
            print("  ⚠ WARNING: Shannon index has negative values")
            results['shannon_valid'] = False
        else:
            print("  ✓ Shannon index in valid range")
            results['shannon_valid'] = True

        # For 2 groups, max Shannon is ln(2) ≈ 0.693
        print(f"  Expected max for 2 groups: {np.log(2):.4f}")
        if shannon_max > np.log(2) + 0.01:  # Small tolerance
            print(f"  ⚠ WARNING: Shannon index exceeds theoretical max for 2 groups")

    # Check foreign-born percentage
    if 'foreign_born_pct' in df.columns:
        fb_min = df['foreign_born_pct'].min()
        fb_max = df['foreign_born_pct'].max()
        print(f"\nForeign-born percentage range: [{fb_min:.1%}, {fb_max:.1%}]")

        if fb_min < 0 or fb_max > 1:
            print("  ⚠ WARNING: Foreign-born percentage outside valid range [0,1]")
            results['foreign_born_valid'] = False
        else:
            print("  ✓ Foreign-born percentage in valid range [0,100%]")
            results['foreign_born_valid'] = True

    return results

def identify_outliers(df):
    """
    Identify potential outliers in key variables.

    Uses IQR method (values > Q3 + 1.5*IQR or < Q1 - 1.5*IQR)

    Args:
        df: Input DataFrame

    Returns:
        dict: Outlier information by variable
    """
    print("\n" + "=" * 60)
    print("Outlier Detection (IQR Method)")
    print("=" * 60)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    key_vars = [col for col in ['simpson_index', 'shannon_index', 'foreign_born_pct',
                                  'total_population', 'inrikes_fodda', 'utrikes_fodda']
                if col in numeric_cols]

    outlier_info = {}

    for col in key_vars:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        n_outliers = len(outliers)

        if n_outliers > 0:
            print(f"\n{col}:")
            print(f"  Outliers detected: {n_outliers} ({n_outliers/len(df)*100:.1f}%)")
            print(f"  Valid range: [{lower_bound:.2f}, {upper_bound:.2f}]")
            print(f"  Outlier values: {sorted(outliers[col].unique())[:10]}...")  # Show first 10

            outlier_info[col] = {
                'n_outliers': n_outliers,
                'pct_outliers': n_outliers/len(df)*100,
                'bounds': (lower_bound, upper_bound)
            }

    if not outlier_info:
        print("\n✓ No outliers detected in key variables")

    return outlier_info

def main():
    """
    Main execution: Validate all data.
    """
    print("=" * 60)
    print("Data Validation and Quality Checks")
    print("=" * 60)

    # Load data
    print(f"\nLoading data from {INPUT_FILE}...")

    if not Path(INPUT_FILE).exists():
        print(f"\nERROR: {INPUT_FILE} not found!")
        print("Please run 01_calculate_diversity_indices.py first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Data loaded: {len(df)} observations, {len(df.columns)} columns")

    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Run all validation checks
    results = {}

    # 1. Missing data
    results['missing'] = check_missing_data(df)

    # 2. CRITICAL: Sparsity analysis
    results['sparsity'] = analyze_sparsity(df)

    # 3. Aggregation recommendations
    results['strategies'] = recommend_aggregation_strategies(
        results['sparsity'].get('sparsity_stats', {})
    )

    # 4. Geographic coverage
    results['geography'] = check_geographic_coverage(df)
    if results['geography'] is not None:
        results['geography'].to_csv(f"{OUTPUT_DIR}/municipality_summary.csv")
        print(f"\nSaved: {OUTPUT_DIR}/municipality_summary.csv")

    # 5. Diversity indices validation
    results['diversity_valid'] = check_diversity_indices(df)

    # 6. Outlier detection
    results['outliers'] = identify_outliers(df)

    # Save summary report
    with open(f"{OUTPUT_DIR}/validation_report.txt", 'w', encoding='utf-8') as f:
        f.write("DATA VALIDATION REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Input file: {INPUT_FILE}\n")
        f.write(f"Total observations: {len(df):,}\n\n")

        f.write("CRITICAL FINDINGS\n")
        f.write("=" * 60 + "\n\n")

        if results['sparsity'].get('sparsity_stats'):
            stats = results['sparsity']['sparsity_stats']
            f.write("Data Sparsity Issue:\n")
            f.write(f"  - Only {stats['estimated_coverage_pct']:.1f}% of DeSO areas have permits\n")
            f.write(f"  - Average {stats['avg_permits_per_deso']:.2f} permits per DeSO\n")
            f.write(f"  - RECOMMENDATION: Aggregate to municipality level for primary analysis\n\n")

        f.write("All validation checks completed. See detailed output above.\n")

    print(f"\nSaved: {OUTPUT_DIR}/validation_report.txt")

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    print("\nKey takeaway:")
    print("  → Use MUNICIPALITY-LEVEL aggregation for main analysis")
    print("  → Use DeSO-level for urban sensitivity analysis")
    print("  → Consider count/binary models as alternative specifications")

if __name__ == "__main__":
    main()
