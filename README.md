# The Diversity-Investment Gap

**Full Title:** The Diversity-Investment Gap: Evidence of Lower Renovation Rates in Ethnically Diverse Swedish Municipalities

**Research Question:** Does neighborhood ethnic diversity predict different rates of property renovation investment?

## Study Overview

This research project investigates the relationship between neighborhood demographic composition (specifically ethnic diversity measured by country of birth) and housing renovation activity in Sweden.

### Hypothesis Mechanisms

Several potential mechanisms could explain observed patterns:
- **Social cohesion effects** - Diversity may affect informal monitoring and maintenance norms
- **Information networks** - Different populations may have varying access to contractor networks
- **Preference heterogeneity** - Diverse neighborhoods may have different aesthetic/functional priorities
- **Institutional barriers** - Immigrant homeowners may face different information or financing constraints
- **Selection effects** - Property characteristics may attract/retain different populations

## Data Sources

### 1. Building Permit Data (This Repository)
- **Source:** Bygglovskartan (Geoplan AB)
- **Collection method:** Web scraping via public API
- **Coverage:** All of Sweden, last 30 months
- **Fields:** Permit ID, property name, date, municipality, coordinates, permit type
- **Tool:** `bygglov_scraper.py`

### 2. Demographic Data (To Be Obtained)
- **Source:** SCB (Statistics Sweden) mikrodata
- **Required registers:** Fastighetsregistret, befolkningsregister
- **Fields needed:** Country of birth by address/property
- **Access:** Apply via mikrodata@scb.se
- **Timeline:** 3-6 months processing time

## Methodology

### Data Collection
1. ✅ Scrape building permit records with geographic coordinates
2. ⏳ Apply for SCB mikrodata access
3. ⏳ Link permit data to demographic data by coordinates/property ID

### Analysis Plan
1. **Define neighborhoods** - 100m radius, street segment, or DeSO areas
2. **Calculate diversity measures** - Simpson index, fractionalization by region of birth
3. **Count renovation permits** - Per neighborhood, per time period
4. **Control variables** - Property age, size, income, education, property values
5. **Statistical model** - Panel regression with neighborhood and time fixed effects

### Pre-registration
- Plan to pre-register on OSF before analysis
- Specify hypotheses and robustness checks upfront

## Repository Structure

```
diversity_renovation_study/
├── README.md                    # This file - project overview
├── README_SCRAPER.md           # Technical documentation for scraper
├── bygglov_scraper.py          # Main scraper script
├── requirements.txt            # Python dependencies
├── data/                       # (created when you run scraper)
│   └── bygglov_data_*.csv     # Raw permit data
└── analysis/                   # (create this for your analysis scripts)
    └── (your R/Python analysis scripts)
```

## Getting Started

### Step 1: Collect Permit Data

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper (see README_SCRAPER.md for options)
python bygglov_scraper.py
```

### Step 2: Apply for SCB Data

Draft application to mikrodata@scb.se including:
- Research question and methodology
- Specific registers needed (Fastighetsregister, befolkningsregister)
- Variables required (country of birth, property ID, coordinates)
- Ethics approval from your institution
- Data security plan

### Step 3: Data Linkage

Once you have both datasets:
- Match permits to neighborhoods using coordinates
- Aggregate demographic data to neighborhood level
- Calculate diversity indices
- Prepare analysis dataset

## Ethical Considerations

### Framing
- Emphasize understanding barriers and mechanisms
- Avoid stigmatizing narratives
- Focus on policy implications for integration support
- Consider publishing in Swedish for nuanced local discussion

### Data Privacy
- Use pseudonymized data only
- Follow GDPR requirements
- Aggregate to neighborhood level (no individual identification)
- Secure data storage

### Robustness
- Test multiple diversity measures
- Check for selection bias
- Use instrumental variables if possible
- Transparent reporting of all specifications

## Timeline

- ✅ **Week 1:** Data collection tool development
- ⏳ **Week 2-4:** Scrape permit data for target regions
- ⏳ **Month 2:** Submit SCB mikrodata application
- ⏳ **Month 3-8:** Wait for SCB approval and data delivery
- ⏳ **Month 9:** Data linkage and cleaning
- ⏳ **Month 10:** Pre-registration and analysis
- ⏳ **Month 11-12:** Write-up and submission

## Citation

If you use this scraper or methodology, please cite:

> Building permit data obtained from Bygglovskartan (Geoplan AB, https://geoplan.se/bygglovskartan), accessed December 2025.

## Contact

For questions about the methodology or collaboration opportunities, contact [your contact info].

## License

Research tools in this repository are for academic use only. Building permit data is public under Swedish offentlighetsprincipen but should be used responsibly.

---

**Status:** Data collection phase
**Last updated:** December 1, 2025
