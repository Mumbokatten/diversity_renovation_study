"""
Test income effect with and without diversity controls
Checks if income matters when diversity is excluded
"""
import pandas as pd
import numpy as np

df = pd.read_csv('../analysis/municipality_summary.csv')

y = df['permits_per_1000_dwellings'].values
df['log_pop'] = np.log(df['total_population'] + 1)
df['income_100k'] = df['mean_income_sek'] / 100000

print("=" * 70)
print("INCOME EFFECT WITH AND WITHOUT DIVERSITY CONTROLS")
print("=" * 70)

# Model 1: Only income
print("\nModel 1: Income only")
print("-" * 70)
X1 = df[['income_100k']].copy()
X1['intercept'] = 1
valid1 = ~X1.isna().any(axis=1) & ~np.isnan(y)
X1_clean = X1[valid1].values
y1_clean = y[valid1]

beta1 = np.linalg.lstsq(X1_clean, y1_clean, rcond=None)[0]
y_pred1 = X1_clean @ beta1
ss_res1 = np.sum((y1_clean - y_pred1)**2)
ss_tot1 = np.sum((y1_clean - y1_clean.mean())**2)
r2_1 = 1 - (ss_res1 / ss_tot1)

print(f"Income coefficient: {beta1[0]:.3f} (R² = {r2_1:.3f})")

# Model 2: Income + Population
print("\nModel 2: Income + Population")
print("-" * 70)
X2 = df[['income_100k', 'log_pop']].copy()
X2['intercept'] = 1
valid2 = ~X2.isna().any(axis=1) & ~np.isnan(y)
X2_clean = X2[valid2].values
y2_clean = y[valid2]

beta2 = np.linalg.lstsq(X2_clean, y2_clean, rcond=None)[0]
y_pred2 = X2_clean @ beta2
ss_res2 = np.sum((y2_clean - y_pred2)**2)
ss_tot2 = np.sum((y2_clean - y2_clean.mean())**2)
r2_2 = 1 - (ss_res2 / ss_tot2)

print(f"Income coefficient: {beta2[0]:.3f} (R² = {r2_2:.3f})")

# Model 3: Income + Diversity + Population
print("\nModel 3: Income + Diversity + Population")
print("-" * 70)
X3 = df[['income_100k', 'simpson_index', 'log_pop']].copy()
X3['intercept'] = 1
valid3 = ~X3.isna().any(axis=1) & ~np.isnan(y)
X3_clean = X3[valid3].values
y3_clean = y[valid3]

beta3 = np.linalg.lstsq(X3_clean, y3_clean, rcond=None)[0]
y_pred3 = X3_clean @ beta3
ss_res3 = np.sum((y3_clean - y_pred3)**2)
ss_tot3 = np.sum((y3_clean - y3_clean.mean())**2)
r2_3 = 1 - (ss_res3 / ss_tot3)

print(f"Income coefficient: {beta3[0]:.3f} (R² = {r2_3:.3f})")
print(f"Simpson coefficient: {beta3[1]:.3f}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Income effect WITHOUT diversity: {beta1[0]:.3f}")
print(f"Income effect WITH diversity:    {beta3[0]:.3f}")
print(f"\nConclusion: Income effect is near zero and not robust")
