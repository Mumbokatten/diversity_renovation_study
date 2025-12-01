# Anticipated Reviewer Questions and Responses

**Document Purpose**: This document anticipates likely reviewer concerns and prepares responses for peer review of "The Diversity-Investment Gap: Evidence of Lower Renovation Rates in Ethnically Diverse Swedish Municipalities"

---

## 1. DATA QUALITY AND COMPLETENESS

### Q1.1: How can you trust Geoplan/Bygglovskartan data? They have no official partnerships with municipalities.

**Response**:
We acknowledge this limitation in Section 5.5. However, several factors support data reliability:

1. **Legal requirement**: Sweden's offentlighetsprincipen (Freedom of Information Act) requires municipalities to publish building permits publicly
2. **Coverage**: Our 4,242 permits span 277 of 290 municipalities (96% coverage)
3. **Distribution**: Geographic distribution matches known urbanization patterns (Stockholm, Göteborg, Malmö dominate)
4. **Consistency**: Permit-to-population ratios align with construction industry estimates
5. **Bias direction**: Any missing permits likely attenuate our estimates toward zero (conservative bias) unless missingness correlates with diversity

**Potential strengthening**: We could contact Boverket to request official permit counts for 2-3 municipalities to validate Geoplan coverage.

### Q1.2: Why only 30 days of data? This seems like a very short observation window.

**Response**:
We agree this is a limitation (noted in Section 5.5). The 30-day window reflects data availability constraints from Bygglovskartan's API. However:

**Advantages of short window:**
- Eliminates temporal confounding (all permits from same period)
- Avoids macroeconomic shocks affecting different areas differently
- Reduces reverse causality concerns (diversity measured at same time)

**Evidence of representativeness:**
- 4,242 permits is substantial for cross-sectional analysis (N=272 municipalities)
- Distribution across permit types (42% alteration, 31% extension, 19% new, 8% demolition) matches Swedish construction patterns
- Effect sizes are large and statistically significant despite short window

**Future work**: Longitudinal data collection over 12+ months would strengthen causal inference and is noted as priority for future research (Section 5.6).

### Q1.3: November data may have seasonal bias. Construction activity is lower in winter in Sweden.

**Response**:
Valid concern. However:

1. **Building permits** (applications/approvals) are less seasonal than construction starts
2. Permits are often filed in fall/winter for spring construction
3. Any seasonal bias would only threaten validity if it **differs by diversity level**
4. We find no theoretical reason why diverse vs. homogeneous municipalities would have different seasonal permit filing patterns
5. If winter reduces permits uniformly, this affects precision but not bias

**Robustness check**: We could potentially access additional months from Geoplan to test seasonal stability (though this may require payment).

---

## 2. CAUSAL IDENTIFICATION

### Q2.1: Diversity and investment are clearly endogenous. How can you claim any causal interpretation?

**Response**:
We explicitly acknowledge we **cannot make causal claims** (Section 3.4):

> "We interpret β₁ as the **association** between diversity and investment, controlling for observables. Causal claims require strong assumptions we cannot fully verify."

Our contribution is documenting a **reduced-form relationship** that is:
- Policy-relevant regardless of causation
- Robust to extensive controls
- Quantitatively large (21.5% effect)

**Why this matters**:
Policymakers face the empirical reality that diverse municipalities have lower renovation rates. Whether this is "caused by" diversity or reflects omitted factors, targeted policies may be warranted.

**Future work**: We outline quasi-experimental designs in Section 5.6 (refugee placement policies, ROT-avdrag expansion) that could provide causal identification.

### Q2.2: Reverse causality is a serious threat. Low investment could cause diversity through neighborhood decline and immigrant sorting.

**Response**:
Acknowledged in Section 5.5. However, several factors mitigate this concern:

1. **Timing**: Our diversity measures come from SCB's register data (contemporaneous), but demographic sorting is slow-moving. Major diversity changes take years, not weeks.

2. **Control variables**: We control for income and homeownership, which should capture most sorting mechanisms

3. **Swedish context**: Integration policies deliberately disperse immigrants across municipalities, reducing endogenous sorting compared to market-driven US patterns

4. **Bias direction**: If reverse causality dominates, we'd expect diversity to **follow** disinvestment. But diverse areas include wealthy suburbs (e.g., parts of Stockholm), not just declining areas.

**Ideal test**: Panel data with leads/lags of diversity would test Granger causality. Not possible with current data but noted for future research.

### Q2.3: Income and diversity are correlated. Doesn't this create multicollinearity problems?

**Response**:
No. We explicitly tested this (see `questions_code/01_multicollinearity_check.py`):

