"""Test persistence implementations."""
import pytest
import json
from datetime import datetime

def test_json_persistence_save_load(json_persistence):
    test_data = {"test": "data", "number": 42}
    json_persistence.save("test", test_data)
    
    loaded_data = json_persistence.load("test")
    assert loaded_data == test_data
