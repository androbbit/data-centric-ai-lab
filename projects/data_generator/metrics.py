"""Generation metrics and statistics."""
from typing import Any, Dict, List
import time
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GenerationMetrics:
    recipe_name: str
    start_time: datetime
    end_time: datetime
    record_count: int
    validation_errors: int
    
    @property
    def duration_seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()

class MetricsCollector:
    def __init__(self):
        self.metrics: List[GenerationMetrics] = []
        
    def add_metrics(self, metrics: GenerationMetrics) -> None:
        self.metrics.append(metrics)
        
    def get_summary(self) -> Dict[str, Any]:
        total_records = sum(m.record_count for m in self.metrics)
        total_duration = sum(m.duration_seconds for m in self.metrics)
        total_errors = sum(m.validation_errors for m in self.metrics)
        
        return {
            "total_records": total_records,
            "total_duration_seconds": total_duration,
            "records_per_second": total_records / total_duration if total_duration > 0 else 0,
            "total_validation_errors": total_errors,
            "recipe_metrics": {
                m.recipe_name: {
                    "records": m.record_count,
                    "duration_seconds": m.duration_seconds,
                    "validation_errors": m.validation_errors
                }
                for m in self.metrics
            }
        }