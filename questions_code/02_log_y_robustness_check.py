"""
Robustness Check: Log(Y) Specification
Compare level vs log dependent variable
"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('../analysis/municipality_summary.csv')

# Prepare variables
df['log_pop'] = np.log(df['total_population'] + 1)
df['income_100k'] = df['mean_income_sek'] / 100000

# Level Y
y_level = df['permits_per_1000_dwellings'].values

# Log Y (add small constant to avoid log(0))
y_log = np.log(df['permits_per_1000_dwellings'] + 0.01).values

print("=" * 70)
print("ROBUSTNESS CHECK: LOG(Y) vs LEVEL Y")
print("=" * 70)

results = []

# Run regressions for both specifications
for spec_name, y_var in [('Level Y', y_level), ('Log(Y)', y_log)]:
    print(f"\n{spec_name}")
    print("-" * 70)

    # Full model: Simpson + Log Pop + Income + Owner
    X = df[['simpson_index', 'log_pop', 'income_100k', 'owner_share']].copy()
    X['intercept'] = 1
    valid = ~X.isna().any(axis=1) & ~np.isnan(y_var)
    X_clean = X[valid].values
    y_clean = y_var[valid]

    # OLS
    beta = np.linalg.lstsq(X_clean, y_clean, rcond=None)[0]
    y_pred = X_clean @ beta
    ss_res = np.sum((y_clean - y_pred)**2)
    ss_tot = np.sum((y_clean - y_clean.mean())**2)
    r2 = 1 - (ss_res / ss_tot)

    print(f"Intercept:        {beta[4]:.3f}")
    print(f"Simpson Index:    {beta[0]:.3f}")
    print(f"Log Population:   {beta[1]:.3f}")
    print(f"Income (100k):    {beta[2]:.3f}")
    print(f"Owner Share:      {beta[3]:.3f}")
    print(f"R-squared:        {r2:.3f}")
    print(f"N:                {len(y_clean)}")

    results.append({
        'Specification': spec_name,
        'Simpson_Index': beta[0],
        'Log_Population': beta[1],
        'Income_100k': beta[2],
        'Owner_Share': beta[3],
        'R_squared': r2,
        'N': len(y_clean)
    })

# Create comparison table
results_df = pd.DataFrame(results)
print("\n" + "=" * 70)
print("COMPARISON TABLE")
print("=" * 70)
print(results_df.to_string(index=False))

# Save results
results_df.to_csv('../analysis/results/robustness_log_y.csv', index=False)
print("\nResults saved to: analysis/results/robustness_log_y.csv")
