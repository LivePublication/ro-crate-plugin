import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from rocrate import rocrate
import json
import os

# Assuming the classes and logic above are in a file named artifact_module.py
from src.logic.cache_manager import ARTIFACTS_DIR
from src.logic.artifact_manager import Artifact, EntityType

@pytest.fixture
def real_artifact():
    #real_rocrate = new rocrate()
    return Artifact(None, None)

# @pytest.fixture
# def mock_artifact():
#     mock_rocrate = MagicMock()
#     mock_rocrate.path = "/path/to/rocrate"
#     mock_rocrate.source = "/source/path"
    
#     mock_entity = MagicMock()
#     mock_entity.id = "artifact.txt"
#     mock_entity.name = "Test Artifact"
#     mock_entity.type = EntityType.FILE.value
#     mock_entity.properties = json.dumps({"key": "value"})
    
#     return Artifact(mock_rocrate, mock_entity)

# @pytest.fixture
# def mock_artifact_two():
#     mock_rocrate = MagicMock()
#     mock_rocrate.path = "/path/to/rocrate_two"
#     mock_rocrate.source = "/source/path_two"
    
#     mock_entity = MagicMock()
#     mock_entity.id = "artifact_two.txt"
#     mock_entity.name = "Test Artifact Two"
#     mock_entity.type = EntityType.FILE.value
#     mock_entity.properties = json.dumps({"key": "value"})
    
#     return Artifact(mock_rocrate, mock_entity)

@pytest.fixture
def create_mock_artifact():
    """Helper function to create a mock Artifact with specified values."""
    def _create_mock_artifact(rocrate_path, source_path, entity_id, entity_name, entity_type):
        mock_rocrate = MagicMock()
        mock_rocrate.path = rocrate_path
        mock_rocrate.source = source_path

        mock_entity = MagicMock()
        mock_entity.id = entity_id
        mock_entity.name = entity_name
        mock_entity.type = entity_type.value
        mock_entity.properties = json.dumps({"key": "value"})

        return Artifact(mock_rocrate, mock_entity)

    return _create_mock_artifact

@pytest.fixture
def null_artifact():
    return Artifact(None, None)

@pytest.fixture
def mock_artifact(create_mock_artifact):
    return create_mock_artifact(
        rocrate_path="/path/to/rocrate",
        source_path="/source/path",
        entity_id="artifact.txt",
        entity_name="Test Artifact",
        entity_type=EntityType.FILE
    )

@pytest.fixture
def mock_artifact_two(create_mock_artifact):
    return create_mock_artifact(
        rocrate_path="/path/to/rocrate_two",
        source_path="/source/path_two",
        entity_id="artifact_two.txt",
        entity_name="Test Artifact Two",
        entity_type=EntityType.FILE
    )

@pytest.fixture
def mock_artifacts(create_mock_artifact):
    """Fixture that creates a list of mock artifacts with different types."""
    mock_one = create_mock_artifact(
            rocrate_path="/path/to/rocrate",
            source_path="/source/path",
            entity_id="artifact.txt",
            entity_name="Test Artifact",
            entity_type=EntityType.FILE
        )
    mock_two = create_mock_artifact(
            rocrate_path="/path/to/rocrate",
            source_path="/source/path",
            entity_id="artifact.txt",
            entity_name="Test Artifact Dataset",
            entity_type=EntityType.DATASET
        )
    mock_three = create_mock_artifact(
            rocrate_path="/path/to/rocrate",
            source_path="/source/path",
            entity_id="artifact.txt",
            entity_name="Test Artifact Script",
            entity_type=EntityType.SCRIPT
        )
    mock_four = create_mock_artifact(
            rocrate_path="/path/to/rocrate",
            source_path="/source/path",
            entity_id="artifact.txt",
            entity_name="Test Artifact Workflow",
            entity_type=EntityType.WORKFLOW
        )
    mock_five = create_mock_artifact(
            rocrate_path="/path/to/rocrate",
            source_path="/source/path",
            entity_id="artifact.txt",
            entity_name="Test Artifact Unknown",
            entity_type=EntityType.UNKNOWN
        )
    return [
        mock_one,
        mock_two,
        mock_three,
        mock_four,
        mock_five
    ]

def test_equal(mock_artifact):
    assert mock_artifact.__eq__(mock_artifact)

def test_not_equal(mock_artifact, mock_artifact_two):
    assert not mock_artifact.__eq__(mock_artifact_two)

def test_hash(mock_artifact):
    correct_hash = hash((mock_artifact.rocrate, mock_artifact.entity))
    assert correct_hash == mock_artifact.__hash__()

def test_extract_artifact(mock_artifact, temp_path):
    pseudonym = "artifact_file.txt" 
    artifacts_dir = temp_path 
    temp_path.mkdir()
    
    artifact = {
        "id": "artifact.txt",
        "name": "Test Artifact",
        "type": EntityType.FILE.value,
        "path": "/path/to/rocrate",
        "description": "",
        "pseudonym": pseudonym,
        "version": "1.0",
        "metadata": hash(json.dumps({"key": "value"})), 
        "symbolic_link": str(ARTIFACTS_DIR / pseudonym) 
    }
    assert mock_artifact.extract_artifact() == artifact
    
def test_generate_pseudonym(mock_artifact):
    pseudonym = "artifact_file.txt"
    assert pseudonym == mock_artifact.create_pseudonym()
    
def test_generate_pseudonyms(mock_artifacts):
    pseudonyms = ["artifact_file.txt", "artifact", "artifact_script.txt", "artifact_test_artifact", "artifact.txt"]
    for i, mock_artifact in enumerate(mock_artifacts):
        generated_pseudonym = mock_artifact.create_pseudonym()
        assert generated_pseudonym == pseudonyms[i]
