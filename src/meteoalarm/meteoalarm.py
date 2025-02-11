import datetime
from dataclasses import dataclass
from importlib import resources
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
    identifier: str
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

    def _parse_datetime(self, dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object with proper error handling."""
        if not dt_str:
            return None
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.astimezone(pytz.UTC)
        except (ValueError, AttributeError):
            return None

    def _get_parameter_value(self, info: ET.Element, param_name: str, default: str = '') -> str:
        """Extract parameter value from info element with proper error handling."""
        try:
            for param in info.findall(f".//{{{NAMESPACE_CAP}}}parameter"):
                name = param.find(f"{{{NAMESPACE_CAP}}}valueName")
                value = param.find(f"{{{NAMESPACE_CAP}}}value")
                if name is not None and value is not None and name.text == param_name:
                    return value.text.split(';')[0].strip()
            return default
        except (AttributeError, IndexError):
            return default

    def _parse_warning_xml(self, xml_content: str, country: str) -> Optional[Alert]:
        """Parse individual warning XML and create Alert object."""
        try:
            root = ET.fromstring(xml_content)
            first_info = root.find(f".//{{{NAMESPACE_CAP}}}info")

            if first_info is None:
                return None

            # Helper function to safely get text from XML element
            def safe_get_text(element: Optional[ET.Element], xpath: str, default: str = '') -> str:
                try:
                    elem = element.find(xpath) if element is not None else None
                    return elem.text if elem is not None and elem.text is not None else default
                except (AttributeError, TypeError):
                    return default

            # Get descriptions and headlines in different languages
            descriptions = {}
            headlines = {}
            for info in root.findall(f".//{{{NAMESPACE_CAP}}}info"):
                lang = safe_get_text(info, f".//{{{NAMESPACE_CAP}}}language")
                if lang:
                    desc = safe_get_text(info, f".//{{{NAMESPACE_CAP}}}description")
                    headline = safe_get_text(info, f".//{{{NAMESPACE_CAP}}}headline")
                    if desc:
                        descriptions[lang] = desc
                    if headline:
                        headlines[lang] = headline

            # Get sender information
            sender = {
                'sender': safe_get_text(root, f".//{{{NAMESPACE_CAP}}}sender"),
                'senderName': safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}senderName"),
                'contact': safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}contact"),
                'web': safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}web")
            }

            # Get area information
            area = {}
            area_elem = first_info.find(f".//{{{NAMESPACE_CAP}}}area")
            if area_elem is not None:
                area['areaDesc'] = safe_get_text(area_elem, f".//{{{NAMESPACE_CAP}}}areaDesc")
                geocode = area_elem.find(f".//{{{NAMESPACE_CAP}}}geocode")
                if geocode is not None:
                    area['EMMA_ID'] = safe_get_text(geocode, f".//{{{NAMESPACE_CAP}}}value")

            # Create Alert object with proper error handling for all fields
            return Alert(
                identifier=safe_get_text(root, f".//{{{NAMESPACE_CAP}}}identifier"),
                category=safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}category"),
                event=safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}event"),
                urgency=safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}urgency"),
                severity=safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}severity"),
                certainty=safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}certainty"),
                onset=self._parse_datetime(safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}onset")),
                effective=self._parse_datetime(safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}effective")),
                expires=self._parse_datetime(safe_get_text(first_info, f".//{{{NAMESPACE_CAP}}}expires")),
                sender=sender,
                headline=headlines,
                description=descriptions,
                awareness_level=self._get_parameter_value(first_info, "awareness_level"),
                awareness_type=self._get_parameter_value(first_info, "awareness_type"),
                area=area,
                country=country,
                geometry=self.geocodes.get(area.get('EMMA_ID'))
            )
        except Exception as e:
            print(f"Error parsing warning for {country}: {str(e)}")
            return None

    def _get_warnings_for_country(self, country: str) -> List[Alert]:
        """Get weather warnings for a specific country."""
        try:
            url = self.country_urls.get(country.lower())
            if not url:
                raise ValueError(f"No URL configuration found for country: {country}")

            # Get the Atom feed
            response = requests.get(url)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            warnings = []

            # Process each entry in the feed
            for entry in root.findall(f".//{{{NAMESPACE_ATOM}}}entry"):
                try:
                    warning_link = entry.find(f".//{{{NAMESPACE_ATOM}}}link[@type='application/cap+xml']")
                    if warning_link is not None:
                        warning_url = warning_link.get('href')
                        warning_response = requests.get(warning_url)
                        warning_response.raise_for_status()

                        warning = self._parse_warning_xml(warning_response.content, country)
                        if warning:
                            warnings.append(warning)
                except Exception as e:
                    print(f"Error processing entry for {country}: {str(e)}")
                    continue

            return warnings
        except Exception as e:
            print(f"Error fetching warnings for {country}: {str(e)}")
            return []

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