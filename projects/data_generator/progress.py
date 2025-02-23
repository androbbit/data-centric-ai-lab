"""Progress reporting utilities."""
from typing import Optional
from tqdm import tqdm


class ProgressReporter:
    def __init__(self, total_recipes: int):
        self.progress_bar = tqdm(
            total=total_recipes,
            desc="Generating datasets",
            unit="recipe"
        )
        
    def update(self, recipe_name: str) -> None:
        self.progress_bar.set_description(
            f"Generated {recipe_name}"
        )
        self.progress_bar.update(1)
        
    def close(self) -> None:
        self.progress_bar.close()