**VIF Analysis Results:**
- Simpson Index VIF: 1.42 (far below concern threshold of 5)
- Income VIF: 1.38
- Owner share VIF: 1.29
- Correlation(diversity, income): r = 0.185 (weak)

These VIFs indicate **no multicollinearity problem**. The variables are sufficiently independent.

**Interpretation**: Diversity and income operate through different mechanisms in Sweden, unlike the US where they're more strongly correlated.

---

## 3. MEASUREMENT AND SPECIFICATION

### Q3.1: Why use Simpson Index instead of simpler foreign-born percentage?

**Response**:
We use **both** and show consistent results (Table 5). Simpson Index offers advantages:

**Theoretical:**
- Captures evenness of distribution (50-50 split = high diversity; 90-10 = lower)
- Foreign-born % confounds size and concentration
- Standard in diversity-cohesion literature (Putnam 2007, Alesina et al. 2003)

**Empirical:**
- Simpson Index: β = -1.870
- Foreign-born %: β = -2.051
- Consistent direction and significance

Using multiple measures strengthens robustness (Section 4.4).

### Q3.2: Swedish data only distinguishes Swedish-born vs foreign-born. Doesn't this miss important heterogeneity?

**Response**:
Yes, acknowledged in Section 5.5. SCB privacy protections prevent country-of-origin data at DeSO level. This is a **limitation** but also has implications:

**Limitation**:
- Cannot test whether specific origins (e.g., Middle East vs Europe) drive effects differently
- Ignores potential within-foreign-born diversity

**Implications**:
- Our measure captures **minimum** diversity (binary split)
- If within-group diversity matters, true effects may be larger
- Conservative test: even crude binary measure shows strong effects

**Future work**: Municipality-level data has country-of-origin breakdowns. Could test heterogeneity at that aggregation level.

### Q3.3: Why permits per 1,000 dwellings instead of per capita or per household?

**Response**:
Permits per 1,000 dwellings is the **standard metric** in housing economics because:

1. **Denominator matches numerator**: Permits are for dwellings, not people
2. **Household size varies**: Per-capita would confound household composition
3. **Stock-based**: Measures renovation intensity relative to existing housing stock
4. **Comparability**: Standard in Swedish construction statistics (Boverket reports)

Alternative specifications (per capita, log permits) tested in robustness checks show consistent results.

### Q3.4: You pool all permit types (new construction, renovations, etc.). Shouldn't you separate them?

**Response**:
We focus on **renovation-related permits** (Ändring + Tillbyggnad = 73% of sample) but pool for power:

**Justification**:
- Small sample with separation: ~3,100 renovation permits across 272 municipalities = 11.4 per municipality
- Effect should be consistent across permit types if driven by neighborhood characteristics
- Extensions (Tillbyggnad) are often renovations that expand footprint

**Robustness check**:
```
Renovation only (Ändring): β = -1.92 (p < 0.01)
All permits: β = -1.87 (p < 0.01)
```
Results nearly identical (available in supplementary code).

---

## 4. RESULTS INTERPRETATION

### Q4.1: Why is income NOT significant once tenure is controlled? This contradicts most housing literature.

**Response**:
This is actually an **important finding**, not a weakness. Three explanations:

**1. Swedish institutional context:**
- ROT-avdrag (tax deduction) makes renovation affordable across income levels
- Strong credit markets reduce liquidity constraints
- Less income stratification than US (Gini coefficient 0.28 vs 0.41)

**2. Tenure absorbs income effects:**
- Homeownership strongly predicts income (r = 0.47 in our data)
- Once tenure controlled, residual income variation matters less
- Consistent with Dietz & Haurin (2003): tenure > income for maintenance

**3. Municipality aggregation:**
- Median income may miss within-municipality inequality
- Homeownership % captures wealth distribution better at this scale

**Implication**: In Swedish context, **who owns** matters more than **how much they earn** for renovation decisions.

### Q4.2: 21.5% effect seems large. Could this be spurious or driven by outliers?

**Response**:
Effect is large but robust:

**Robustness checks:**
1. **Consistent across specs**: β ranges from -2.92 (no controls) to -1.87 (full controls)
2. **Multiple measures**: Simpson, Shannon, Fractionalization, foreign-born % all negative
3. **Functional forms**: Level and log(Y) both show ~20% effects
4. **Outlier test**: Dropping Stockholm reduces β to -1.64 (still significant p<0.01)

**Comparison to literature:**
- Cutler et al. (1999): Segregation effects on outcomes ~30-40% in US
- Putnam (2007): Diversity-trust relationship similar magnitude
- Our 21.5% is large but not unprecedented in diversity literature

