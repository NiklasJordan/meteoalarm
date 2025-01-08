import requests
from xml.etree import ElementTree as ET
from dataclasses import dataclass
from typing import List, Optional, Any
from datetime import datetime
import yaml
import os

@dataclass
class Alert:
    id: str
    title: str
    updated: datetime
    published: datetime
    identifier: str
    sender: Optional[str] = None
    sent: Optional[datetime] = None
    status: Optional[str] = None
    msgType: Optional[str] = None
    scope: Optional[str] = None
    language: Optional[str] = None
    category: Optional[str] = None
    event: Optional[str] = None
    responseType: Optional[str] = None
    urgency: Optional[str] = None
    severity: Optional[str] = None
    certainty: Optional[str] = None
    effective: Optional[datetime] = None
    onset: Optional[datetime] = None
    expires: Optional[datetime] = None
    senderName: Optional[str] = None
    headline: Optional[str] = None
    description: Optional[str] = None
    instruction: Optional[str] = None
    web: Optional[str] = None
    contact: Optional[str] = None
    awareness_level: Optional[str] = None
    awareness_type: Optional[str] = None
    areaDesc: Optional[str] = None
    geocode: Optional[str] = None

    def __str__(self):
        return f"""Alert Summary:
    Title: {self.title}
    Event: {self.event}
    Area: {self.areaDesc}
    Severity: {self.severity}
    Urgency: {self.urgency}
    Certainty: {self.certainty}
    Effective: {self.effective}
    Expires: {self.expires}
    Description: {self.description}
"""

class MeteoAlarm:
    def __init__(self, region: str = None, url: str = None):
        self.urls = self._load_urls()
        if region:
            self.url = self.urls.get(region.lower())
            if not self.url:
                raise ValueError(f"Invalid region: {region}")
        elif url:
            self.url = url
        else:
            raise ValueError("Either 'region' or 'url' must be provided")

        self.ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'cap': 'urn:oasis:names:tc:emergency:cap:1.2'
        }
        self.entries = self._parse()

    @staticmethod
    def _load_urls():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(script_dir, 'assets/MeteoAlarm_urls.yaml')
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    @classmethod
    def getRegions(cls):
        return list(cls._load_urls().keys())

    def _parse(self) -> List[Alert]:
        response = requests.get(self.url)
        root = ET.fromstring(response.content)
        entries = []

        for entry in root.findall('atom:entry', self.ns):
            entry_data = {}
            for child in entry:
                tag = child.tag.split('}')[-1]
                if tag in Alert.__annotations__:
                    if tag in ['updated', 'published']:
                        entry_data[tag] = datetime.fromisoformat(child.text.rstrip('Z'))
                    elif tag == 'id':
                        entry_data['id'] = child.text
                        detailed_alert = self._fetch_detailed_alert(child.text)
                        entry_data.update(detailed_alert)
                    else:
                        entry_data[tag] = child.text

            entries.append(Alert(**entry_data))

        return entries

    def _fetch_detailed_alert(self, url: str) -> dict:
        response = requests.get(url)
        root = ET.fromstring(response.content)
        alert_data = {}
    
        for elem in root.findall('.//cap:*', self.ns):
            tag = elem.tag.split('}')[-1]
            if tag in Alert.__annotations__:
                if tag in ['sent', 'effective', 'onset', 'expires']:
                    alert_data[tag] = datetime.fromisoformat(elem.text.rstrip('Z'))
                elif tag == 'parameter':
                    value_name = elem.find('cap:valueName', self.ns).text
                    value = elem.find('cap:value', self.ns).text
                    if value_name == 'awareness_level':
                        alert_data['awareness_level'] = value
                    elif value_name == 'awareness_type':
                        alert_data['awareness_type'] = value
                elif tag == 'area':
                    alert_data['areaDesc'] = elem.find('cap:areaDesc', self.ns).text
                    geocode = elem.find('cap:geocode', self.ns)
                    if geocode is not None:
                        value_name = geocode.find('cap:valueName', self.ns).text
                        if value_name == 'EMMA_ID':
                            alert_data['geocode'] = geocode.find('cap:value', self.ns).text
                else:
                    alert_data[tag] = elem.text
    
        return alert_data


    def filter(self, **kwargs):
        def match_entry(entry):
            for k, v in kwargs.items():
                attr_value = getattr(entry, k, None)
                if attr_value is None:
                    return False
                if isinstance(attr_value, str) and isinstance(v, str):
                    if v.lower() not in attr_value.lower():
                        return False
                elif attr_value != v:
                    return False
            return True
        
        filtered_entries = list(filter(match_entry, self.entries))
        return filtered_entries[0] if len(filtered_entries) == 1 else filtered_entries