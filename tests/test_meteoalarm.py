import unittest
from unittest.mock import patch, Mock
from meteoalarm import Meteoalarm, Warning

class TestMeteoalarm(unittest.TestCase):
    @patch('requests.get')
    def test_parse_warnings(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.content = '''
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:cap="urn:oasis:names:tc:emergency:cap:1.2">
            <entry>
                <id>test_id</id>
                <title>Test Warning</title>
                <updated>2025-01-08T12:00:00Z</updated>
                <published>2025-01-08T11:00:00Z</published>
                <cap:identifier>test_identifier</cap:identifier>
                <cap:event>yellow Wind</cap:event>
                <cap:severity>Moderate</cap:severity>
            </entry>
        </feed>
        '''
        mock_get.return_value = mock_response

        meteoalarm = Meteoalarm("https://example.com/feed")
        warnings = meteoalarm.entries

        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0].id, "test_id")
        self.assertEqual(warnings[0].title, "Test Warning")
        self.assertEqual(warnings[0].event, "yellow Wind")
        self.assertEqual(warnings[0].severity, "Moderate")

    def test_filter_warnings(self):
        warnings = [
            Warning(id="1", title="Yellow Wind", event="yellow Wind", severity="Moderate"),
            Warning(id="2", title="Orange Rain", event="orange Rain", severity="Severe"),
            Warning(id="3", title="Yellow Wind", event="yellow Wind", severity="Moderate"),
        ]

        meteoalarm = Meteoalarm("https://example.com/feed")
        meteoalarm.entries = warnings

        filtered = meteoalarm.filter(event="yellow Wind")
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].id, "1")
        self.assertEqual(filtered[1].id, "3")

        single_result = meteoalarm.filter(id="2")
        self.assertIsInstance(single_result, Warning)
        self.assertEqual(single_result.title, "Orange Rain")

if __name__ == '__main__':
    unittest.main()
