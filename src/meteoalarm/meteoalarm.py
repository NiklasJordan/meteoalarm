import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz
import os
import yaml
import json

# Constants
NAMESPACE_CAP = "urn:oasis:names:tc:emergency:cap:1.2"
NAMESPACE_ATOM = "http://www.w3.org/2005/Atom"

@dataclass
class Alert:
    category: str
    event: str
    urgency: str
    severity: str
    certainty: str
    onset: datetime
    effective: datetime
    expires: datetime
    sender: Dict[str, str]
    headline: Dict[str, str]
    description: Dict[str, str]
    awareness_level: str
    awareness_type: str
    area: Dict[str, str]
    country: str
    geometry: Optional[str] = None

    def get_available_languages(self) -> List[str]:
        """Get list of available languages for this warning."""
        # Since both headline and description should have the same languages,
        # we can use either one
        return list(self.description.keys())

    def get_description(self, lang: str = "en-EN") -> Optional[str]:
        """
        Get description in specified language.
        Returns None if language is not available.
        """
        return self.description.get(lang)

    def get_headline(self, lang: str = "en-EN") -> Optional[str]:
        """
        Get headline in specified language.
        Returns None if language is not available.
        """
        return self.headline.get(lang)

    def __str__(self) -> str:
        """String representation of the warning using English if available."""
        # Default to English, fallback to first available language
        lang = "en-EN"
        if lang not in self.get_available_languages():
            lang = self.get_available_languages()[0]

        return (f"Weather Warning for {self.area['areaDesc']} ({self.country})\n"
                f"Headline: {self.get_headline(lang)}\n"
                f"Severity: {self.severity}\n"
                f"Valid until: {self.expires}")

    def matches_filter(self, **kwargs) -> bool:
        """Check if warning matches all filter criteria."""
        for key, value in kwargs.items():
            # Handle nested dictionary attributes
            if key in ['description', 'headline'] and isinstance(value, str):
                # Search in all languages
                if not any(value.lower() in v.lower() for v in getattr(self, key).values()):
                    return False
            # Handle dictionary attributes
            elif key in ['sender', 'area'] and isinstance(value, str):
                if not any(value.lower() in v.lower() for v in getattr(self, key).values()):
                    return False
            # Handle datetime attributes
            elif key in ['onset', 'effective', 'expires'] and isinstance(value, (datetime, str)):
                if isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        return False
                if getattr(self, key) != value:
                    return False
            # Handle regular attributes
            else:
                attr_value = getattr(self, key, None)
                if attr_value is None:
                    return False
                if isinstance(attr_value, str) and isinstance(value, str):
                    if value.lower() not in attr_value.lower():
                        return False
                elif attr_value != value:
                    return False
        return True

