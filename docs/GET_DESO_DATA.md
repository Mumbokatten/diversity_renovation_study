# How to Get DeSO Boundaries and Demographics

## Step 1: Download DeSO Boundaries

### Option A: Geodata Portal (Recommended)
1. Go to: **https://www.geodata.se/geodataportalen/**
2. Search for: "DeSO" or "Demografiska statistikområden"
3. Download format: **GeoPackage (.gpkg)** or **Shapefile (.shp)**
4. Save to: `diversity_renovation_study/data/deso_boundaries/`

### Option B: SCB Direct
1. Go to: **https://www.scb.se/hitta-statistik/regional-statistik-och-kartor/regionala-indelningar/deso---demografiska-statistikomraden/**
2. Look for download links on the page
3. Current version: DeSO 2025 (6,160 areas)

### Option C: Lantmäteriet API
- API endpoint for DeSO may be available
- Check: https://www.lantmateriet.se/sv/geodata/geodatatjanster/

## Step 2: Download Demographics (Country of Birth by DeSO)

### Via Statistikdatabasen (Free, No Login)

1. **Go to:** https://www.statistikdatabasen.scb.se/

2. **Navigate:**
   - Befolkning → Befolkningens sammansättning → Befolkningsstatistik
   - Look for tables with "DeSO" in region options

3. **Specific Table (Example):**
   - "Inrikes och utrikes födda efter region, ålder och kön"
   - URL: https://www.statistikdatabasen.scb.se/sq/130360

4. **Select:**
   - Region: "Alla DeSO" (All DeSO areas)
   - Variables: Inrikes födda (Swedish-born), Utrikes födda (Foreign-born)
   - Or more detailed: Country of birth
   - Year: Latest available (2024)

5. **Download:**
   - Format: Excel or CSV
   - Save to: `diversity_renovation_study/data/deso_demographics/`

### Alternative: More Detailed Country of Birth Data

**Table:** "Antal personer med utländsk eller svensk bakgrund (fin indelning) efter region"
- **URL:** https://www.statistikdatabasen.scb.se/goto/sv/ssd/UtlSvBakgFin
- Gives breakdown by region of origin (Nordic, EU, outside EU, etc.)

## Step 3: What You Should Have

After downloading:

```
diversity_renovation_study/
├── data/
│   ├── deso_boundaries/
│   │   └── deso_2025.gpkg (or .shp)
│   ├── deso_demographics/
│   │   └── deso_country_of_birth_2024.csv
│   └── bygglov_sweden_complete_20251201_194602.csv
```

## Step 4: Run the Linkage Script

Once you have the files, run:
```bash
python link_permits_to_deso.py
```

This will create a merged dataset with permits + demographics.

## 📋 Checklist

- [ ] Download DeSO boundaries (gpkg or shp)
- [ ] Download DeSO demographics (CSV with country of birth)
- [ ] Put files in correct folders
- [ ] Run linkage script
- [ ] Check output for any permits that didn't match

## 🆘 If You Get Stuck

**For boundary data:**
- Email: geodata@lantmateriet.se

**For statistics:**
- Email: uppdrag@scb.se
- Phone: 010-479 40 00

**Common Issues:**
- DeSO boundaries might be split by year (use DeSO 2025 for current data)
- Make sure CRS (coordinate system) is SWEREF99 TM (EPSG:3006)
