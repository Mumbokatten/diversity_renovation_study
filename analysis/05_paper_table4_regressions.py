"""
Reproduce Table 4 from Research Paper
======================================
This script reproduces the exact regression results shown in Table 4:
"OLS Regression Results - Permits per 1,000 Dwellings"

Models:
- Model 1: Simpson Index only
- Model 2: + Log Population
- Model 3: + Income + Owner Share
- Model 4: Alternative diversity measures

All models use OLS with no robust standard errors in this implementation.
For publication-quality standard errors, use statsmodels with robust SE.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def run_ols(X, y):
    """
    Simple OLS regression: beta = (X'X)^-1 X'y

    Returns:
        beta: coefficients
        r2: R-squared
        n: sample size
    """
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - (ss_res / ss_tot)
    return beta, r2, len(y)

def main():
    print("=" * 70)
    print("REPRODUCING TABLE 4: OLS REGRESSION RESULTS")
    print("Dependent Variable: Permits per 1,000 Dwellings")
    print("=" * 70)

    # Load data
    df = pd.read_csv('analysis/municipality_summary.csv')

    # Dependent variable
    y = df['permits_per_1000_dwellings'].values

    # Prepare independent variables
    df['log_population'] = np.log(df['total_population'] + 1)
    df['income_100k'] = df['mean_income_sek'] / 100000

    results = []

    # ==========================================
    # MODEL 1: Simpson Index only
    # ==========================================
    print("\nMODEL 1: Simpson Index Only")
    print("-" * 70)

    X1 = df[['simpson_index']].copy()
    X1['intercept'] = 1
    valid1 = ~X1.isna().any(axis=1) & ~np.isnan(y)
    X1_clean = X1[valid1].values
    y1_clean = y[valid1]

    beta1, r2_1, n1 = run_ols(X1_clean, y1_clean)

    print(f"Simpson Index:  {beta1[0]:.3f}")
    print(f"Intercept:      {beta1[1]:.3f}")
    print(f"R-squared:      {r2_1:.3f}")
    print(f"N:              {n1}")

    results.append({
        'Model': 'Model 1',
        'Simpson': beta1[0],
        'Log_Pop': np.nan,
        'Income': np.nan,
        'Owner': np.nan,
        'R2': r2_1,
        'N': n1
    })

    # ==========================================
    # MODEL 2: + Log Population
    # ==========================================
    print("\nMODEL 2: + Log Population")
    print("-" * 70)

    X2 = df[['simpson_index', 'log_population']].copy()
    X2['intercept'] = 1
    valid2 = ~X2.isna().any(axis=1) & ~np.isnan(y)
    X2_clean = X2[valid2].values
    y2_clean = y[valid2]

    beta2, r2_2, n2 = run_ols(X2_clean, y2_clean)

    print(f"Simpson Index:  {beta2[0]:.3f}")
    print(f"Log Population: {beta2[1]:.3f}")
    print(f"Intercept:      {beta2[2]:.3f}")
    print(f"R-squared:      {r2_2:.3f}")
    print(f"N:              {n2}")

    results.append({
        'Model': 'Model 2',
        'Simpson': beta2[0],
        'Log_Pop': beta2[1],
        'Income': np.nan,
        'Owner': np.nan,
        'R2': r2_2,
        'N': n2
    })

    # ==========================================
    # MODEL 3: + Income + Owner Share (MAIN MODEL)
    # ==========================================
    print("\nMODEL 3: + Income + Owner Share (MAIN)")
    print("-" * 70)

    X3 = df[['simpson_index', 'log_population', 'income_100k', 'owner_share']].copy()
    X3['intercept'] = 1
    valid3 = ~X3.isna().any(axis=1) & ~np.isnan(y)
    X3_clean = X3[valid3].values
    y3_clean = y[valid3]

    beta3, r2_3, n3 = run_ols(X3_clean, y3_clean)

    print(f"Simpson Index:  {beta3[0]:.3f}")
    print(f"Log Population: {beta3[1]:.3f}")
    print(f"Income (100k):  {beta3[2]:.3f}")
    print(f"Owner Share:    {beta3[3]:.3f}")
    print(f"Intercept:      {beta3[4]:.3f}")
    print(f"R-squared:      {r2_3:.3f}")
    print(f"N:              {n3}")

    results.append({
        'Model': 'Model 3',
        'Simpson': beta3[0],
        'Log_Pop': beta3[1],
        'Income': beta3[2],
        'Owner': beta3[3],
        'R2': r2_3,
        'N': n3
    })

    # ==========================================
    # MODEL 4: Alternative diversity measures
    # ==========================================
    print("\nMODEL 4: Shannon Entropy (Alternative Measure)")
    print("-" * 70)

    X4 = df[['shannon_index', 'log_population', 'income_100k', 'owner_share']].copy()
    X4['intercept'] = 1
    valid4 = ~X4.isna().any(axis=1) & ~np.isnan(y)
    X4_clean = X4[valid4].values
    y4_clean = y[valid4]

    beta4, r2_4, n4 = run_ols(X4_clean, y4_clean)

    print(f"Shannon Index:  {beta4[0]:.3f}")
    print(f"Log Population: {beta4[1]:.3f}")
    print(f"Income (100k):  {beta4[2]:.3f}")
    print(f"Owner Share:    {beta4[3]:.3f}")
    print(f"R-squared:      {r2_4:.3f}")

    results.append({
        'Model': 'Model 4 (Shannon)',
        'Simpson': np.nan,
        'Shannon': beta4[0],
        'Log_Pop': beta4[1],
        'Income': beta4[2],
        'Owner': beta4[3],
        'R2': r2_4,
        'N': n4
    })

    # ==========================================
    # SUMMARY TABLE
    # ==========================================
    print("\n" + "=" * 70)
    print("SUMMARY TABLE (matches Table 4 in paper)")
    print("=" * 70)

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    # Save results
    Path("analysis/results").mkdir(parents=True, exist_ok=True)
    results_df.to_csv('analysis/results/table4_regression_results.csv', index=False)

    print("\n" + "=" * 70)
    print("Results saved to: analysis/results/table4_regression_results.csv")
    print("=" * 70)

    # KEY FINDING
    print("\nKEY FINDING:")
    print(f"Simpson Index coefficient in Model 3: {beta3[0]:.3f}")
    print(f"Moving from 20th to 80th percentile (Simpson 0.19 -> 0.32):")
    print(f"  Effect = {beta3[0]:.3f} × 0.13 = {beta3[0]*0.13:.3f} permits/1000")
    print(f"  Percentage effect = {(beta3[0]*0.13 / 1.127) * 100:.1f}%")

if __name__ == "__main__":
    main()
