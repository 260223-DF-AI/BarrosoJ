import pytest
from generators import read_lines, batch, filter_by, filter_errors

def test_batch_correct_sizes():
    """Batch should yield correct batch sizes."""
    result = list(batch(range(7), 3))
    assert len(result) == 3
    assert len(result[0]) == 3
    assert len(result[2]) == 1

def test_filter_by_predicate():
    """Filter should only yield matching items."""
    test: list[int] = list(range(10))
    result = filter_by(test, lambda x: x % 2 == 0)
    assert list(result) == [0, 2, 4, 6, 8]

def test_read_lines_skips_empty():
    """Read lines should skip empty lines."""
    
    test_filepath: str = "samples/empty_lines.txt"

    for line in read_lines(test_filepath):
        assert line != ""


def test_filter_errors():
    """Filter Errors should only return lines with errors"""
    errors: list = []
    for error in filter_errors(list(read_lines("samples/app.log"))):
        assert 'ERROR' in error
        errors.append(error)

    # in app.log, only two errors
    assert len(errors) == 2

    