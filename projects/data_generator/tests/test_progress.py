"""Test progress reporting."""
from data_generator.progress import ProgressReporter

def test_progress_reporter(capsys):
    reporter = ProgressReporter(total_recipes=2)
    
    reporter.update("recipe1")
    reporter.update("recipe2")
    reporter.close()
    
    captured = capsys.readouterr()
    assert "Generated recipe1" in captured.err
    assert "Generated recipe2" in captured.err