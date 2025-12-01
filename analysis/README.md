# Analysis Scripts

This folder contains all Python scripts used to perform the analysis for the research paper on ethnic diversity and renovation investment in Swedish municipalities.

## Main Analysis Pipeline

### 01_calculate_diversity_indices.py
- **Purpose**: Calculate diversity indices (Simpson, Shannon) for each municipality
- **Inputs**: DeSO-level demographic data from SCB
- **Outputs**: Municipality-level diversity indices
- **Key Metrics**: Simpson Index, Shannon Entropy, Foreign-born percentage

### 02_regression_analysis.py
- **Purpose**: Run main OLS regressions
- **Methods**: OLS with robust standard errors
- **Models**: Progressive model specifications adding controls
- **Outputs**: Regression tables and coefficients

### 03_validate_data.py
- **Purpose**: Data quality checks and validation
- **Methods**: Check for missing values, outliers, data integrity
- **Outputs**: Validation reports

### 04_create_visualizations.py
- **Purpose**: Generate all figures for the paper
- **Outputs**:
  - Geographic choropleth maps
  - Bivariate map (diversity × permits)
  - Scatter plots with regression lines
  - Histograms and distributions

### 05_paper_table4_regressions.py
- **Purpose**: Reproduce exact regression results from Table 4 in the paper
- **Methods**: OLS regression using numpy for full transparency
- **Models**:
  - Model 1: Simpson Index only
  - Model 2: + Log Population
  - Model 3: + Income + Owner Share (MAIN MODEL)
  - Model 4: Alternative diversity measure (Shannon)
- **Outputs**: `results/table4_regression_results.csv`
- **Key Finding**: Simpson Index coefficient = -1.870 (21.5% effect)

## Running the Scripts

All scripts should be run from the project root directory:

```bash
# From diversity_renovation_study/
python analysis/01_calculate_diversity_indices.py
python analysis/02_regression_analysis.py
python analysis/03_validate_data.py
python analysis/04_create_visualizations.py
python analysis/05_paper_table4_regressions.py
```

## Required Data Files

- `analysis/municipality_summary.csv` - Main analysis dataset
- `analysis/permits_with_diversity_municipality.csv` - Permits with diversity data
- `analysis/permits_with_demographics_municipality.csv` - Permits with demographics

## Output Locations

- **Results**: `analysis/results/`
- **Figures**: `analysis/figures/`
- **Maps**: `analysis/` (top-level for inclusion in paper)

## Exploratory and Robustness Checks

For exploratory analyses and robustness checks performed during the research process, see the `questions_code/` folder in the project root.

## Dependencies

```python
pandas
numpy
matplotlib
statsmodels  # For robust standard errors in 02
scipy        # For statistical tests
```

## Notes

- All regression models use OLS estimation
- Model 3 (full specification) is the main model reported in the paper
- The Simpson Index ranges from 0 (no diversity) to ~0.83 (maximum theoretical diversity)
- Permits per 1,000 dwellings is the dependent variable throughout
- All scripts handle missing data by dropping observations with NaN values in relevant columns
