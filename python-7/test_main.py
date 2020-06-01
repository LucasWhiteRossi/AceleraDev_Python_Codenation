from main import get_temperature
from unittest.mock import patch
import pytest


valid_test_data = [
                (62, 16, -14.235004, -51.92528),
                (70, 21, -14.26, -51.92528),
                (90, 32, -15.24, -49.92528)
                ]


@pytest.mark.parametrize('fahrenheit, expected_celsius, lat, lng',
                         valid_test_data)
def test_get_temperature_by_lat_lng(fahrenheit, expected_celsius, lat, lng):

    mock_requests = patch('main.requests.get')

    temperature = {"currently": {"temperature": fahrenheit}}
    # part of original json structure to be mocked on request

    mock_response = mock_requests.start()
    mock_response.return_value.json.return_value = temperature
    celsius = get_temperature(lat, lng)
    mock_requests.stop()

    assert celsius == expected_celsius
