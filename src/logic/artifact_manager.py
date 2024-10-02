# Copyright 2024 victoriahendersonn

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logic.cache_manager import CacheManager, ARTIFACTS_DIR
from pathlib import Path
from enum import Enum
import logging
import os

# Logger to help keep a trace of any events that occur.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EntityType(Enum):
    FILE = str("File")
    DATASET = str("Dataset")  # Also known as directory
    SCRIPT = ["File", "SoftwareSourceCode"]
    WORKFLOW = ["File", "SoftwareSourceCode", "ComputationalWorkflow"]


class Artifact:
    def __init__(self, rocrate, entity):
        self.rocrate = rocrate
        self.entity = entity
    
    def __eq__(self, other):
        return self.rocrate == other.rocrate and self.entity == other.entity 
    
    def __hash__(self):
        return hash((self.rocrate, self.entity)) 
    
    def extract_artifact(self):
        artifact = {
            "id": self.entity.id if hasattr(self.entity, "id") else "",
            "name": self.entity.name if hasattr(self.entity, "name") else "",
            "type": self.entity.type if hasattr(self.entity, "type") else "",
            "path": self.rocrate.path if hasattr(self.rocrate, "path") else "",
            "pseudonym": self.create_pseudonym(),
            "version": "1.0",
            # "provenance:": None,
            "metadata": hash(self.entity.properties),  # hash the metadata
            "symbolic_link": self.create_symlink(self.entity.id, Path.joinpath(self.rocrate.source, self.entity.id))
        }
        return artifact
    
    def create_symlink(self, id, original_path) -> str | None:
        """
        Creates a symbolic link for the entity from the original path to a symbolic path.
        """
        logger.info(f"Creating symbolic link for entity: {id}")
        symlink_path = Path.joinpath(ARTIFACTS_DIR, self.create_pseudonym())

        try:
            if os.path.islink(symlink_path):
                current_target = os.readlink(symlink_path)
                if current_target == original_path:
                    logger.info(f"Symlink already exists and points to the correct target: {symlink_path} -> {original_path}. Skipping re-creation.")
                    return
                else:
                    logger.info(f"Symlink {symlink_path} points to a different target. Removing it.")
                    os.remove(symlink_path)
            elif os.path.exists(symlink_path):
                logger.info(f"Path {symlink_path} exists but is not a symlink. Removing it.")
                os.remove(symlink_path)

            logger.info(f"Creating symlink from {original_path} to {symlink_path}.")
            os.symlink(original_path, symlink_path)
            return str(symlink_path)
        except OSError as error:
            logger.error(f"Error: {error} encountered when creating a symlink from {original_path} to {symlink_path}.")
            return None
    
    def create_pseudonym(self) -> str:
        """
        Creates a pseudonym for the artifact based on it's properties.
        """
        logger.info("Creating a pseudonym for the artifact.")
        
        entity_id = self.entity.id
        entity_type = str(self.entity.type)
        description = self.entity.get("description", "").lower().replace(" ", "_")[:20]
        name = self.entity.get("name", "")

        try:
            filename, ext = entity_id.rsplit('.', 1)
        except ValueError:
            filename = entity_id
            ext = ""

        if entity_type == EntityType.FILE.value:
            pseudonym = filename + "_file" + ext
        elif entity_type == EntityType.SCRIPT.value:
            pseudonym = filename + "_script" + ext
        elif entity_type == EntityType.DATASET.value:
            pseudonym = filename.rstrip("/")  # If it's a directory or dataset, remove the trailing slash
        else:
            if description:
                pseudonym = description + "_" + filename
            pseudonym = entity_id.replace("/", "_")  # TODO: clean entity id?
        return pseudonym
    
    def resolve_symlink(self, pseudonym) -> str | None:
        """
        Resolves the symbolic link for the given pseudonyn.
        
        params:
            pseudonym: str - the pseudonym of the artifact to resolve the symlink for.
        returns:
            str - the path of the symbolic link or None if the symlink does not exist.
        """
        symlink_path = ARTIFACTS_DIR.joinpath(pseudonym)
        logger.info(f"Resolving symlink for artifact: {pseudonym}")
        
        try:
            if os.path.islink(symlink_path):
                return os.readlink(symlink_path)
            logger.warning("No symlink found for artifact: {pseudonym}.")
            return None
        except Exception as error:
            logger.error(f"Failed to resolve symlink for artifact {pseudonym}: {error}.")
            return None
