# Housing Study - Data Dictionary & Notes

## Data Sources
- **Permit Data**: Being scraped by other agent
- **Demographics Data**: SCB (Statistiska centralbyrån / Statistics Sweden)

---

## Study Hypotheses & Expected Findings

### Research Question

**Do residents in immigrant-heavy areas take worse care of their buildings / invest less in improvements?**

Building permits (for renovations, extensions, improvements) serve as a proxy for housing investment and upkeep.

### Primary Hypothesis

**H1: Higher foreign-born share → Lower building permit rates**

The logic:
- Lower permit rates = less renovation, fewer improvements, less maintenance
- If true: buildings in immigrant-heavy areas are being maintained/improved less
- Over time, these areas may deteriorate relative to native-dominated areas
- This would show up as: `correlation(foreign_born_share, permit_rate) < 0`

### Null Hypothesis

**H0: No correlation between foreign-born share and permit rates**

If no relationship:
- Residents invest equally in housing maintenance regardless of area demographics
- Permit rates driven by other factors (income, housing age, tenure) not who lives there
- `correlation(foreign_born_share, permit_rate) ≈ 0` after controlling for confounders

### Expected Data Patterns

| If We Find... | Interpretation |
|---------------|----------------|
| **Negative correlation** (high foreign-born → low permits) | Areas with immigrants receiving less investment; integration concern |
| **No correlation** (after controls) | Demographics don't predict development; integration working |
| **Positive correlation** | Unexpected - would need explanation (new construction attracting immigrants?) |

### Key Variables

| Variable | Role | Source |
|----------|------|--------|
| Building permits per capita | **Outcome** (Y) | Permit data |
| Foreign-born population share | **Predictor** (X) | SCB |
| Tenure composition | **Confounder** | SCB - rental areas have fewer individual permits regardless |
| Income levels | **Confounder** | SCB - affects ability to invest in housing |
| Population density | **Confounder** | SCB - urban/rural differences |
| Housing stock age | **Confounder** | SCB - older stock may need more permits |

### Analysis Approach

1. **Descriptive**: Scatter plot of permit rates vs foreign-born share by municipality
2. **Bivariate correlation**: Raw relationship
3. **Multiple regression** (controlling for confounders):
   ```
   permit_rate ~ foreign_born_share + tenure_mix + income + density + housing_age
   ```
4. **Key question**: Does foreign-born share remain significant after controlling for tenure?

### Critical Confounder: Tenure Mix

**This may explain the relationship:**
- Immigrant-heavy areas often have high rental share
- Renters can't apply for permits (landlord decides)
- So low permits in immigrant areas may be a **tenure effect**, not a discrimination/disinvestment effect

**Analysis must separate:**
- Is it `high foreign-born → low permits`?
- Or is it `high rental → low permits` (and immigrants happen to live in rentals)?

### Potential Conclusions

**If H1 confirmed (negative correlation persists after controls):**
> "Areas with higher foreign-born populations show significantly lower building permit rates, even after controlling for tenure composition, income, and density. This suggests systematic underinvestment in immigrant-heavy areas - these neighborhoods are developing more slowly than comparable native-dominated areas."

**If H0 supported (no correlation after controls):**
> "Foreign-born population share does not predict building permit rates once tenure composition and income are controlled for. Lower permit rates in immigrant-heavy areas are explained by housing tenure (rental vs ownership) rather than demographic composition per se."

### Policy Implications

**If H1 confirmed:**
- Targeted investment programs for immigrant-heavy areas may be needed
- Investigate why landlords in these areas invest less
- Potential discrimination in municipal permit processes?

**If H0 supported:**
- Focus on tenure diversification rather than demographic targeting
- Help immigrants access homeownership to enable housing investment

---

## Key Variables to Download from SCB

### 1. Population Demographics
| Variable | SCB Table | Notes |
|----------|-----------|-------|
| Population by municipality | BE0101 | Use "folkmängd" tables |
| Age distribution | BE0101 | 5-year age groups common |
| Household composition | HE0111 | Number of persons per household |
| Migration flows | BE0101 | In-migration (inflyttning), out-migration (utflyttning) |

### 2. Economic Indicators
| Variable | SCB Table | Notes |
|----------|-----------|-------|
| Disposable income | HE0110 | **See income warnings below** |
| Employment rate | AM0207 | Registered employment 16-64 years |
| Unemployment | AM0401 | AKU survey data |

