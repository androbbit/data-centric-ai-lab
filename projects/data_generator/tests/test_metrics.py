"""Test metrics collection."""
from datetime import datetime
from data_generator.metrics import GenerationMetrics, MetricsCollector

def test_metrics_collection():
    collector = MetricsCollector()
    
    # Add some test metrics
    metrics1 = GenerationMetrics(
        recipe_name="test1",
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 10, 1),
        record_count=100,
        validation_errors=0
    )
    
    metrics2 = GenerationMetrics(
        recipe_name="test2",
        start_time=datetime(2025, 1, 1, 10, 1),
        end_time=datetime(2025, 1, 1, 10, 2),
        record_count=200,
        validation_errors=2
    )
    
    collector.add_metrics(metrics1)
    collector.add_metrics(metrics2)
    
    summary = collector.get_summary()
    assert summary["total_records"] == 300
    assert summary["total_validation_errors"] == 2
    assert len(summary["recipe_metrics"]) == 2