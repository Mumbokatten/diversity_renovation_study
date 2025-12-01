# Bygglovskartan Scraper - Ready to Use!

## ✅ The scraper is now FULLY CONFIGURED and ready to run!

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper:**
   ```bash
   python bygglov_scraper.py
   ```

   By default, it will scrape the **Stockholm region** (last 30 months of permits).

3. **Wait for it to complete** - you'll see progress in the console

4. **Find your data** - A CSV file will be created: `bygglov_data_YYYYMMDD_HHMMSS.csv`

## What Data You'll Get

The CSV will have these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `permit_id` | Unique permit identifier | 141757 |
| `property_name` | Property name | "Skären 3" |
| `municipal_case_id` | Municipality's case ID | "K891308/25" |
| `publication_date` | Date permit was published | "2025-11-26" |
| `municipality` | Municipality name | "Stockholm" |
| `permit_type_num` | Permit type code | 0 |
| `permit_type` | Permit type description | "Bygglov" |
| `longitude` | Property longitude | 18.0719 |
| `latitude` | Property latitude | 59.3342 |

**Permit types:**
- 0 = Bygglov (Building permit)
- 1 = Rivningslov (Demolition permit)
- 2 = Marklov (Land permit)
- 3 = Förhandsbesked (Pre-decision)

## Customization Options

Edit the `main()` function in `bygglov_scraper.py`:

### Option 1: Scrape a Different Region

```python
permits = scraper.scrape_bounding_box(
    lat_min=57.6,    # Göteborg region
    lat_max=57.8,
    lon_min=11.8,
    lon_max=12.2,
    window=30,       # Last 30 months
    types=[0],       # Only building permits
    fetch_details=True
)
```

**Common regions (approximate coordinates):**

| City | lat_min | lat_max | lon_min | lon_max |
|------|---------|---------|---------|---------|
| Stockholm | 59.2 | 59.5 | 17.8 | 18.2 |
| Göteborg | 57.6 | 57.8 | 11.8 | 12.2 |
| Malmö | 55.5 | 55.7 | 12.9 | 13.1 |
| Uppsala | 59.8 | 60.0 | 17.5 | 17.8 |
| Linköping | 58.3 | 58.5 | 15.5 | 15.7 |

### Option 2: Scrape ALL of Sweden

⚠️ **WARNING:** This will take **many hours** and make thousands of requests!

Uncomment the example in `main()`:

```python
permits = scraper.scrape_sweden(
    window=30,
    types=[0],       # Only building permits (faster)
    grid_size=1.0,   # Degrees per grid cell
    fetch_details=True
)
```

**Time estimate:**
- With 1 req/second rate limiting
- ~50-100 grid cells × ~100-500 permits each
- Expect 5-10 hours for all of Sweden

### Option 3: Change Time Window

```python
window=12  # Last 12 months instead of 30
```

### Option 4: Adjust Rate Limiting

```python
scraper = BygglovScraper(rate_limit_seconds=0.5)  # Faster but less respectful
```

**Recommendation:** Keep it at 1.0 seconds to be respectful to Geoplan's servers.

## How It Works

The scraper uses Bygglovskartan's public API:

1. **Step 1:** Query `get_locations` to find all permit IDs in a geographic area
2. **Step 2:** For each permit ID, query `get_details/{id}` to get full information
3. **Step 3:** Extract relevant fields and save to CSV

**Rate limiting:** 1 second between requests (configurable)

## For Your Research (Study #3)

This data is perfect for your diversity/renovation study because:

✅ **Geographic coordinates** - Can map to neighborhoods
✅ **Permit dates** - Track renovation activity over time
✅ **Municipality names** - Filter by region
✅ **Property identifiers** - Link to other datasets

### Next Steps for Your Study:

1. **Scrape permit data** (this script)
2. **Get demographic data** from SCB mikrodata (apply at mikrodata@scb.se)
3. **Link datasets** by coordinates or municipality
4. **Calculate diversity measures** for each neighborhood
5. **Analyze correlation** between diversity and permit rates

### Linking to SCB Data

You can link this permit data to SCB demographics using:
- **Coordinates** (longitude/latitude) to assign permits to geographic areas
- **Municipality names** (though this is very coarse)
- **Property names** might partially match SCB property data

For more granular linking, you'll need to apply for SCB mikrodata access to get address-level demographic information.

## Troubleshooting

**"No permits found"**
- Check your bounding box coordinates (are they valid for Sweden?)
- Try a larger area
- Verify internet connection

**Script runs slowly**
- This is intentional! Rate limiting = 1 second per request
- Scraping 1000 permits = ~16 minutes
- Be patient and respectful to the servers

**CSV has duplicate permits**
- The script automatically removes duplicates
- You'll see a log message: "Removed X duplicate permits"

**Connection errors**
- The script will log errors and continue
- Failed permits are skipped
- Check the logs for specific error messages

## Legal & Ethical Notes

✅ **Legal:** Data is public (offentlighetsprincipen)
✅ **Ethical:** Academic research use
✅ **Respectful:** 1 second rate limiting
✅ **Attribution:** Cite Geoplan as data source in your paper

**Suggested citation:**
> Building permit data obtained from Bygglovskartan (Geoplan AB, geoplan.se), accessed [date].

## Contact

If Geoplan contacts you about the scraping:
- Explain it's for academic research
- Offer to cite them in your publication
- Offer to share your findings
- Ask if they prefer a different data access method

Good luck with your research! 🏘️📊