### 3. Housing Variables
| Variable | SCB Table | Notes |
|----------|-----------|-------|
| Housing stock | BO0104 | By dwelling type and tenure |
| Housing prices | BO0501 | Småhus prices by region |
| Living space | BO0102 | m² per person |

---

## IMPORTANT: Potentially Confusing Numbers

### Income Data - CRITICAL NOTES

1. **Individual vs Household Income**
   - SCB reports BOTH - make sure you know which you're using
   - "Sammanräknad förvärvsinkomst" = total earned income (individual)
   - "Disponibel inkomst" = disposable income (can be per person or per household)
   - Household income ≠ individual income × household size (due to economies of scale, tax effects)

2. **Before vs After Tax**
   - "Förvärvsinkomst" = earned income (before tax)
   - "Disponibel inkomst" = disposable income (after tax + transfers)
   - Difference can be 30-50% depending on income level

3. **Median vs Mean**
   - SCB often reports MEDIAN (less affected by outliers)
   - Mean income is typically 10-20% higher than median
   - Always check which measure you're using

4. **Regional Variation Examples (2023 approximate)**
   - Danderyd (wealthy Stockholm suburb): ~500,000 SEK median disposable income
   - National median: ~280,000 SEK
   - Some northern municipalities: ~230,000 SEK
   - **Ratio of richest to poorest municipality can be 2:1 or more**

5. **Time Lag**
   - Income data typically has 1-2 year lag (2024 data shows 2022 incomes)

### Population Data - NOTES

1. **Registered vs Actual Residents**
   - SCB uses "folkbokförd" (registered) population
   - Actual residents may differ (students, temporary workers, undocumented)
   - University towns especially affected

2. **Reference Date**
   - End-of-year (31 December) is standard
   - Some quarterly data uses other dates

### Geographic Boundaries - CRITICAL

1. **Geographic Levels in Sweden**
   | Level | Swedish | Count (approx) | Notes |
   |-------|---------|----------------|-------|
   | National | Riket | 1 | Whole country |
   | County | Län | 21 | Regional administration |
   | Municipality | Kommun | 290 | Main local unit |
   | District | Distrikt | ~2,500 | Sub-municipal |
   | DeSO | DeSO | ~5,984 | Demographic statistics areas (new) |
   | RegSO | RegSO | ~3,363 | Regional statistics areas |

2. **IMPORTANT: Municipality Codes**
   - 4-digit codes (e.g., 0180 = Stockholm, 1480 = Göteborg, 1280 = Malmö)
   - First 2 digits = county (län)
   - Codes are stable but boundaries occasionally change

3. **FA-regioner vs LA-regioner**
   - Functional labor market regions - NOT administrative boundaries
   - Useful for commuting analysis but harder to match with other data

### Time Periods

1. **Annual vs Quarterly**
   - Most demographic data is annual (December 31)
   - Some economic data is quarterly
   - Make sure permit data time period matches!

2. **Calendar Year vs Academic Year**
   - Education data may use different periods

---

## Data Quality Flags

When downloading, note:
- ".." = data not available
- "0" = actual zero OR rounded to zero (check context)
- Some small-area data is suppressed for privacy

---

## Matching Keys

To join permit data with demographics:
- **Primary key**: Municipality code (kommunkod, 4 digits)
- **Secondary**: Year
- Ensure consistent coding (leading zeros matter: "0180" not "180")

---

## Files Downloaded

| Filename | Source | Variables | Geography | Time Period | Downloaded |
|----------|--------|-----------|-----------|-------------|------------|
| population_by_municipality.csv | SCB BE0101A/BefolkningNy | Population by gender, marital status | 290 municipalities | 2019-2024 | 2025-12-01 |
| income_by_municipality.csv | SCB HE0110A/SamForvInk1 | Mean income, Median income, Total sum, Person count | 290 municipalities | 2019-2023 | 2025-12-01 |
| housing_stock_by_municipality.csv | SCB BO0104D/BO0104T04 | Dwelling count by type and tenure | 290 municipalities | 2019-2024 | 2025-12-01 |
| households_by_municipality.csv | SCB BE0101S/HushallT09 | Household statistics | 50 municipalities (sample) | 2023 | 2025-12-01 |
| dependency_ratio_by_municipality.csv | SCB BE0101A/FkvotHVD | Age dependency ratios | 290 municipalities | 2019-2024 | 2025-12-01 |
| migration_by_municipality.csv | SCB BE0101J/Flyttningar97 | In/out migration, net flows | 290 municipalities | 2019-2024 | 2025-12-01 |
| land_area_by_municipality.csv | SCB MI0802/Areal2025 | Land area (km²) | 290 municipalities | 2025 | 2025-12-01 |
| **foreign_born_by_municipality.csv** | SCB BE0101E/FolkmRegFlandK | Total pop + Sweden-born (calculate foreign-born) | 290 municipalities | 2019-2024 | 2025-12-01 |

