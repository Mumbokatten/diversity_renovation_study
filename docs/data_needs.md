# Data Needs for Diversity & Renovation Study

## ✅ Data We Have

### Building Permits (4,242 records)
- **Source:** Bygglovskartan scraping
- **Fields:** permit_id, property_name, municipality, date, coordinates
- **Coverage:** All Sweden, last 30 months
- **File:** `bygglov_sweden_complete_20251201_194602.csv`

## ❌ Data Still Needed

### 1. Demographic Data (CRITICAL)

**Need: Neighborhood ethnic diversity measures**

Options for obtaining:
- **A) SCB Mikrodata** (Best but slowest)
  - Apply at: mikrodata@scb.se
  - Registers needed: Befolkningsregister (RTB)
  - Variables: Country of birth by coordinate/DeSO area
  - Timeline: 3-6 months
  - Cost: €€€

- **B) SCB Open Statistics by DeSO**
  - Source: statistikdatabasen.scb.se
  - Free, immediate
  - Granularity: DeSO areas (~1000-2000 people each)
  - May be sufficient for initial analysis

### 2. Geographic Data

**Need: Spatial boundaries to define "neighborhoods"**

Options:
- **DeSO Boundaries** (Recommended)
  - Download from: scb.se/hitta-statistik/regional-statistik-och-kartor/regionala-indelningar/deso
  - Format: Shapefile/GeoJSON
  - Use PostGIS or Python (geopandas) to link permits to DeSO areas

- **Custom Buffers**
  - Create 100m or 500m radius around each permit
  - Aggregate demographics within buffer
  - More work but very precise

### 3. Control Variables

**Need: Economic/housing characteristics by neighborhood**

From SCB (DeSO level, free):
- Median household income
- Education levels (% with university degree)
- Age distribution
- Property values (via Lantmäteriet or tax data)

### 4. Property Characteristics

**Need: Building age, size, type**

Options:
- **Lantmäteriet Building Register**
  - Source: lantmateriet.se (Fastighetsinformation)
  - Cost: Paid product
  - Can link via property name or coordinates

- **SCB Fastighetsregister**
  - Request with mikrodata application
  - Has building characteristics

## 📋 Next Steps (Prioritized)

### Immediate (This Week)
1. ✅ Download DeSO boundaries from SCB
2. ✅ Download DeSO-level demographics (country of birth) from statistikdatabasen
3. ✅ Test linkage: assign each permit to a DeSO area

### Short-term (This Month)
4. ⏳ Run pilot analysis with DeSO-level data
5. ⏳ Assess if DeSO granularity is sufficient
6. ⏳ If not, apply for SCB mikrodata

### Long-term (Next 3-6 Months)
7. ⏳ Wait for mikrodata approval
8. ⏳ Link individual-level data to permits
9. ⏳ Run full analysis with fine-grained neighborhoods

## 🔧 Technical Tools Needed

### Python Libraries
```
pip install geopandas pandas shapely pyproj
```

### GIS Software (Optional)
- QGIS (free) for visualization and checking linkages

## 📊 Expected Data Structure After Linkage

```csv
permit_id,property_name,municipality,date,longitude,latitude,deso_code,diversity_index,foreign_born_pct,median_income,edu_university_pct
137691,Stenyxan 7,Falkenberg,2025-11-03,12.48,56.90,1382C0010,0.45,0.23,320000,0.35
```

## 📝 Notes

- Start with DeSO-level data for quick proof-of-concept
- DeSO areas average ~1000 people, may be sufficient granularity
- Can always refine with mikrodata later
- Ethics approval needed before applying for mikrodata
