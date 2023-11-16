import pytest

from stream_pipeline import validate_msg


def test_validate_message_basic_func_with_rating_type():
    assert validate_msg({'at': '2023-11-15T12:14:32.862269+00:00', 'site': '5', 'val': 2}) == True

def test_validate_message_basic_func_with_assistance_type():
    assert validate_msg({'at': '2023-11-15T12:14:32.862269+00:00', 'site': '5', 'val': -1, 'type': 1}) == True

def test_validate_message_basic_func_with_emergency_type():
    assert validate_msg({'at': '2023-11-15T12:14:32.862269+00:00', 'site': '5', 'val': -1, 'type': 0}) == True

def test_validate_message_invalid_rating_val():
    assert validate_msg({'at': '2023-11-15T12:14:32.862269+00:00', 'site': '5', 'val': 6}) == False

def test_validate_message_invalid_date():
    assert validate_msg({'at': '2023-11', 'site': '5', 'val': 2}) == False

def test_validate_message_missing_keys():
    assert validate_msg({'site': '5', 'val': '4'}) == False

def test_validate_message_err_keys():
    assert validate_msg({'at': '2023-11-15T12:15:37.926965+00:00', 'site': '5', 'val': 'ERR'}) == False

def test_validate_message_none_values():
    assert validate_msg({'at': '2023-11-15T12:14:23.852592+00:00', 'site': 'None', 'val': 0}) == False

def test_validate_message_inf_values():
    assert validate_msg({'at': '2023-11-15T12:14:40.871258+00:00', 'site': '2', 'val': 'INF'}) == False

def test_validate_message_invalid_type():
    assert validate_msg({'at': '2023-11-15T12:14:32.862269+00:00', 'site': '5', 'val': -1, 'type': 2}) == False