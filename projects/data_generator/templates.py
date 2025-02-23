"""Data generation templates."""
from typing import Any, Dict, List, Optional, Union
import random
from datetime import datetime, timedelta

import numpy as np
from faker import Faker

class Template:
    def __init__(self, faker: Optional[Faker] = None):
        self.faker = faker or Faker()
        
    def sequence(self, start: int = 1) -> callable:
        counter = start
        def generate():
            nonlocal counter
            value = counter
            counter += 1
            return value
        return generate
        
    def choice(self, options: List[Any]) -> callable:
        return lambda: random.choice(options)
    
    def randnorm(self, loc: float, scale: float) -> callable:
        return np.random.normal(loc, scale)
        
    def date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> callable:
        return lambda: self.faker.date_time_between(
            start_date=start_date,
            end_date=end_date
        )

class TemplateBuilder:
    def __init__(self):
        self.template = Template()
        self.fields: Dict[str, callable] = {}
        
    def add_field(
        self,
        name: str,
        generator: Union[callable, Any]
    ) -> "TemplateBuilder":
        if callable(generator):
            self.fields[name] = generator
        else:
            self.fields[name] = lambda: generator
        return self
        
    def build(self) -> callable:
        def generate() -> Dict[str, Any]:
            return {
                name: generator()
                for name, generator in self.fields.items()
            }
        return generate