# Questions Code Folder

This folder contains exploratory analyses and robustness checks performed during the research process.

## Scripts

### 01_multicollinearity_check.py
- **Purpose**: Check for multicollinearity between income and diversity
- **Methods**: VIF analysis, correlation matrix
- **Key Finding**: No multicollinearity (all VIFs < 1.5, r(diversity, income) = 0.185)

### 02_log_y_robustness_check.py
- **Purpose**: Test whether results are robust to log-transformation of dependent variable
- **Methods**: Compare level vs log(Y) specifications
- **Key Finding**: Diversity effect robust (β = -1.870 for level, β = -1.970 for log)
- **Output**: `../analysis/results/robustness_log_y.csv`

### 03_income_effect_without_diversity.py
- **Purpose**: Test whether income has an effect when diversity is excluded
- **Methods**: Progressive addition of controls
- **Key Finding**: Income effect weak and unstable (-0.183 without controls, +0.046 with full controls)

## Running the Scripts

From this directory:
```bash
python 01_multicollinearity_check.py
python 02_log_y_robustness_check.py
python 03_income_effect_without_diversity.py
```

All scripts assume they are run from the `questions_code/` directory and reference data files using relative paths (`../analysis/`).

## Results Added to Paper

- **Table 6**: Log(Y) robustness check (from script 02)
- **Section 5.5**: Discussion of multicollinearity and endogeneity (from scripts 01 and 03)
