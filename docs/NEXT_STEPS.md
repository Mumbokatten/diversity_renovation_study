# Next Steps - DeSO Data Integration

## ✅ What You Have Now

1. **Building Permits:** 4,242 permits across Sweden with coordinates
2. **Scraping Tools:** Fully functional for future updates
3. **Linkage Script:** Ready to merge permits with DeSO demographics
4. **Documentation:** Complete research framework

## 📋 Action Items (Do These This Week)

### Step 1: Install GIS Libraries

```bash
cd C:/Users/Hampu/diversity_renovation_study
pip install -r requirements.txt
```

This installs `geopandas` and other libraries needed for spatial analysis.

### Step 2: Download DeSO Boundaries

**Go to:** https://www.geodata.se/geodataportalen/

1. Search for "DeSO 2025"
2. Download as GeoPackage (.gpkg) or Shapefile (.shp)
3. Save to: `data/deso_boundaries/`

**OR try direct SCB link:**
- https://www.scb.se/hitta-statistik/regional-statistik-och-kartor/regionala-indelningar/deso---demografiska-statistikomraden/

### Step 3: Download Demographics

**Go to:** https://www.statistikdatabasen.scb.se/

**Navigate to:**
- Befolkning → Befolkningens sammansättning → Befolkningsstatistik

**Find table with:**
- Region: DeSO
- Variables: Inrikes födda / Utrikes födda (Swedish-born / Foreign-born)
- Or more detailed country of birth

**Download:**
- Format: CSV or Excel
- Year: 2024 (latest)
- Save to: `data/deso_demographics/`

**Suggested tables:**
1. "Inrikes och utrikes födda efter region" (Basic)
2. "Antal personer med utländsk eller svensk bakgrund (fin indelning)" (Detailed)

### Step 4: Create Folder Structure

```bash
cd C:/Users/Hampu/diversity_renovation_study
mkdir -p data/deso_boundaries
mkdir -p data/deso_demographics
```

### Step 5: Run the Linkage Script

Once you have the DeSO files:

```bash
python link_permits_to_deso.py
```

**Expected output:**
- `permits_with_demographics.csv` - Your analysis-ready dataset!

### Step 6: Check the Output

The final CSV should have:
- All permit columns (id, date, location, etc.)
- DeSO code
- Population statistics (Swedish-born, foreign-born)
- Calculated diversity index

## 🔍 What to Do If...

**"I can't find DeSO boundaries"**
- Email: geodata@lantmateriet.se
- Or use this direct link (if available): [check SCB DeSO page]

**"Column names don't match in the script"**
- Open the script: `link_permits_to_deso.py`
- Look for lines marked with `# ADJUST THIS`
- Change column names to match your actual data

**"Spatial join fails"**
- Make sure both files use same coordinate system (SWEREF99 TM, EPSG:3006)
- Script handles conversion automatically, but check if errors occur

**"Many permits don't match a DeSO"**
- Some permits might be outside DeSO boundaries (e.g., very rural areas)
- Check if coordinates are correct (should be in Sweden!)

## 📊 After Linkage - Analysis Ideas

Once you have `permits_with_demographics.csv`:

1. **Descriptive Statistics**
   - How many permits in high vs low diversity areas?
   - Are diverse areas more urban or rural?

2. **Regression Analysis**
   ```
   permit_rate ~ diversity_index + income + education + property_age
   ```

3. **Spatial Analysis**
   - Cluster analysis: Do renovations cluster in certain areas?
   - Hot spot analysis

4. **Time Series**
   - Are diverse areas renovating more/less over time?

## 🎓 Research Timeline

- **This Week:** Get DeSO data, run linkage
- **Next Week:** Exploratory analysis, summary statistics
- **Week 3-4:** Calculate diversity indices, test correlations
- **Month 2:** Draft methods section, create visualizations
- **Month 3:** Write full paper, submit for review

## 📚 Useful Resources

**SCB Help:**
- General: uppdrag@scb.se
- Phone: 010-479 40 00

**DeSO Documentation:**
- https://www.scb.se/hitta-statistik/regional-statistik-och-kartor/regionala-indelningar/deso---demografiska-statistikomraden/

**Python GIS Tutorial:**
- https://geopandas.org/en/stable/docs/user_guide/mapping.html

**Diversity Indices:**
- Simpson Index: 1 - Σ(p_i²)
- Shannon Index: -Σ(p_i × ln(p_i))
- Fractionalization: 1 - Σ(p_i²)

## ✅ Final Checklist

- [ ] Installed GIS libraries (`pip install -r requirements.txt`)
- [ ] Downloaded DeSO boundaries → `data/deso_boundaries/`
- [ ] Downloaded demographics → `data/deso_demographics/`
- [ ] Created folder structure
- [ ] Ran `link_permits_to_deso.py`
- [ ] Checked output file `permits_with_demographics.csv`
- [ ] Verified data looks correct (spot check a few rows)

**Once all checked → You're ready to start analysis! 🎉**
