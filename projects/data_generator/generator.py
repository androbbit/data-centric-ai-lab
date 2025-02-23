"""Enhanced framework for generating and managing synthetic datasets."""
from typing import Any, Dict, List, Optional, Set, Type
from pathlib import Path
import logging
from concurrent.futures import as_completed
from datetime import datetime
import networkx as nx

from data_generator.schema import DataSchema, SchemaRegistry
from data_generator.persistence import DataPersistence
from data_generator.persistence import JsonPersistence
from data_generator.metrics import MetricsCollector, GenerationMetrics
from data_generator.progress import ProgressReporter


logger = logging.getLogger(__name__)

class DataRecipe:
    def __init__(
        self,
        name: str,
        schema: Optional[Type[DataSchema]] = None,
    ):
        self.name = name
        self.dependencies: List[str] = []
        self.generated_data: Any = None
        self.schema = schema
        self._validation_enabled = True
        
    def generate(self, input_data: Dict[str, Any] = None) -> Any:
        return self._generate(input_data)
        
    def requires(self, dependencies: List[str]) -> None:
        """Specify what other data this recipe depends on."""
        self.dependencies = dependencies
        
    def validate(self, data: Any) -> None:
        """Validate generated data against schema if available."""
        if not self._validation_enabled or not self.schema:
            return
            
        if isinstance(data, list):
            for item in data:
                self.schema(**item)
        else:
            self.schema(**data)
        
    def cleanup(self) -> None:
        """Override this to cleanup any resources if needed."""
        pass

class DataFactory:
    def __init__(
        self,
        persistence: Optional[DataPersistence] = None,
    ):
        self._recipes: Dict[str, DataRecipe] = {}
        self._generated: Dict[str, Any] = {}
        self._persistence = persistence or JsonPersistence(Path("./output"))
        self._metrics_collector = MetricsCollector()
        
    def generate(self) -> Dict[str, Any]:
        graph = self._build_dependency_graph()
        generation_order = list(nx.topological_sort(graph))
        completed = set()
        
        progress_reporter = ProgressReporter(len(generation_order))
        
        try:
            return self._generate_sequential(
                generation_order,
                completed,
            )
            
        finally:
            progress_reporter.close()
            
    def get_metrics(self) -> Dict[str, Any]:
        return self._metrics_collector.get_summary()

    def add_recipe(self, recipe: DataRecipe) -> None:
        """Register a new data generation recipe."""
        self._recipes[recipe.name] = recipe
        
    def _build_dependency_graph(self) -> nx.DiGraph:
        """Build a directed graph of recipe dependencies."""
        G = nx.DiGraph()
        for recipe_name, recipe in self._recipes.items():
            G.add_node(recipe_name)
            for dep in recipe.dependencies:
                G.add_edge(dep, recipe_name)
        
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Circular dependencies detected in recipes")
            
        return G
        
    def _can_generate(self, recipe_name: str, completed: Set[str]) -> bool:
        """Check if all dependencies for a recipe are satisfied."""
        recipe = self._recipes[recipe_name]
        return all(dep in completed for dep in recipe.dependencies)
    
    def _generate_sequential(
        self,
        generation_order: List[str],
        completed: Set[str]
    ) -> Dict[str, Any]:
        """Generate data sequentially."""
        for recipe_name in generation_order:
            self._generate_single(recipe_name, completed)
        return self._generated
    
    def _generate_single(self, recipe_name: str, completed: Set[str]) -> None:
        """Generate data for a single recipe."""
        recipe = self._recipes[recipe_name]
        deps = {
            dep: self._generated[dep]
            for dep in recipe.dependencies
        }
        
        logger.info(f"Generating data for {recipe_name}")
        data = recipe.generate(deps)
        
        # Validate
        recipe.validate(data)
        
        # Store
        self._generated[recipe_name] = data
        if self._persistence:
            self._persistence.save(recipe_name, data)
    
    def load(self, recipe_name: str) -> Any:
        """Load previously generated data."""
        return self._persistence.load(recipe_name)
    
    def cleanup(self) -> None:
        """Cleanup all recipes."""
        for recipe in self._recipes.values():
            recipe.cleanup()
        self._generated.clear()