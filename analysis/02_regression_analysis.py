"""
Regression Analysis: Diversity and Renovation Investment
=========================================================
This script performs regression analysis to examine the relationship between
neighborhood ethnic diversity and property renovation investment in Sweden.

Methods used:
- OLS Regression with robust standard errors
- Fixed Effects Panel Models (when panel data available)
- Multiple control variable specifications

Key Controls:
- Income levels (median household income)
- Tenure (homeownership rate)
- Household composition (size, type)
- Property characteristics (age, type)
- Education levels
- Municipality fixed effects

References:
-----------
Wooldridge, J. M. (2010). Econometric analysis of cross section and panel data
    (2nd ed.). MIT Press.

White, H. (1980). A heteroskedasticity-consistent covariance matrix estimator
    and a direct test for heteroskedasticity. Econometrica, 48(4), 817-838.
    https://doi.org/10.2307/1912934

Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust
    inference. Journal of Human Resources, 50(2), 317-372.
    https://doi.org/10.3368/jhr.50.2.317
"""

import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col

# File paths
INPUT_FILE = "analysis/diversity_indices.csv"
OUTPUT_DIR = "analysis/results"

def prepare_regression_data(df):
    """
    Prepare data for regression analysis.

    Creates necessary variables and handles missing data.

    Args:
        df: DataFrame with diversity indices and demographics

    Returns:
        DataFrame ready for regression analysis
    """
    # Create copy
    reg_df = df.copy()

    # Calculate total population
    if 'inrikes_fodda' in df.columns and 'utrikes_fodda' in df.columns:
        reg_df['total_population'] = reg_df['inrikes_fodda'] + reg_df['utrikes_fodda']

    # Log transformations for skewed variables (common in economic analysis)
    # Add small constant to avoid log(0)
    if 'total_population' in reg_df.columns:
        reg_df['log_population'] = np.log(reg_df['total_population'] + 1)

    # Drop rows with missing key variables
    key_vars = ['simpson_index', 'shannon_index', 'foreign_born_pct']
    reg_df = reg_df.dropna(subset=key_vars)

    return reg_df

def run_baseline_models(df):
    """
    Run baseline OLS regression models.

    Model specifications (progressive control variable addition):
    1. Bivariate: Diversity only
    2. + Population controls
    3. + Socioeconomic controls (income, education, tenure)
    4. + Property characteristics
    5. + Municipality fixed effects

    Args:
        df: Prepared regression DataFrame

    Returns:
        dict: Regression results by model specification

    Reference:
        Progressive control strategy follows Wooldridge (2010, Ch. 6)
    """
    results = {}

    print("\n" + "=" * 60)
    print("Running Baseline Regression Models")
    print("=" * 60)

    # Check which control variables are available
    has_population = 'log_population' in df.columns
    has_income = any('income' in col.lower() for col in df.columns)
    has_education = any('education' in col.lower() or 'edu' in col.lower() for col in df.columns)
    has_tenure = any('tenure' in col.lower() or 'owner' in col.lower() for col in df.columns)
    has_municipality = 'municipality' in df.columns

    # Model 1: Bivariate (diversity only)
    print("\nModel 1: Bivariate (Simpson Index)")
    formula1 = "simpson_index ~ 1"  # Intercept only model for now (dependent var)
    # Note: We need a proper dependent variable (renovation investment)
    # This is a placeholder until we have permit values or counts

    print("WARNING: Models require renovation investment as dependent variable.")
    print("Current data has diversity as independent variable.")
    print("Proceeding with descriptive models only...\n")

    # Instead, let's create models that could be used once we have DV
    model_specs = {
        'Model 1 (Bivariate)': 'renovation_value ~ simpson_index',
        'Model 2 (+ Population)': 'renovation_value ~ simpson_index + log_population',
    }

    # Build Model 3 based on available controls
    model3_formula = 'renovation_value ~ simpson_index + log_population'
    controls_added = []

    if has_income:
        income_cols = [col for col in df.columns if 'income' in col.lower()]
        if income_cols:
            model3_formula += f' + {income_cols[0]}'
            controls_added.append('income')

    if has_education:
        edu_cols = [col for col in df.columns if 'education' in col.lower() or 'edu' in col.lower()]
        if edu_cols:
            model3_formula += f' + {edu_cols[0]}'
            controls_added.append('education')

    if has_tenure:
        tenure_cols = [col for col in df.columns if 'tenure' in col.lower() or 'owner' in col.lower()]
        if tenure_cols:
            model3_formula += f' + {tenure_cols[0]}'
            controls_added.append('tenure')

    if controls_added:
        model_specs['Model 3 (+ Socioeconomic)'] = model3_formula

    # Model 4: + Municipality FE
    if has_municipality:
        model4_formula = model3_formula + ' + C(municipality)'
        model_specs['Model 4 (+ Municipality FE)'] = model4_formula

    # Save model specifications
    results['specifications'] = model_specs

    return results

