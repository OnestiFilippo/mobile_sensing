import sys
from mqttMS import Operation
import pytest
import json
from hypothesis import given, strategies as st
from unittest.mock import Mock, patch, mock_open

class TestProperty():
    @given(payload=st.fixed_dictionaries({
            "datetime": st.text(),
            "g_value": st.integers(),
            "lat": st.text(),
            "long": st.text()
        }).map(lambda d: json.dumps([d, {"name": "record_dd-mm-yy_hh_mm.json"}]).encode('utf-8')))
    @patch('mqttMS.open', new_callable=mock_open)
    def test_write_file_property_based(self, mock_open, payload):
        result = Operation._write_file(payload)

        if result:
            mock_open.assert_called_once()
            filename = json.loads(payload.decode('utf-8'))[-1]["name"]
            mock_open.assert_called_once_with(f"testrecords/{filename}", "w")
            mock_open.return_value.write.assert_called_once_with(
                json.dumps(json.loads(payload.decode('utf-8'))[:-1], sort_keys=True, indent=4)
            )
        else:
            mock_open.assert_not_called()
