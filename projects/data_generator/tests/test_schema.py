"""Test schema validation and registry functionality."""
import pytest
from datetime import datetime
from typing import List, Optional

import numpy as np
from pydantic import Field, ValidationError

from data_generator.schema import DataSchema, SchemaRegistry

class TestDataSchema(DataSchema):
    id: int
    temperature: float
    pressure: float
    thickness: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
def test_valid_test_data():
    """Test validation of valid test data."""
    test_data = {
        "id": 1,
        "temperature": np.random.normal(25, 2),
        "pressure": np.random.normal(1000, 50),
        "thickness": np.random.normal(0, 1)
    }
    
    data = TestDataSchema(**test_data)
    assert data.id == 1
    assert isinstance(data.temperature, float)
    assert isinstance(data.pressure, float)
    assert isinstance(data.thickness, float)
    assert isinstance(data.timestamp, datetime)
    
def test_invalid_test_data():
    """Test validation of invalid test data."""
    invalid_cases = [
        # Missing required field
        {
            "temperature": np.random.normal(25, 2),
            "pressure": np.random.normal(1000, 50),
        },
        # Invalid temperature
        {
            "id": 1,
            "temperature": None,
            "pressure": np.random.normal(1000, 50),
            "thickness": np.random.normal(0, 1)
        },
        # Invalid type for id
        {
            "id": "X",
            "temperature": np.random.normal(25, 2),
            "pressure": np.random.normal(1000, 50),
            "thickness": np.random.normal(0, 1)
        }
    ]
    
    for invalid_data in invalid_cases:
        with pytest.raises(ValidationError):
            TestDataSchema(**invalid_data)

def test_schema_registration():
    """Test schema registration and retrieval."""
    SchemaRegistry.register("data", TestDataSchema)
    
    assert SchemaRegistry.get("data") == TestDataSchema
    
def test_duplicate_registration():
    """Test handling of duplicate schema registration."""
    SchemaRegistry.register("test", TestDataSchema)
    
    # Re-registering should work (override)
    SchemaRegistry.register("test", TestDataSchema)
    assert SchemaRegistry.get("test") == TestDataSchema

def test_unknown_schema():
    """Test retrieval of unknown schema."""
    with pytest.raises(KeyError):
        SchemaRegistry.get("unknown-schema")
