import sys
from mqttMS import Operation
import pytest
import json
from unittest.mock import Mock, patch

class TestUnit():
    @patch('mqttMS.open', new_callable=Mock)
    def test_write_file_success(self, mock_open):
        payload = json.dumps([{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"},{"name": "record_dd-mm-yy_hh_mm.json"}])
        result = Operation._write_file(payload)

        mock_open.assert_called_once_with("testrecords/record_dd-mm-yy_hh_mm.json", "w")
        mock_open.return_value.write.assert_called_once_with(
            json.dumps([{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"}], sort_keys=True, indent=4)
        )
        assert result is True
        #msg = '[{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"},{"name": "record_dd-mm-yy_hh_mm.json"}]'
        #assert Operation._write_file(msg) == expected

    def test_write_file_failure(self):
        payload = '[{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"},,{"name": "record_dd-mm-yy_hh_mm.json"}]'
        result = Operation._write_file(payload)
        assert result is False

