"""Test main generator functionality."""
import pytest
from data_generator.generator import DataRecipe, DataFactory
from data_generator.schema import DataSchema

class TestSchema(DataSchema):
    id: int
    name: str

class TestRecipe(DataRecipe):
    def __init__(self):
        super().__init__("test", TestSchema)
    
    def _generate(self, input_data=None):
        return [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"}
        ]

class DependentRecipe(DataRecipe):
    def __init__(self):
        super().__init__("dependent")
        self.requires(["test"])
    
    def _generate(self, input_data):
        return [{"parent_id": item["id"]} for item in input_data["test"]]

def test_simple_generation(data_factory):
    recipe = TestRecipe()
    data_factory.add_recipe(recipe)
    
    result = data_factory.generate()
    assert "test" in result
    assert len(result["test"]) == 2
    assert result["test"][0]["name"] == "Test 1"

def test_dependency_resolution(data_factory):
    test_recipe = TestRecipe()
    dependent_recipe = DependentRecipe()
    
    data_factory.add_recipe(test_recipe)
    data_factory.add_recipe(dependent_recipe)
    
    result = data_factory.generate()
    
    assert "test" in result
    assert "dependent" in result
    assert len(result["dependent"]) == len(result["test"])
    assert result["dependent"][0]["parent_id"] == result["test"][0]["id"]

def test_metrics_collection(data_factory):
    recipe = TestRecipe()
    data_factory.add_recipe(recipe)
    
    data_factory.generate()
    metrics = data_factory.get_metrics()
    
    assert metrics["total_records"] >= 0
    assert metrics["total_duration_seconds"] >= 0
    