# MeteoAlarm Python Library

A Python library for accessing and filtering weather warnings from MeteoAlarm's CAP (Common Alerting Protocol) feeds. This library provides easy access to weather warnings across European countries through MeteoAlarm's official feeds.

## Features

- Access weather warnings for multiple European countries
- Filter warnings based on various attributes (severity, type, description, etc.)
- Support for multiple languages per warning
- Automatic parsing of CAP format warnings
- GeoJSON geometry support for warning areas
- Timezone-aware datetime handling

## Installation

Install the package using pip:

```bash
pip install meteoalarm
```

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

### Warning Attributes
Each warning object contains the following attributes:

- category: Warning category
- event: Event type
- urgency: Urgency level
- severity: Severity level
- certainty: Certainty level
- onset: Start time (datetime object)
- effective: Effective time (datetime object)
- expires: Expiration time (datetime object)
- sender: Dictionary containing sender information
- headline: Dictionary of headlines in available languages
- description: Dictionary of descriptions in available languages
- awareness_level: Awareness level
- awareness_type: Type of weather warning
- area: Dictionary containing area description and EMMA_ID
- geometry: GeoJSON geometry of the warning area

## Requirements
- Python 3.7+
- requests
- pytz
- pyyaml

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments
- Data provided by MeteoAlarm
- Based on the CAP (Common Alerting Protocol) standard