### DeSO-Level Data (for matching with permits)

| Filename | Source | Variables | Geography | Time Period | Downloaded |
|----------|--------|-----------|-----------|-------------|------------|
| **deso_foreign_born.csv** | SCB BE0101Y/FolkmDesoLandKon | Sweden-born + Total (calculate foreign-born share) | ~3,363 DeSO areas | 2020-2023 | 2025-12-01 |
| **deso_income.csv** | SCB HE0110I/Tab2InkDesoN | Mean wage income (tkr) | ~3,363 DeSO areas | 2020-2023 | 2025-12-01 |
| **deso_housing_tenure.csv** | SCB BO0104X/BO0104T10N | Dwellings by tenure (hyresrätt, bostadsrätt, äganderätt) | ~3,363 DeSO areas | 2020-2023 | 2025-12-01 |

**DeSO = Demografiska statistikområden** (Demographic Statistics Areas)
- Small neighborhood-level areas (~1,000-3,000 residents each)
- 8-character codes: kommun (4 digits) + area identifier (4 chars)
- Example: "0114A0010" = Upplands Väsby, area A0010
- Use these for matching with permit data at neighborhood level

---

## Variable Details for Downloaded Files

### population_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | Format: "0114 Upplands Väsby" |
| civilstånd | Marital status | ogifta (unmarried), gifta (married), skilda (divorced), änklingar/änkor (widowed) |
| ålder | Age | "totalt ålder" = all ages |
| kön | Gender | män (men), kvinnor (women) |
| Folkmängd 20XX | Population count | Annual figures 2019-2024 |

**To get total population**: Sum across all marital statuses and genders, or filter to get subtotals.

### income_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | Format: "0114 Upplands Väsby" |
| kön | Gender | "totalt" = both combined |
| ålder | Age group | "totalt 20+ år" = adults 20+ |
| inkomstklass | Income class | "totalt" = all classes |
| Medelinkomst, tkr 20XX | **Mean income (tkr = thousands SEK)** | BEFORE TAX (förvärvsinkomst) |
| Medianinkomst, tkr 20XX | **Median income (tkr)** | BEFORE TAX |
| Totalsumma, mnkr 20XX | Total sum (millions SEK) | All earners combined |
| Antal personer 20XX | Number of persons | Persons with income |

**WARNING**: This is "Sammanräknad förvärvsinkomst" (total earned income) = BEFORE TAX. For after-tax income, use HE0110G tables (household disposable income).

### housing_stock_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | Format: "0114 Upplands Väsby" |
| hustyp | Housing type | småhus (small houses), flerbostadshus (apartments), övriga hus (other), specialbostäder (special housing) |
| upplåtelseform | Tenure type | hyresrätt (rental), bostadsrätt (tenant-owned), äganderätt (owner-occupied), uppgift saknas (unknown) |
| Antal 20XX | Number of dwellings | Annual figures 2019-2024 |

**Tenure types explained**:
- **Hyresrätt**: Rental apartments (public or private landlord)
- **Bostadsrätt**: Cooperative/tenant-owned (own shares in housing association)
- **Äganderätt**: Owner-occupied (typically single-family homes)

### households_by_municipality.csv
Limited sample - consider downloading full dataset if needed.

### dependency_ratio_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | Format: "0114 Upplands Väsby" |
| Försörjningskvot totalt 20XX | **Total dependency ratio** | (0-19 + 65+) / (20-64) × 100 |
| Försörjningskvot, från äldre 65+ 20XX | **Old-age dependency** | 65+ / (20-64) × 100 |
| Försörjningskvot, från yngre 0-19 20XX | **Youth dependency** | 0-19 / (20-64) × 100 |

