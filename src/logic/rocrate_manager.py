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

"""
This file holds all required logic for managing RO-Crates, including storing,
updating, and loading them from the cache. It also handles the extraction of 
artifacts from these RO-Crates.
"""
import os
import logging
from enum import Enum
from rocrate.rocrate import ROCrate
from pathlib import Path
from logic.scanner import scanner
from logic.validator import Validator
from logic.cache_manager import CacheManager
from logic.artifact_manager import Artifact
import platformdirs
import re
import json
import uuid
import hashlib

# Logger to help keep a trace of any events that occur.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Paths and directories for storing the cache.
USER_CACHE_DIR = Path(platformdirs.user_cache_dir())
ROCRATE_DATA_DIR = Path.joinpath(USER_CACHE_DIR, "rocrate-cache")
ARTIFACTS_DIR = Path.joinpath(USER_CACHE_DIR, "rocrate-cache/artifacts")


class ROCratesManager:
    def __init__(self, directory=os.getcwd()):
        self.cache_manager = CacheManager()
        self.validator = None
        self.setup_done = False
        self.directory = directory  # TODO: Change the directory to the current working directory of the document.

        # Set up the validator when the ROCratesManager is instantiated.
        self.setup()

    def setup(self):
        """
        Sets up the RO-Crate manager by scanning the directory for RO-Crates and validating them through
        the rocrate-validator package.
        """
        if not self.setup_done:
            try:
                # TODO: get the current working directory from the plugin, this has been created as an issue in Stencila's GitHub repository.
                paths = scanner(self.directory)
                self.validator = Validator()

                # Go through all found RO-Crates and validate them using the rocrate-validator
                for path in paths:
                    self.validator.validate_rocrate(path)

                # Store the RO-Crates and their corresponding artifacts to the user cache
                self.store_rocrates()
            except Exception as error:
                logger.error(f"Error encountered during setup: {error}")
                raise

    def store_rocrates(self, version=1):
        if not self.validator:
            raise RuntimeError("Validator not set up. Call setup() first.")

        logger.info("Storing RO-Crates and their corresponding artifacts to the user cache.")
        rocrate_data = { "version": str(version), "rocrates": [] }

        # Go through all valid rocrates found and store them in the cache.
        for path in self.validator.valid_rocrates:
            # Create the RO-Crate instance from the path
            rocrate = ROCrate(path)

            # Need to extract the current RO-Crate's metadata to store it so, create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")

            try:
                rocrate_info = self.make_rocrate_info(path, metadata_file_path, rocrate)
                rocrate_data["rocrates"].append(rocrate_info)
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")

        for path in self.validator.invalid_rocrates:
            # Need to extract the current RO-Crate's metadata to store it so, # create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")

            try:
                rocrate_info = self.make_rocrate_info(path, metadata_file_path, None)
                rocrate_data["rocrates"].append(rocrate_info)
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")

        # Saving the data to a json file
        self.cache_manager.save_data_to_json(rocrate_data)

    def update(self):
        if self.validator is None:
            logger.error("Validator has not been set up, call setup() first.")
            raise RuntimeError("Validator has not been set up, call setup() first.")

        logger.info("Updating the cache with the latest RO-Crates.")

        # Load the previous cache data
        try:
            previous_cache = self.cache_manager.load_data_from_json()
        except FileNotFoundError:
            logger.error("No previous cache found, no need to update.")
            return
        except Exception as error:
            logger.error(f"Error loading previous cache: {error}")
            return

        # Scan for new RO-Crates
        current_paths = scanner(self.directory)
        rocrate_data = { "version": str(int(previous_cache["version"]) + 1), "rocrates": [] }
        previous_rocrates = { rocrate["path"]: rocrate for rocrate in previous_cache["rocrates"] }

        # Go through all found RO-Crates and validate them using the rocrate-validator
        self.validator.valid_rocrates.clear()
        self.validator.invalid_rocrates.clear()
        self.cache_manager.clear_cache()
        for path in current_paths:
            self.validator.validate_rocrate(path)

        # Handle valid RO-Crates
        for path in self.validator.valid_rocrates:
            # Create the RO-Crate instance from the path
            rocrate = ROCrate(path)
            
            # Need to extract the current RO-Crate's metadata to store it so, create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")
            metadata_hash = self.hash_file(str(metadata_file_path))

            # A valid RO-Crate has been found that was previously in the cache
            if path in previous_rocrates:
                old_rocrate = previous_rocrates[path]
                
                # If it was previously valid and is still valid, keep it in the cache as long as it is 
                # still the same rocrate
                if old_rocrate["valid"] and old_rocrate["metadata"] == metadata_hash:
                    logger.info(f"RO-Crate at {path} is still valid but it's contents have not changed.")

                # If it was previously invalid and is now valid, update the cache as long as it is
                # still the same rocrate, this case should not happen but it is handled here in case it does.
                elif not old_rocrate["valid"] and old_rocrate["metadata"] == metadata_hash:
                    logger.info(f"RO-Crate at {path} is now valid but it's contents have not changed.")

                # If it was previously valid and is still valid, but not the same rocrate, update it
                elif old_rocrate["valid"] and old_rocrate["metadata"] != metadata_hash:
                    logger.info(f"RO-Crate at {path} is still valid but it's contents have changed.")
                
                # If it was previously invalid and is now valid, but not the same rocrate, update it
                elif not old_rocrate["valid"] and old_rocrate["metadata"] != metadata_hash:
                    logger.info(f"RO-Crate at {path} is now valid and it's contents have changed.")

                # Ideally, this case should not happen, but it is handled here just in case it does.
                else:
                    logger.warning(f"Unexpected state for RO-Crate at {path}, potential logic issue.")
                    logger.info(f"RO-Crate at {path} is valid.")
                
                updated_rocrate = self.make_rocrate_info(path, metadata_file_path, rocrate)
                rocrate_data["rocrates"].append(updated_rocrate)
            
            # New valid RO-Crate
            else:
                logger.info(f"New RO-Crate has been found at {path}, saving it to cache.")
                new_rocrate = self.make_rocrate_info(path, metadata_file_path, rocrate)
                rocrate_data["rocrates"].append(new_rocrate)

        # Handle invalid RO-Crates
        for path in self.validator.invalid_rocrates:
            
            # Need to extract the current RO-Crate's metadata to store it so, create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")
            metadata_hash = self.hash_file(str(metadata_file_path))

            # An invalid RO-Crate has been found that was previously in the cache
            if path in previous_rocrates:
                old_rocrate = previous_rocrates[path]
                
                # If it was previously invalid and is still invalid, keep it in the cache as long as it is
                # still the same rocrate
                if not old_rocrate["valid"] and old_rocrate["metadata"] == metadata_hash:
                    logger.info(f"RO-Crate at {path} is still invalid but it's contents have not changed.")
                    rocrate_data["rocrates"].append(old_rocrate)
                
                # If it was previously valid and is now invalid, update the cache as long as it is 
                # still the same rocrate, this case should not happen but it is handled here in case it does.
                elif old_rocrate["valid"] and old_rocrate["metadata"] == metadata_hash:
                    logger.warning(f"RO-Crate at {path} is now invalid but it's contents have not changed.")
                    updated_rocrate = self.make_rocrate_info(path, metadata_file_path, None)
                    rocrate_data["rocrates"].append(old_rocrate)
                
                # If it was previously invalid and is still invalid, but not the same rocrate, update it
                elif not old_rocrate["valid"] and old_rocrate["metadata"] != metadata_hash:
                    logger.info(f"RO-Crate at {path} is still invalid but it's contents have changed.")
                    updated_rocrate = self.make_rocrate_info(path, metadata_file_path, None)
                    rocrate_data["rocrates"].append(updated_rocrate)
                
                # If it was previously valid and is now invalid, but not the same rocrate, update it and
                # store it in the cache
                elif old_rocrate["valid"] and old_rocrate["metadata"] != metadata_hash:
                    logger.warning(f"RO-Crate at {path} is now invalid and it's contents have changed.")
                    updated_rocrate = self.make_rocrate_info(path, metadata_file_path, None)
                    rocrate_data["rocrates"].append(updated_rocrate)
                
                # Ideally, this case should not happen, but it is handled here just in case it does.
                else:
                    logger.warning(f"Unexpected state for RO-Crate at {path}, potential logic issue.")
                    logger.info(f"RO-Crate at {path} is invalid.")
                    updated_rocrate = self.make_rocrate_info(path, metadata_file_path, None)
                    rocrate_data["rocrates"].append(updated_rocrate)
                    
            # A new invalid RO-Crate has been found
            else:
                logger.warning(f"New invalid RO-Crate has been found at {path}, saving it to the cache.")
                updated_rocrate = self.make_rocrate_info(path, metadata_file_path, None)
                rocrate_data["rocrates"].append(updated_rocrate)

        self.cache_manager.save_data_to_json(rocrate_data)
        logger.info("The RO-Crate cache has been updated successfully.")

    def hash_file(self, path):
        cwd = Path(os.getcwd())
        file_path = cwd / path
        file_content = None

        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            return hashlib.sha256(file_content).hexdigest()
        except Exception as e:
            logger.error(f"RO-Crate {path} cannot be hashed")
            return file_content

    def extract_artifacts(self, rocrate):
        """
        Extracts artifacts from the RO-Crate and stores them in the cache
        """
        artifacts = []
        entities = rocrate.data_entities
        for entity in entities:
            artifact = Artifact(rocrate, entity)
            artifacts.append(artifact.extract_artifact())
        return artifacts

    def load_artifacts(self):
        return self.cache_manager.load_cache()
    
    def make_rocrate_info(self, rocrate_path, metadata_file_path, rocrate=None):
        info = {
            "uuid": str(uuid.uuid4()),
            "path": str(rocrate_path),
            "metadata": self.hash_file(str(metadata_file_path)),
            "artifacts": self.extract_artifacts(rocrate) if rocrate else None,
            "valid": True if rocrate else False,
        }
        return info


if __name__ == "__main__":
    # setup stages
    manager = ROCratesManager()
    #manager.cache_manager.load_data_from_json()
    manager.update()
