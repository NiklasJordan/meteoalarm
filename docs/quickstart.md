## Quickstart

```python
from meteoalarm import MeteoAlarm

# Initialize with one or more countries
warnings = MeteoAlarm(["estonia", "denmark"])

# Print all warnings
for warning in warnings:
    print(f"\nWarning for {warning.area["areaDesc"]} ({warning.country}):")
    print(f"Headline: {warning.get_headline("en-EN")}")
    print(f"Severity: {warning.severity}")
    print(f"Valid until: {warning.expires}")
```

### Filtering Warnings

The library provides flexible filtering capabilities:

```python
# Filter by severity
severe_warnings = warnings.filter(severity="Severe")

# Filter by description content (searches in all languages)
wind_warnings = warnings.filter(description="wind")

# Filter by multiple criteria
specific_warnings = warnings.filter(
    country="estonia",
    severity="Moderate",
    awareness_type="Wind"
)

# Chain filters
critical_wind = warnings.filter(awareness_type="Wind").filter(severity="Severe")
```

### Multilingual Support

Warnings are available in multiple languages:

```python
# Get available languages for a warning
languages = warning.get_available_languages()

# Get warning information in specific language
english_headline = warning.get_headline("en-EN")
estonian_desc = warning.get_description("et-ET")
```

### Plotting the Warning Area

```python
from shapely.geometry import shape
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import json

# Parse the GeoJSON string
geojson_dict = json.loads(warnings[0].geometry)

# Create geometry object
geometry = shape(geojson_dict)

# Create GeoDataFrame directly
gdf = gpd.GeoDataFrame(geometry=[geometry], crs="EPSG:4326")

# Convert to Web Mercator projection for contextily
gdf_web = gdf.to_crs(epsg=3857)

# Create plot
fig, ax = plt.subplots(figsize=(10, 10))
gdf_web.plot(ax=ax, alpha=0.5, color='red')

# Add background map
ctx.add_basemap(ax)

plt.axis('off')
plt.show()
```