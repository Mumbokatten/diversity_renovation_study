# Quick Download Guide - DeSO Data

I've prepared everything, but Swedish government data requires manual download (for now). Here are the EXACT steps:

## ✅ Folders Created

- `data/deso_boundaries/` ← DeSO shapefiles go here
- `data/deso_demographics/` ← Demographics CSV goes here

## 🗺️ Part 1: DeSO Boundaries (5 minutes)

### Option A: Geodata Portal (Recommended)

**Step by step:**

1. Go to: **https://geodata.se/**
2. Click "Sök data" (Search data)
3. Type: **"DeSO 2025"**
4. Look for: "Demografiska statistikområden (DeSO) 2025" from SCB
5. Download format: **GeoPackage (.gpkg)** or **Shapefile (.zip)**
6. Save to: `C:/Users/Hampu/diversity_renovation_study/data/deso_boundaries/`
7. If ZIP, extract files to that folder

**File you should get:** `deso_2025.gpkg` or `deso_2025.shp` (+ associated files)

### Option B: Direct from Lantmäteriet

1. Go to: **https://www.lantmateriet.se/geodataportal**
2. Search: "DeSO"
3. Download and save to same folder

### Option C: WFS Service (Advanced)

If you're comfortable with GIS:
- WFS URL: `https://geodata.scb.se/geoserver/stat/wfs`
- Layer: `stat:deso_2025`
- Use QGIS or Python to fetch

## 📊 Part 2: Demographics (5 minutes)

### Method: Statistikdatabasen

**Step by step:**

1. Go to: **https://www.statistikdatabasen.scb.se/**

2. Navigate:
   - START
   - Befolkning (BE)
   - Befolkningens sammansättning (BE0101)
   - Befolkningsstatistik (BE0101E)

3. Find table: **"Inrikes och utrikes födda efter region, ålder och kön"**
   - Direct link: https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__BE__BE0101__BE0101E/InrUtrFoddaRegAlKon/

4. **Select variables:**
   - Region: Välj "DeSO" → Click "Välj alla" (Select all)
   - Ålder: "totalt ålder" (total age)
   - Kön: "totalt" (total)
   - Födelseregion: "Inrikes födda", "Utrikes födda" (Swedish-born, Foreign-born)
   - År: 2024 (latest year)

5. Click **"Fortsätt"** (Continue)

6. **Download:**
   - Click "Ladda ner" or export icon
   - Format: **CSV with comma separator**
   - Save as: `deso_country_of_birth_2024.csv`
   - Save to: `C:/Users/Hampu/diversity_renovation_study/data/deso_demographics/`

## 🏃 Once Downloaded

Run this to verify files:

```bash
cd C:/Users/Hampu/diversity_renovation_study
ls -lh data/deso_boundaries/
ls -lh data/deso_demographics/
```

You should see:
- `data/deso_boundaries/deso_2025.gpkg` (or .shp files)
- `data/deso_demographics/deso_country_of_birth_2024.csv`

## ▶️ Then Run the Linkage

```bash
python link_permits_to_deso.py
```

## 🆘 Troubleshooting

**Can't find DeSO in geodata portal:**
- Try searching "demografiska statistikområden"
- Or email: geodata@lantmateriet.se

**Demographics table doesn't show DeSO option:**
- Make sure you're looking at 2024+ data (DeSO 2025 is new)
- Try different table: "Antal personer med utländsk eller svensk bakgrund"

**Files downloaded but wrong format:**
- GeoPackage (.gpkg) is best for boundaries
- CSV is correct for demographics
- If you got Shapefile (.shp), that works too - just make sure all associated files (.shx, .dbf, .prj) are in the same folder

---

**Total time: ~10-15 minutes** ⏱️

Once you have both files, you're ready to run the analysis! 🚀