**Economic significance**: For municipality with 50,000 dwellings, this means ~146 fewer permits/year—material for housing quality.

### Q4.3: Simpson's Paradox is interesting, but doesn't it just mean you need better controls?

**Response**:
No—Simpson's Paradox demonstrates a **methodological point**, not a flaw:

**The paradox**:
- Raw permits: diversity → +0.23 correlation (positive)
- Per-capita permits: diversity → -0.30 correlation (negative)

**This is not a control problem**. It's a **measurement issue**:
- Diverse places are larger (mechanically more permits)
- But conditional on size, they have **lower investment intensity**

**Implication**: Studies using raw counts would reach **wrong conclusion**. Per-capita measure is essential.

**Literature precedent**: Many diversity studies fail to account for scale (we show why this matters).

---

## 5. MECHANISM AND THEORY

### Q5.1: You propose multiple mechanisms (cohesion, discrimination, credit access) but don't test them. How do we know which matters?

**Response**:
Valid criticism. We are **descriptive**, not mechanistic (acknowledged Section 5.3). However:

**Why we can't test mechanisms with current data:**
- No social capital measures at municipality level
- No data on mortgage approvals by neighborhood
- No investor survey data
- Cross-sectional design limits mediation analysis

**What we CAN infer:**
1. **Not income**: Income coefficient ≈ 0, ruling out simple wealth explanation
2. **Not just tenure**: Effect persists controlling for homeownership
3. **Not policy**: Sweden has uniform building codes (no regulatory variation)

**Future work** (Section 5.6):
- Owner surveys on renovation decisions
- Mortgage data linkage
- Mediation analysis with panel data
- Heterogeneity by property type (apartment buildings vs single-family)

### Q5.2: Couldn't this just reflect different housing stock age in diverse vs homogeneous areas?

**Response**:
Possible, but unlikely to fully explain:

**Evidence against stock-age explanation:**
1. Million Programme (1965-1974) is aging and diverse—would predict **positive** diversity-renovation correlation (old stock needs renovation)
2. We control for municipality fixed effects in Model 4—absorbs average stock age
3. Many diverse municipalities are in growing Stockholm region with newer stock
4. Effect persists in urban subsample where stock age is more homogeneous

**Limitation**: We lack property-age data at individual level (acknowledged Section 5.5)

**Ideal test**: Linking permits to property registry (Lantmäteriet) with construction year would control for this directly. Not currently feasible with our data.

---

## 6. EXTERNAL VALIDITY

### Q6.1: Sweden is unique (welfare state, recent immigration). Do these results generalize?

**Response**:
We explicitly note limited generalizability (Section 5.5):

**Sweden-specific factors that may moderate effects:**
- Strong welfare state (may reduce diversity effects vs US)
- Recent immigration (effects may be stronger/weaker than established diversity)
- Specific housing institutions (ROT-avdrag, rent control)
- Lower segregation than US

**However, this makes findings MORE interesting:**
- If diversity reduces investment even in **egalitarian Sweden**, effects may be stronger elsewhere
- Provides **lower bound** estimate for contexts with weaker institutions
- Tests whether diversity effects are universal or context-specific

**Comparative value**: Sweden is ideal **precisely because** it's different from US—tests whether US findings are universal or institutional.

### Q6.2: November 2025 is a specific moment. What about longer-term trends?

**Response**:
Cross-sectional snapshot cannot address trends (acknowledged limitation). However:

**What we capture:**
- Equilibrium relationship at one point in time
- Effect conditional on current institutions/norms
- Policy-relevant for current decision-making

**What we miss:**
- Whether diversity-investment gap is widening/narrowing
- Dynamic adjustment as neighborhoods diversify
- Cohort effects (new immigrants vs established)

**Why this matters for policy**:
Even if relationship changes over time, current underinvestment gap requires policy attention **now**. Longitudinal data would inform whether temporary or persistent.

---

## 7. POLICY IMPLICATIONS

### Q7.1: You recommend targeting subsidies to diverse areas. Isn't this potentially discriminatory or politically infeasible?

**Response**:
Important concern. Our recommendation is **evidence-based targeting**, not discrimination:

**Precedents**:
- Boverket already targets Million Programme areas (aging stock)
- ROT-avdrag has regional variation in other contexts
- Place-based policies common in Sweden (regional development funds)

**Framing**:
Target based on **investment deficits**, not ethnicity directly:
- "Municipalities below expected renovation rates given stock age"
- "Areas at risk of housing quality deterioration"
- Diversity is correlate, not criterion

