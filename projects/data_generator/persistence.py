"""Data persistence handlers."""
from typing import Any, Dict
import json
from pathlib import Path
import pickle
from abc import ABC, abstractmethod

class DataPersistence(ABC):
    """Abstract base class for data persistence."""
    
    @abstractmethod
    def save(self, name: str, data: Any) -> None:
        pass
    
    @abstractmethod
    def load(self, name: str) -> Any:
        pass

class JsonPersistence(DataPersistence):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, name: str, data: Any) -> None:
        with open(self.output_dir / f"{name}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def load(self, name: str) -> Any:
        with open(self.output_dir / f"{name}.json", "r") as f:
            return json.load(f)

class PicklePersistence(DataPersistence):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, name: str, data: Any) -> None:
        with open(self.output_dir / f"{name}.pkl", "wb") as f:
            pickle.dump(data, f)
    
    def load(self, name: str) -> Any:
        with open(self.output_dir / f"{name}.pkl", "rb") as f:
            return pickle.load(f)