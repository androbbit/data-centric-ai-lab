"""Schema definitions for synthetic data validation."""
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
from datetime import datetime

class DataSchema(BaseModel):
    """Base class for data schemas."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"

    class Config:
        arbitrary_types_allowed = True

class SchemaRegistry:
    """Registry for data schemas."""
    _schemas: Dict[str, Type[DataSchema]] = {}

    @classmethod
    def register(cls, name: str, schema: Type[DataSchema]) -> None:
        cls._schemas[name] = schema

    @classmethod
    def get(cls, name: str) -> Type[DataSchema]:
        if name not in cls._schemas:
            raise KeyError(f"Schema {name} not found in registry")
        return cls._schemas[name]