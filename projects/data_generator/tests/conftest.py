"""Common test fixtures."""
import pytest
from pathlib import Path
import tempfile
from datetime import datetime

from data_generator.persistence import JsonPersistence
from data_generator.generator import DataFactory

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def json_persistence(temp_dir):
    return JsonPersistence(temp_dir)

@pytest.fixture
def data_factory(json_persistence):
    return DataFactory(persistence=json_persistence)