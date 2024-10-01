import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.logic.validator import Validator, ValidatorCommand


def test_setup_non_existent_rocrate_validator_directory():
    with patch('os.path.isdir', return_value=False):
        with pytest.raises(FileNotFoundError):
            Validator()


@pytest.fixture
def validator():
    with patch.object(Validator, "setup", return_value=None):
        return Validator()


def test_setup(validator):
    assert validator.valid_rocrates == []
    assert validator.invalid_rocrates == []


def test_valid_rocrate(validator):
    with tempfile.TemporaryDirectory() as temp_dir:
        ro_crate_path = os.path.join(temp_dir, "ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")

        with patch('subprocess.run', return_value=MagicMock(returncode=0)):
            validator.validate_rocrate(temp_dir)

        assert validator.valid_rocrates == [temp_dir]
        assert validator.invalid_rocrates == []


def test_invalid_rocrate(validator):
    with tempfile.TemporaryDirectory() as temp_dir:
        ro_crate_path = os.path.join(temp_dir, "ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")

        with patch('subprocess.run', return_value=MagicMock(returncode=1)):
            validator.validate_rocrate(temp_dir)

        assert validator.valid_rocrates == []
        assert validator.invalid_rocrates == [temp_dir]
        

def test_none_path(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate(None)

def test_invalid_path(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate("invalid_path")
        
def test_invalid_path_type_int(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate(int(1))

def test_invalid_path_type_float(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate(float(1))


def test_invalid_path_type_list(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate([])


def test_invalid_path_type_dict(validator):
    with pytest.raises(FileNotFoundError):
        validator.validate_rocrate({"key": "value"})


def test_valid_rocrates(validator):
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(os.path.join(temp_dir, "one"))
        os.mkdir(os.path.join(temp_dir, "two"))
        os.mkdir(os.path.join(temp_dir, "three"))
        
        ro_crate_path = os.path.join(temp_dir, "one/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")
            
        ro_crate_path = os.path.join(temp_dir, "two/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")
            
        ro_crate_path = os.path.join(temp_dir, "three/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")

        with patch('subprocess.run', return_value=MagicMock(returncode=0)):
            validator.validate_rocrate(os.path.join(temp_dir, "one"))
            validator.validate_rocrate(os.path.join(temp_dir, "two"))
            validator.validate_rocrate(os.path.join(temp_dir, "three"))

        assert validator.valid_rocrates == [os.path.join(temp_dir, "one"), os.path.join(temp_dir, "two"), os.path.join(temp_dir, "three")]
        assert validator.invalid_rocrates == []

def test_valid_rocrate_multiple_directories(validator):
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(os.path.join(temp_dir, "one"))
        os.mkdir(os.path.join(temp_dir, "two"))
        os.mkdir(os.path.join(temp_dir, "three"))
        
        ro_crate_path = os.path.join(temp_dir, "one/ro-crate-metadata.json")
        with open(ro_crate_path, 'w') as f:
            f.write("{}")

        with patch('subprocess.run', return_value=MagicMock(returncode=0)):
            validator.validate_rocrate(os.path.join(temp_dir, "one"))
        
        assert validator.valid_rocrates == [os.path.join(temp_dir, "one")]
        assert validator.invalid_rocrates == []


def test_setup_dependencies_installed(validator):
    with patch('subprocess.run') as mock_run:
        validator.setup()
        mock_run.assert_called_once_with(ValidatorCommand.INSTALL_DEPENDENCIES.value, check=True)


def test_get_help(validator):
    with patch('subprocess.run') as mock_run:
        validator.get_help()
        mock_run.assert_called_once_with(ValidatorCommand.HELP.value, check=True)


def test_validate_invalid_rocrate(validator):
    with patch('subprocess.run') as mock_run:
        with tempfile.TemporaryDirectory() as temp_dir:
            validator.validate_rocrate(temp_dir)
            mock_run.assert_called_once_with(ValidatorCommand.VALIDATE.value + [temp_dir], stdout=-1, stderr=-1)


def test_validate_valid_rocrate(validator):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as temp_dir:
            ro_crate_path = os.path.join(temp_dir, "ro-crate-metadata.json")
            with open(ro_crate_path, 'w') as f:
                f.write("{}")
            
            validator.validate_rocrate(ro_crate_path)

            mock_run.assert_called_once_with(ValidatorCommand.VALIDATE.value + [os.path.join(temp_dir, "ro-crate-metadata.json")], stdout=-1, stderr=-1)


