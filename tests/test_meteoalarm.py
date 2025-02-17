import pytest
from datetime import datetime
import pytz
from unittest.mock import patch, mock_open
import json
from meteoalarm import MeteoAlarm, Alert

# Sample test data
SAMPLE_URLS_YAML = """
estonia: https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-estonia
denmark: https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-denmark
"""

SAMPLE_ATOM_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:cap="urn:oasis:names:tc:emergency:cap:1.2">
    <link href="https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-estonia" rel="self"/>
    <entry>
        <cap:geocode>
            <valueName>EMMA_ID</valueName>
            <value>EE013</value>
        </cap:geocode>
        <link href="https://feeds.meteoalarm.org/api/v1/warnings/feeds-estonia/ede7f627-1b35-4479-8168-1c6f71f0d304" type="application/cap+xml"/>
        <cap:areaDesc>Valga maakond</cap:areaDesc>
        <cap:event>STURMBÖEN</cap:event>
        <cap:sent>2025-02-04T10:45:01+00:00</cap:sent>
        <cap:expires>2025-02-05T10:36:06+00:00</cap:expires>
        <cap:effective>2025-02-04T10:46:01+00:00</cap:effective>
        <cap:onset>2025-02-04T10:45:01+00:00</cap:onset>
        <cap:certainty>Likely</cap:certainty>
        <cap:severity>Moderate</cap:severity>
        <cap:urgency>Immediate</cap:urgency>
    </entry>
</feed>"""

SAMPLE_CAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
    <identifier>2.49.0.0.233.0.EE2025020412450132</identifier>
    <sender>test@example.com</sender>
    <sent>2025-02-04T10:45:01+00:00</sent>
    <status>Actual</status>
    <msgType>Alert</msgType>
    <scope>Public</scope>
    <info>
        <language>en-EN</language>
        <category>Met</category>
        <event>Strong Wind</event>
        <urgency>Immediate</urgency>
        <severity>Moderate</severity>
        <certainty>Likely</certainty>
        <onset>2025-02-04T10:45:01+00:00</onset>
        <effective>2025-02-04T10:46:01+00:00</effective>
        <expires>2025-02-05T10:36:06+00:00</expires>
        <senderName>Test Agency</senderName>
        <headline>Strong Wind Warning</headline>
        <description>Test description in English</description>
        <web>http://example.com</web>
        <contact>Test Contact</contact>
        <parameter>
            <valueName>awareness_level</valueName>
            <value>2; yellow; Moderate</value>
        </parameter>
        <parameter>
            <valueName>awareness_type</valueName>
            <value>1; Wind</value>
        </parameter>
        <area>
            <areaDesc>Valga maakond</areaDesc>
            <geocode>
                <valueName>EMMA_ID</valueName>
                <value>EE013</value>
            </geocode>
        </area>
    </info>
    <info>
        <language>et-ET</language>
        <event>Tugev tuul</event>
        <headline>Tugeva tuule hoiatus</headline>
        <description>Test kirjeldus eesti keeles</description>
    </info>
</alert>"""

@pytest.fixture
def mock_files(monkeypatch):
    """Mock file operations for configuration files."""
    def mock_file_open(*args, **kwargs):
        if 'MeteoAlarm_urls.yaml' in str(args[0]):
            return mock_open(read_data=SAMPLE_URLS_YAML)(*args, **kwargs)
        elif 'geocodes.json' in str(args[0]):
            return mock_open(read_data=json.dumps({"features": []}))(*args, **kwargs)
        return mock_open()(*args, **kwargs)

    monkeypatch.setattr('builtins.open', mock_file_open)
    return mock_file_open

@pytest.fixture
def mock_requests(monkeypatch):
    """Mock HTTP requests."""
    class MockResponse:
        def __init__(self, content, status_code=200):
            self.content = content.encode('utf-8')
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("HTTP Error")

    def mock_get(url):
        if 'feeds/meteoalarm-legacy-atom' in url:
            return MockResponse(SAMPLE_ATOM_FEED)
        elif 'warning' in url or 'feeds-estonia' in url:
            return MockResponse(SAMPLE_CAP_XML)
        return MockResponse("", 404)

    monkeypatch.setattr('requests.get', mock_get)
    return mock_get

def test_initialization(mock_files, mock_requests):
    """Test basic initialization of MeteoAlarm."""
    alarm = MeteoAlarm(['estonia'])
    assert len(alarm) > 0
    assert isinstance(alarm[0], Alert)

def test_error_handling(mock_files):
    """Test error handling for invalid countries."""
    with pytest.raises(ValueError, match="No URL configuration found for country: invalid_country"):
        MeteoAlarm(['invalid_country'])

def test_empty_country_list(mock_files):
    """Test initialization with empty country list."""
    with pytest.raises(ValueError, match="No countries provided"):
        MeteoAlarm([])

def test_none_country_list(mock_files):
    """Test initialization with None as country list."""
    with pytest.raises(ValueError, match="Countries list cannot be None"):
        MeteoAlarm(None)

def test_invalid_country_type(mock_files):
    """Test initialization with invalid country type."""
    with pytest.raises(ValueError, match="Countries must be provided as a list"):
        MeteoAlarm("estonia")

def test_available_languages(mock_files, mock_requests):
    """Test available languages across all warnings."""
    alarm = MeteoAlarm(['estonia'])
    languages = alarm.available_languages()

    assert isinstance(languages, set)
    assert len(languages) > 0
    assert "en-EN" in languages
    assert "et-ET" in languages

def test_filter_warnings(mock_files, mock_requests):
    """Test warning filtering."""
    alarm = MeteoAlarm(['estonia'])
    filtered = alarm.filter(severity="Moderate")
    assert isinstance(filtered, list)
    assert len(filtered) > 0

    for warning in filtered:
        assert warning.severity == "Moderate"

    # Test filtering by non-existent severity
    filtered = alarm.filter(severity="NonExistent")
    assert isinstance(filtered, list)
    assert len(filtered) == 0

    # Test filtering by multiple criteria
    filtered = alarm.filter(severity="Moderate", urgency="Immediate")
    assert isinstance(filtered, list)
    for warning in filtered:
        assert warning.severity == "Moderate"
        assert warning.urgency == "Immediate"

def test_warning_string_representation(mock_files, mock_requests):
    """Test string representation of warnings."""
    alarm = MeteoAlarm(['estonia'])
    warning = alarm[0]
    str_repr = str(warning)
    assert "Weather Warning for" in str_repr
    assert warning.severity in str_repr

def test_case_insensitive_country(mock_files, mock_requests):
    """Test that country names are case insensitive."""
    alarm = MeteoAlarm(['ESTONIA'])
    assert len(alarm) > 0