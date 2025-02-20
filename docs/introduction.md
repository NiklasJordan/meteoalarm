# MeteoAlarm Python library

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14885078.svg)](https://doi.org/10.5281/zenodo.14885078) ![PyPI - Downloads](https://img.shields.io/pypi/dm/meteoalarm?label=PyPI%20Downloads&labelColor=blue&color=black&link=https%3A%2F%2Fpypi.org%2Fproject%2Fmeteoalarm%2F)

::::{grid}
:reverse:
:gutter: 3 4 4 4
:margin: 1 2 1 2

:::{grid-item}
:columns: 12 4 4 4

```{image} _static/logo-square.svg
:width: 200px
:class: sd-m-auto
:name: landing-page-logo
```

:::

:::{grid-item}
:columns: 12 8 8 8
:child-align: justify
:class: sd-fs-5

```{rubric} MyST - Markedly Structured Text - Parser
```

A Sphinx and Docutils extension to parse MyST,
a rich and extensible flavour of Markdown for authoring technical and scientific documentation.

````{div} sd-d-flex-row
```{button-ref} intro
:ref-type: doc
:color: primary
:class: sd-rounded-pill sd-mr-3

Get Started
```

```{button-ref} live-preview
:ref-type: doc
:color: secondary
:class: sd-rounded-pill

Live Demo
```
````

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
