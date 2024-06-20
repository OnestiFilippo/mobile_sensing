import sys
from mqttMS import Operation, on_connect, on_message
import pytest
import json
from unittest.mock import Mock, patch

class TestIntegration():
    @pytest.fixture
    def mock_mqtt_client(self):
        client = Mock()
        client.subscribe = Mock()
        return client

    def test_on_connect(self, mock_mqtt_client):
        # Chiama la funzione on_connect
        on_connect(mock_mqtt_client, None, None, 0)

        # Verifica che la funzione subscribe sia stata chiamata con l'argomento corretto
        mock_mqtt_client.subscribe.assert_called_once_with("records")

    @patch('mqttMS.Operation._write_file', return_value=True)
    def test_on_message_write_file_success(self, mock_write_file):
        mock_msg = Mock()
        mock_msg.topic = "records"
        payload = json.dumps([{"name": "testfile"}])
        mock_msg.payload = payload

        with patch('builtins.print') as mocked_print:
            on_message(None, None, mock_msg)
            mocked_print.assert_any_call("Record saved")

    @patch('mqttMS.Operation._write_file', return_value=False)
    def test_on_message_write_file_failure(self, mock_write_file):
        mock_msg = Mock()
        mock_msg.topic = "records"
        payload = json.dumps([{"name": "testfile"}])
        mock_msg.payload = payload

        with patch('builtins.print') as mocked_print:
            on_message(None, None, mock_msg)
            mocked_print.assert_any_call("Error saving record")