**Interpretation**: Higher ratio = more dependents per working-age person. Affects housing needs (family homes vs elderly housing).

### migration_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | |
| ålder | Age group | "totalt ålder" = all ages |
| kön | Gender | män/kvinnor |
| Inflyttningar 20XX | Total in-migration | Domestic + international |
| Utflyttningar 20XX | Total out-migration | |
| Invandringar 20XX | Immigration (international) | |
| Utvandringar 20XX | Emigration (international) | |
| Flyttningsöverskott 20XX | **Net migration** | In - Out |
| Invandringsöverskott 20XX | Net international migration | |
| Inrikes inflyttningar 20XX | Domestic in-migration | |
| Inrikes utflyttningar 20XX | Domestic out-migration | |
| Inrikes flyttningsöverskott 20XX | Net domestic migration | |

**Use case**: High net in-migration → increased housing demand → more permits expected.

### land_area_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | |
| arealtyp | Area type | "landareal" = land (excluding water) |
| Kvadratkilometer 2025 | Land area in km² | |

**Use case**: Divide population by area to get **population density** (persons/km²). Urban vs rural distinction.

### foreign_born_by_municipality.csv
| Column | Description | Notes |
|--------|-------------|-------|
| region | Municipality code + name | Format: "0114 Upplands Väsby" |
| födelseregion | Birth region | "Samtliga födelseland" = Total, "Sverige" = Sweden-born |
| kön | Gender | "totalt" = both combined |
| Antal 20XX | Population count | Annual figures 2019-2024 |

**To calculate foreign-born share**:
```
foreign_born = total - sweden_born
foreign_born_share = foreign_born / total
```

**Integration metric**: This is the key outcome variable. Higher foreign-born share indicates areas where immigrants have settled. The question is whether permit rates correlate with integration patterns.

---

## CRITICAL: Tenure Effects on Building Permits

**This is a key confounding variable for permit analysis!**

### Who Can Apply for Bygglov (Building Permits)?

| Tenure Type | Swedish | Who Decides on Renovations? | Permit Applicant |
|-------------|---------|----------------------------|------------------|
| Äganderätt | Owner-occupied | **Owner (individual)** | Individual homeowner |
| Bostadsrätt | Tenant-owned coop | **BRF (housing association)** for exterior/structural; individual for interior | BRF or individual |
| Hyresrätt | Rental | **Landlord only** | Housing company |
| Specialbostäder | Student/elderly housing | **Institution** | Institution |

### Implications for Permit Data

1. **High rental share → Fewer individual permits**
   - Tenants cannot apply for permits themselves
   - All decisions made by landlord (often large housing companies like Allmännyttan)
   - Expect bulk/large-scale permits rather than many small ones

2. **High owner-occupied share → More individual permits**
   - Each homeowner can decide on extensions, renovations
   - More granular permit applications

3. **University towns** (e.g., Uppsala, Lund, Umeå)
   - High student housing share
   - Students are "registered" but not permanent
   - Low individual permit rates despite high population

4. **Suggested Control Variable**
   - Calculate: `owner_share = (äganderätt + bostadsrätt) / total_dwellings`
   - Or: `rental_share = hyresrätt / total_dwellings`
   - Include in regression models

### Municipality Examples (approximate)

| Municipality | Rental Share | Expected Permit Pattern |
|--------------|--------------|------------------------|
| Stockholm inner city | ~50-60% | Fewer individual permits |
| Danderyd | ~10-15% | Many individual permits |
| University towns | ~40-50% | Skewed by student housing |
| Rural municipalities | ~20-30% | Mix, but smaller population |

---

## Potential Confounding Variables Summary

| Variable | Data File | Why It Matters |
|----------|-----------|----------------|
| **Tenure mix** | housing_stock_by_municipality.csv | Determines WHO can apply for permits |
| **Age structure** | dependency_ratio_by_municipality.csv | Affects WHAT housing is needed |
| **Migration flows** | migration_by_municipality.csv | Drives housing DEMAND |
| **Population density** | land_area + population | Urban vs rural building patterns |
| **Income levels** | income_by_municipality.csv | Ability to afford renovations |
| **Existing housing stock** | housing_stock_by_municipality.csv | New construction vs renovation permits |

