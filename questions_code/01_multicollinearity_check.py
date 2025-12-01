"""
Check for multicollinearity between income and diversity
VIF analysis and correlation matrix
"""
import pandas as pd
import numpy as np
from numpy.linalg import inv

# Load data
df = pd.read_csv('../analysis/municipality_summary.csv')

print("CORRELATION ANALYSIS: Income vs Diversity")
print("=" * 60)

# Calculate correlations
corr_simpson_income = df['simpson_index'].corr(df['mean_income_sek'])
corr_foreign_income = df['foreign_born_pct'].corr(df['mean_income_sek'])

print(f"\nSimpson Index vs Mean Income: {corr_simpson_income:.3f}")
print(f"Foreign-born % vs Mean Income: {corr_foreign_income:.3f}")

# Also check with owner share
corr_simpson_owner = df['simpson_index'].corr(df['owner_share'])
corr_income_owner = df['mean_income_sek'].corr(df['owner_share'])

print(f"\nSimpson Index vs Owner Share: {corr_simpson_owner:.3f}")
print(f"Mean Income vs Owner Share: {corr_income_owner:.3f}")

# VIF calculation
X = df[['simpson_index', 'mean_income_sek', 'owner_share']].dropna()
X_std = (X - X.mean()) / X.std()
X_with_const = np.column_stack([np.ones(len(X_std)), X_std])

print("\n" + "=" * 60)
print("VARIANCE INFLATION FACTORS (VIF)")
print("=" * 60)
print("Rule of thumb: VIF > 10 indicates serious multicollinearity")
print("               VIF > 5 indicates moderate multicollinearity\n")

for i, col in enumerate(['simpson_index', 'mean_income_sek', 'owner_share']):
    y = X_std.iloc[:, i].values
    X_others = np.delete(X_with_const, i+1, axis=1)

    beta = inv(X_others.T @ X_others) @ X_others.T @ y
    y_pred = X_others @ beta

    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - (ss_res / ss_tot)

    vif = 1 / (1 - r2)
    status = "OK" if vif < 5 else ("MODERATE" if vif < 10 else "SEVERE")
    print(f"{col:20s}: VIF = {vif:6.2f}  [{status}]")
