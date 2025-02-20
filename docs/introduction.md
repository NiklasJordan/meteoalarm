# MeteoAlarm Python library

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14885078.svg)](https://doi.org/10.5281/zenodo.14885078) ![PyPI - Downloads](https://img.shields.io/pypi/dm/meteoalarm?label=PyPI%20Downloads&labelColor=blue&color=black&link=https%3A%2F%2Fpypi.org%2Fproject%2Fmeteoalarm%2F)

A Python library for accessing and filtering weather warnings from MeteoAlarm's CAP (Common Alerting Protocol) feeds. This library provides easy access to weather warnings across European countries through MeteoAlarm's official feeds.

```{note}
MeteoAlarm Python libraries interface are not guaranteed stable and may change until version 1.0 when backwards compatibility will be a main focus.
```

## Features

- Access weather warnings for multiple European countries
- Filter warnings based on various attributes (severity, type, description, etc.)
- Support for multiple languages per warning
- Automatic parsing of CAP format warnings
- GeoJSON geometry support for warning areas
- Timezone-aware datetime handling

## License
This project is licensed under the MIT License - see the LICENSE file for details.