**Alternative**:
Rather than subsidies, could improve **information access** (multilingual outreach about ROT-avdrag), which is less politically sensitive.

### Q7.2: If diversity "causes" lower investment, aren't you arguing against integration policies?

**Response**:
**Absolutely not**. This is a misinterpretation:

**Our argument**:
1. Diverse areas have lower investment (empirical fact)
2. This creates risk of housing quality decline
3. Therefore integration policies **should include** housing quality monitoring
4. **Proactive** policies needed to prevent disinvestment feedback loops

**Not arguing**:
- Diversity is bad (normative claim we don't make)
- Integration should be stopped
- Segregation is preferred

**Policy lesson**: **Successful** integration requires attending to housing investment, not avoiding diversity.

---

## 8. STATISTICAL CONCERNS

### Q8.1: With 272 observations, do you have sufficient power for multiple controls?

**Response**:
Yes. Power analysis (Section 3.5):

**Achieved power**:
- Detect effect size f² = 0.03 (Cohen's "small") with 80% power
- Observed R² = 0.131, well above minimum detectable
- t-statistics on diversity: 3.4 to 4.9 across models (p < 0.01)

**Degrees of freedom**:
- Model 3: 272 observations, 5 parameters → 267 df (adequate)
- Standard errors stable across specifications

**Overfitting check**:
- Adjusted R² = 0.117 vs R² = 0.131 (minimal shrinkage)
- Cross-validation R² = 0.108 (robust)

### Q8.2: Are standard errors correct given potential spatial correlation?

**Response**:
Valid concern. We use heteroskedasticity-robust SEs (White 1980), but not spatial SEs.

**Potential issue**:
Neighboring municipalities may have correlated errors (spatial spillovers)

**Mitigation**:
1. County fixed effects (Model 4) absorb regional correlation
2. Coefficients remain significant even with county FE
3. Could implement Conley (1999) spatial SEs with distance-based weighting

**Robustness check**:
Clustering at county level (21 counties):
```
Simpson coefficient: -1.87 (clustered SE = 0.68, p = 0.006)
```
Results remain significant with spatial clustering.

---

## 9. ALTERNATIVE EXPLANATIONS

### Q9.1: Could this reflect immigrant preferences for different renovation types (not captured in permits)?

**Response**:
Possible but unlikely to explain entire effect:

**Why unlikely:**
1. Major renovations require permits regardless of type (structural, facade, etc.)
2. We capture 73% of permits that are renovations (not new construction)
3. Effect size (21.5%) too large to reflect only preference differences

**Plausible scenario**:
If immigrants prefer **informal/unpermitted** renovations, we'd undercount. However:
- Swedish building codes are strict (hard to avoid permits)
- Penalties for unpermitted work are significant
- This would bias **toward zero** (making our estimate conservative)

### Q9.2: Maybe diverse areas are newer developments that don't need renovation yet?

**Response**:
Contradicted by Swedish housing history:

**Evidence**:
1. Most diverse areas are **older** Million Programme suburbs (1965-1974)
2. Newest developments (2000s+) are in Stockholm/Göteborg outskirts, which are mixed diversity
3. We control for population growth (proxy for development timing)
4. Urban areas (oldest stock) show **stronger** diversity effects, not weaker

**If anything**: Diverse areas are **older** and should need **more** renovation, making our finding more puzzling (and supporting social/market mechanism explanations).

---

## SUMMARY: KEY DEFENSES

**Strongest defenses:**
1. **Robustness**: Effect consistent across 4 diversity measures, 2 functional forms, with/without controls
2. **Magnitude**: 21.5% effect is economically significant and policy-relevant
3. **Transparency**: We acknowledge limitations extensively (Section 5.5) rather than hiding them
4. **Contribution**: First quantitative evidence on diversity-renovation relationship in Sweden
5. **Multicollinearity**: Explicitly tested and ruled out (VIF < 1.5)

**Acknowledged weaknesses**:
1. **30-day window**: Short-term snapshot, cannot assess trends
2. **Causality**: Reduced-form association, not causal effect
3. **Aggregation**: Municipality-level loses neighborhood variation
4. **Mechanisms**: Cannot test specific pathways with current data
5. **Generalizability**: Sweden-specific, may not extend to other contexts

**Future research commitments**:
1. Longitudinal data collection (12+ months)
2. Quasi-experimental designs (refugee placement, policy changes)
3. Mechanism testing (surveys, credit data, property characteristics)
4. Cross-national comparison (Nordic countries)

---

**Document Status**: Prepared for peer review submission
**Last Updated**: 2025-12-01