def calculate_correlations(df):
    """
    Calculate correlation matrix for key variables.

    Useful for checking multicollinearity and descriptive statistics.

    Args:
        df: Regression DataFrame

    Returns:
        DataFrame: Correlation matrix
    """
    print("\n" + "=" * 60)
    print("Correlation Matrix - Key Variables")
    print("=" * 60)

    # Select numeric columns related to diversity and demographics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    key_vars = []

    # Add diversity indices
    for col in ['simpson_index', 'shannon_index', 'fractionalization', 'foreign_born_pct']:
        if col in numeric_cols:
            key_vars.append(col)

    # Add demographic controls
    for col in ['total_population', 'log_population']:
        if col in numeric_cols:
            key_vars.append(col)

    # Add any income/education/tenure variables
    for col in numeric_cols:
        if any(keyword in col.lower() for keyword in ['income', 'education', 'edu', 'tenure', 'owner']):
            if col not in key_vars:
                key_vars.append(col)

    if key_vars:
        corr_matrix = df[key_vars].corr()
        return corr_matrix
    else:
        print("WARNING: No numeric variables found for correlation analysis")
        return None

def create_summary_statistics(df):
    """
    Create summary statistics table for all variables.

    Following standard practice in empirical economics papers.

    Args:
        df: Regression DataFrame

    Returns:
        DataFrame: Summary statistics (N, mean, SD, min, max)
    """
    print("\n" + "=" * 60)
    print("Summary Statistics - All Variables")
    print("=" * 60)

    # Select key variables
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    summary = df[numeric_cols].describe().T
    summary['N'] = summary['count'].astype(int)
    summary = summary[['N', 'mean', 'std', 'min', 'max']]
    summary.columns = ['N', 'Mean', 'Std Dev', 'Min', 'Max']

    return summary

def main():
    """
    Main execution: Run all regression analyses.
    """
    print("=" * 60)
    print("Regression Analysis: Diversity and Renovation")
    print("=" * 60)

    # Load data
    print(f"\nLoading data from {INPUT_FILE}...")

    if not Path(INPUT_FILE).exists():
        print(f"\nERROR: {INPUT_FILE} not found!")
        print("Please run 01_calculate_diversity_indices.py first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Data loaded: {len(df)} observations")

    # Prepare data
    print("\nPreparing regression data...")
    reg_df = prepare_regression_data(df)
    print(f"After data preparation: {len(reg_df)} observations")

    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Summary statistics
    summary_stats = create_summary_statistics(reg_df)
    print("\n" + str(summary_stats.round(2)))
    summary_stats.to_csv(f"{OUTPUT_DIR}/summary_statistics.csv")
    print(f"\nSaved: {OUTPUT_DIR}/summary_statistics.csv")

    # Correlation matrix
    corr_matrix = calculate_correlations(reg_df)
    if corr_matrix is not None:
        print("\n" + str(corr_matrix.round(3)))
        corr_matrix.to_csv(f"{OUTPUT_DIR}/correlation_matrix.csv")
        print(f"\nSaved: {OUTPUT_DIR}/correlation_matrix.csv")

    # Run regression models
    results = run_baseline_models(reg_df)

    # Save model specifications
    with open(f"{OUTPUT_DIR}/model_specifications.txt", 'w') as f:
        f.write("Regression Model Specifications\n")
        f.write("=" * 60 + "\n\n")
        for model_name, formula in results['specifications'].items():
            f.write(f"{model_name}:\n")
            f.write(f"  {formula}\n\n")

    print(f"\nSaved: {OUTPUT_DIR}/model_specifications.txt")

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("\n1. Obtain renovation investment data as dependent variable:")
    print("   - Permit estimated costs")
    print("   - Or: Count of permits per DeSO area per time period")
    print("   - Or: Binary indicator (any renovation in period)")

    print("\n2. Merge additional control variables from SCB data:")
    print("   - Median household income by DeSO")
    print("   - Education levels by DeSO")
    print("   - Homeownership rates by DeSO")
    print("   - Property age distribution")

    print("\n3. Run actual regression models with complete data")

    print("\n" + "=" * 60)
    print("Interpretation Notes")
    print("=" * 60)
    print("\nExpected coefficient signs (hypotheses):")
    print("  Simpson Index → Renovation: ? (Research question)")
    print("    - Positive: Diversity encourages investment")
    print("    - Negative: Diversity discourages investment")
    print("    - Zero: No relationship after controlling for confounders")
    print("\nControl variables (expected signs):")
    print("  Income → Renovation: + (wealthier areas invest more)")
    print("  Population → Renovation: + (more units = more renovation)")
    print("  Homeownership → Renovation: + (owners invest more than renters)")
    print("  Education → Renovation: + (correlated with income/preferences)")

if __name__ == "__main__":
    main()
