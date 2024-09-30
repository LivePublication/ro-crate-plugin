"""
Unit tests for the scanner module.
"""
import pytest
import tempfile
import os
from src.logic.scanner import scanner


def test_no_rocrates():
    temp_dir = tempfile.TemporaryDirectory()
    assert scanner(str(temp_dir)) == []
    
def test_none_rocrates():
    assert scanner(None) == []

def test_one_rocrate():
    with tempfile.TemporaryDirectory() as temp_dir:
        ro_crate_path = os.path.join(temp_dir, "ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")  # Write a minimal JSON object

        detected_paths = scanner(str(temp_dir))
        assert detected_paths == [temp_dir]

def test_multiple_rocrates():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "one"))
        os.makedirs(os.path.join(temp_dir, "two"))
        
        ro_crate_path = os.path.join(temp_dir, "one/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")

        ro_crate_path_two = os.path.join(temp_dir, "two/ro-crate-metadata.json")
        with open(ro_crate_path_two, 'w') as f:
            f.write("{}")
        
        detected_paths = scanner(str(temp_dir))
        assert detected_paths == [os.path.join(temp_dir, "one"), os.path.join(temp_dir, "two")]
