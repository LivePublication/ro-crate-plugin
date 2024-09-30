"""
Unit tests for the scanner module.
"""
import pytest
import tempfile
import os
from src.logic.scanner import scanner


def test_none_input_returns_empty_list():
    assert scanner(None) == []


def test_empty_directory_returns_empty_list():
    with tempfile.TemporaryDirectory() as temp_dir:
        assert scanner(str(temp_dir)) == []


def test_empty_directories_returns_empty_list():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "one"))
        os.makedirs(os.path.join(temp_dir, "two"))
        os.makedirs(os.path.join(temp_dir, "three"))
        
        assert scanner(str(temp_dir)) == []


def test_single_rocrate_returns_rocrate_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        ro_crate_path = os.path.join(temp_dir, "ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")  # Write a minimal JSON object

        detected_paths = scanner(str(temp_dir))
        assert detected_paths == [temp_dir]


def test_multiple_rocrates_returns_all_rocrate_dirs():
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


def test_single_rocrate_multiple_dirs_returns_correct_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "one"))
        os.makedirs(os.path.join(temp_dir, "two"))
        os.makedirs(os.path.join(temp_dir, "three"))
        
        ro_crate_path = os.path.join(temp_dir, "one/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")
        
        detected_paths = scanner(str(temp_dir))
        assert detected_paths == [os.path.join(temp_dir, "one")]


def test_multiple_rocrates_multiple_dirs_returns_correct_dirs():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.makedirs(os.path.join(temp_dir, "one"))
        os.makedirs(os.path.join(temp_dir, "two"))
        os.makedirs(os.path.join(temp_dir, "three"))
        
        ro_crate_path = os.path.join(temp_dir, "one/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")
            
        ro_crate_path_two = os.path.join(temp_dir, "two/ro-crate-metadata.json")
        with open(ro_crate_path_two, 'w') as f:
            f.write("{}")

        assert sorted(scanner(str(temp_dir))) == [os.path.join(temp_dir, "one"), os.path.join(temp_dir, "two")]


def test_large_number_rocrates_returns_correct_dirs():
    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(1000):
            os.makedirs(os.path.join(temp_dir, f"{i}"))
            ro_crate_path = os.path.join(temp_dir, f"{i}/ro-crate-metadata.json")
            with open(ro_crate_path, 'w') as f:
                f.write("{}")
        
        assert sorted(scanner(str(temp_dir))) == sorted([os.path.join(temp_dir, str(i)) for i in range(1000)])


def test_large_number_rocrates_returns_correct_number_dirs():
    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(1000):
            os.makedirs(os.path.join(temp_dir, f"{i}"))
            ro_crate_path = os.path.join(temp_dir, f"{i}/ro-crate-metadata.json")
            with open(ro_crate_path, 'w') as f:
                f.write("{}")
        
        assert len(scanner(str(temp_dir))) == 1000