class MeteoAlarm:
    def __init__(self, countries: List[str]):
        """Initialize and fetch weather warnings for specified countries."""
        self.country_urls = self._load_urls()
        self.geocodes = self._load_geocodes()
        self._warnings = self._get_all_warnings(countries)

    def __iter__(self):
        """Make the MeteoAlarm object directly iterable."""
        return iter(self._warnings)

    def __len__(self):
        """Return the number of warnings."""
        return len(self._warnings)

    def __getitem__(self, index):
        """Allow indexing of warnings."""
        return self._warnings[index]

    def __call__(self):
        """Allow the object to be called to return all warnings."""
        return self._warnings

    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse datetime string to datetime object."""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.astimezone(pytz.UTC)
        except ValueError:
            return None

    def _load_urls(self) -> Dict[str, str]:
        """Load country URLs from YAML file."""
        try:
            with resources.files('meteoalarm.assets').joinpath('MeteoAlarm_urls.yaml').open('r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise FileNotFoundError(f"Error loading country URLs configuration: {str(e)}")

    def _load_geocodes(self) -> Dict[str, str]:
        """Load geocodes from JSON file."""
        try:
            with resources.files('meteoalarm.assets').joinpath('geocodes.json').open('r') as file:
                data = json.load(file)
                geocodes = {}
                for feature in data['features']:
                    if feature['properties']['type'] == 'EMMA_ID':
                        emma_id = feature['properties']['code']
                        geometry = json.dumps(feature['geometry'])
                        geocodes[emma_id] = geometry
                return geocodes
        except Exception as e:
            raise FileNotFoundError(f"Error loading geocodes: {str(e)}")

    def _get_parameter_value(self, info: ET.Element, param_name: str) -> Optional[str]:
        """Extract parameter value from info element."""
        for param in info.findall(f".//{{{NAMESPACE_CAP}}}parameter"):
            name = param.find(f"{{{NAMESPACE_CAP}}}valueName")
            value = param.find(f"{{{NAMESPACE_CAP}}}value")
            if name is not None and value is not None and name.text == param_name:
                return value.text.split(';')[0].strip()
        return None

    def _parse_warning_xml(self, xml_content: str, country: str) -> Alert:
        """Parse individual warning XML and create Alert object."""
        root = ET.fromstring(xml_content)
        descriptions = {}
        headlines = {}  # New dictionary for headlines
        sender = {}
        area = {}

        # Get base info from first info element
        first_info = root.find(f".//{{{NAMESPACE_CAP}}}info")

        # Parse area information
        area_elem = first_info.find(f".//{{{NAMESPACE_CAP}}}area")
        if area_elem is not None:
            area['areaDesc'] = area_elem.find(f".//{{{NAMESPACE_CAP}}}areaDesc").text
            geocode = area_elem.find(f".//{{{NAMESPACE_CAP}}}geocode")
            if geocode is not None:
                emma_id = geocode.find(f".//{{{NAMESPACE_CAP}}}value").text
                area['EMMA_ID'] = emma_id
                # Get geometry for this EMMA_ID
                geometry = self.geocodes.get(emma_id)
            else:
                geometry = None

        # Collect descriptions and headlines in different languages
        for info in root.findall(f".//{{{NAMESPACE_CAP}}}info"):
            lang = info.find(f".//{{{NAMESPACE_CAP}}}language").text
            desc = info.find(f".//{{{NAMESPACE_CAP}}}description").text
            headline = info.find(f".//{{{NAMESPACE_CAP}}}headline").text
            descriptions[lang] = desc
            headlines[lang] = headline

        # Collect sender information
        sender.update({
            'sender': root.find(f".//{{{NAMESPACE_CAP}}}sender").text,
            'senderName': first_info.find(f".//{{{NAMESPACE_CAP}}}senderName").text,
            'contact': first_info.find(f".//{{{NAMESPACE_CAP}}}contact").text,
            'web': first_info.find(f".//{{{NAMESPACE_CAP}}}web").text
        })

        return Alert(
            category=first_info.find(f".//{{{NAMESPACE_CAP}}}category").text,
            event=first_info.find(f".//{{{NAMESPACE_CAP}}}event").text,
            urgency=first_info.find(f".//{{{NAMESPACE_CAP}}}urgency").text,
            severity=first_info.find(f".//{{{NAMESPACE_CAP}}}severity").text,
            certainty=first_info.find(f".//{{{NAMESPACE_CAP}}}certainty").text,
            onset=self._parse_datetime(first_info.find(f".//{{{NAMESPACE_CAP}}}onset").text),
            effective=self._parse_datetime(first_info.find(f".//{{{NAMESPACE_CAP}}}effective").text),
            expires=self._parse_datetime(first_info.find(f".//{{{NAMESPACE_CAP}}}expires").text),
            sender=sender,
            headline=headlines,  # Now passing the dictionary of headlines
            description=descriptions,
            awareness_level=self._get_parameter_value(first_info, "awareness_level"),
            awareness_type=self._get_parameter_value(first_info, "awareness_type"),
            area=area,
            country=country,
            geometry=geometry
        )

    def _get_warnings_for_country(self, country: str) -> List[Alert]:
        """Get weather warnings for a specific country."""
        url = self.country_urls.get(country.lower())
        if not url:
            raise ValueError(f"No URL configuration found for country: {country}")

        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        warnings = []

        for entry in root.findall(f".//{{{NAMESPACE_ATOM}}}entry"):
            warning_link = entry.find(f".//{{{NAMESPACE_ATOM}}}link[@type='application/cap+xml']")
            if warning_link is not None:
                warning_url = warning_link.get('href')
                warning_response = requests.get(warning_url)
                warning_response.raise_for_status()
                warning = self._parse_warning_xml(warning_response.content, country)
                warnings.append(warning)

        return warnings

    def _get_all_warnings(self, countries: List[str]) -> List[Alert]:
        """Get all weather warnings for the specified countries as a single list."""
        all_warnings = []
        for country in countries:
            try:
                country_warnings = self._get_warnings_for_country(country)
                all_warnings.extend(country_warnings)
            except Exception as e:
                print(f"Error fetching warnings for {country}: {str(e)}")
        return all_warnings

    def available_languages(self) -> Set[str]:
        """Return a set of all available languages across all warnings."""
        languages = set()
        for warning in self._warnings:
            languages.update(warning.available_languages())
        return languages

    def filter(self, **kwargs) -> 'MeteoAlarm':
        filtered_instance = MeteoAlarm([])  # Create empty instance
        filtered_instance._warnings = [
            warning for warning in self._warnings 
            if warning.matches_filter(**kwargs)
        ]
        return filtered_instance
