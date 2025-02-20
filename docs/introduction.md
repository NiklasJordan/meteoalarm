---
sd_hide_title: true
---

# MeteoAlarm Python library

::::{grid}
:reverse:
:gutter: 3 4 4 4
:margin: 1 2 1 2

:::{grid-item}
:columns: 12 4 4 4

```{image} meteoalarm-lib.png
:width: 200px
:class: sd-m-auto
:name: landing-page-logo
```

:::

:::{grid-item}
:columns: 12 8 8 8
:child-align: justify
:class: sd-fs-5

```{rubric} MeteoAlarm Python library
```

A Python library for accessing and filtering weather warnings from MeteoAlarm's CAP (Common Alerting Protocol) feeds. This library provides easy access to weather warnings across European countries through MeteoAlarm's official feeds.

:::

::::

```{note}
MeteoAlarm Python libraries interface are not guaranteed stable and may change until version 1.0 when backwards compatibility will be a main focus.
```

---

```{rubric} Features
```

- Access weather warnings for multiple European countries
- Filter warnings based on various attributes (severity, type, description, etc.)
- Support for multiple languages per warning
- Automatic parsing of CAP format warnings
- GeoJSON geometry support for warning areas
- Timezone-aware datetime handling

---

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`markdown;1.5em;sd-mr-1` Installation
:link-type: ref

Learn how to install the library via PyPI or from source.

+++
[Learn more »](installation)
:::

:::{grid-item-card} {octicon}`plug;1.5em;sd-mr-1` Quickstart
:link-type: ref

Learn the basic components and how to query for desired warnings.

+++
[Learn more »](quickstart)
:::

:::{grid-item-card} {octicon}`tools;1.5em;sd-mr-1` MeteoAlarm's Warnings
:link-type: ref

Learn what MeteoAlarm warnings are, which information they contain and how to interpret them.

+++
[Learn more »](warnings)
:::

::::

---

```{rubric} License
```
This project is licensed under the MIT License - see the [LICENSE](https://github.com/NiklasJordan/meteoalarm/blob/main/LICENSE) file for details.

```{toctree}
:hidden:
```
