# Warnings

The warnings are provided through [MeteoAlarm](https://meteoalarm.org).

MeteoAlarm is an Early Warning Dissemination System developed for [EUMETNET](https://www.eumetnet.eu/), the European Network of National Meteorological Services. It aggregates and provides awareness information from 38 European National Meteorological and Hydrological Services, using a standardized color-coded system (yellow, orange, red) for consistent interpretation across Europe. The system disseminates warnings via MeteoAlarm Feeds to both national and international redistributors, enabling timely action.

## Alert object

Each `Alert()` object, describes the weather warning in several details, eg awareness level, hazard type, period, instructions, contacts, etc. A detailed and technical overview about the warnings, can be found in [MeteoAlarm's CAP Profile](https://drive.google.com/file/d/1wwDcpaiPXH9fdwTobPqC5BDkmGEJku8T/view).

In the following the different awareness levels and hazard types are explained.

### Awareness Levels
- **Moderate**: The weather is potentially dangerous. The weather phenomena that have been forecast are not unusual, but be attentive if you intend to practice activities exposed to meteorological risks. Keep informed about the expected meteorological conditions and do not take any avoidable risks.
- **Severe**: The weather is dangerous. Unusual meteorological phenomena have been forecast. Damage and casualties are likely to happen. Be very vigilant and keep regularly informed about the detailed expected meteorological conditions. Be aware of the risks that might be unavoidable. Follow any advice given by your authorities.
- **Extreme**: The weather is very dangerous. Exceptionally intense meteorological phenomena have been forecast. Major damage and accidents are likely, in many cases with a threat to life and limb, over a wide area. Keep frequently informed about detailed expected meteorological conditions and risks. Follow orders and any advice given by your authorities under all circumstances. Be prepared for extraordinary measures.

### Hazard Types
- **Wind**: Hazardous event characterised by high wind speeds, which, especially when occurring as wind gusts, may pose serious risks to infrastructure, transportation, and outdoor activities.
- **Snow or Ice**: Hazardous event characterised by snow accumulation, ice formation, or freezing rain, causing slippery conditions and reduced visibility. These conditions may interfere with outdoor activities, travel, and daily life. Ice may form on wet and freezing surfaces or be triggered by freezing rain.
- **Thunderstorm**: Hazardous event characterised by intense lightning and thunder. Often accompanied by heavy rainfall, strong wind gusts, and precipitation in the form of hail or sleet. These conditions may pose severe risks to human life and property, with lightning strikes potentially causing wildfires, especially in dry conditions.
- **Fog**: Hazardous event characterised by significantly reduced visibility. This may negatively impact road safety, aviation, and navigation, particularly in remote or unfamiliar areas.
- **High Temperature**: Hazardous event characterised by a period of abnormally and uncomfortably hot weather, with temperatures exceeding the typical averages for a given area. Prolonged heat stress is exacerbated by elevated minimum temperatures, as hotter nights hinder recovery from daytime heat.
- **Low Temperature**: Hazardous event characterised by a prolonged period of very low temperatures relative to climatic norms for the location. These conditions may pose health risks, particularly with extended exposure, and may also affect infrastructure.
- **Coastal Event**: Hazardous event characterised by conditions impacting coastlines, such as storm surges, high tides, and strong winds. These events may result in coastal flooding, property damage, and risks to human life and the environment.
- **Forest Fire**: Hazardous event characterised by weather conditions conducive to increased wildfire risk, such as high temperatures, low humidity, and strong winds. These conditions not only increase the likelihood of wildfires but also accelerate their spread.
- **Avalanche**: Hazardous event characterised by a rapid flow of snow, ice, and debris down a mountainside, often triggered by natural or human activity. The risk of avalanches increases after heavy snowfall, warming temperatures, or changes in the stability of the snowpack.
- **Rain**: Hazardous event characterised by intense or prolonged rainfall, which may lead to localised or widespread flooding and landslides. These conditions may also reduce visibility and increase the risk of aquaplaning on roads.
- **Flood**: Hazardous event characterised by the inundation of land areas not normally covered by water, predominantly caused by river overflow due to excessive rainfall, rapid snowmelt, or ice jams. These events may result in long-lasting impacts on communities and ecosystems.
- **Rain Flood**: Hazardous event characterised by a rapid rise in water levels caused by intense rainfall over a small area in a short time frame. These events often involve fast-moving water, which may carry debris such as logs and boulders, posing significant risks to people and infrastructure.
- **Marine Hazard**: Hazardous event characterised by dangerous conditions at sea, including high waves, strong winds, and storm surges. These events primarily affect marine activities, such as shipping, fishing, and offshore operations.
- **Drought**: Hazardous event characterised by a prolonged deficiency of precipitation over an extended period, leading to water shortages that adversely affect agriculture, ecosystems, and water resources.

*Page contains content and information from EUMETNET/MeteoAlarm (CC BY 4.0).*