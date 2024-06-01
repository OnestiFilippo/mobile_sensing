import sys
sys.path.append('/home/filippoonesti/mobile_sensing')
from mqttMS import Operation
import pytest
import paho.mqtt.client as mqtt

class TestUnit():
    def test_write_file_correct(self):
        expected = True
        msg = '[{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"},{"name": "record_dd-mm-yy_hh_mm.json"}]'
        assert Operation._write_file(msg) == expected
    
    def test_write_file_incorrect(self):
        expected = False
        msg = '[{"datetime": "13:31:11","g_value": 43,"lat": "44.883560","long": "11.611293"},,{"name": "record_dd-mm-yy_hh_mm.json"}]'
        assert Operation._write_file(msg) == expected
    
