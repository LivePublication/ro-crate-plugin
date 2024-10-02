import logging
import os
import platformdirs
import json

from pathlib import Path 


# Logger to help keep a trace of any events that occur.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Paths and directories for storing the cache.
USER_CACHE_DIR = Path(platformdirs.user_cache_dir())
ROCRATE_DATA_DIR = Path.joinpath(USER_CACHE_DIR, "rocrate-cache")
ARTIFACTS_DIR = Path.joinpath(USER_CACHE_DIR, "rocrate-cache/artifacts")
FILENAME = "rocrate_data.json"


class CacheManager():
    def __init__(self):
        # Set up the directories for the cache.
        if not os.path.exists(ROCRATE_DATA_DIR):
            os.makedirs(ROCRATE_DATA_DIR)
            os.makedirs(ARTIFACTS_DIR)
        else:
            self.clear_cache()
    
    def clear_cache(self):
        logger.info("Clearing the cache of any previous symbolic links.")
        try:
            artifacts = os.listdir(ARTIFACTS_DIR)
            for artifact in artifacts:
                artifact_path = os.path.join(ARTIFACTS_DIR, artifact)
                if os.path.islink(artifact_path):
                    os.unlink(artifact_path)
            logger.info("Cache cleared successfully.")
        except OSError:
            logger.error("Error occured when clearing the cache.")
    
    def save_cache(self, artifact):
        pass
    
    def load_cache(self):
        if not os.path.exists(ARTIFACTS_DIR):
            logger.error(f"Error: Artifacts cache has not been set up, there are no artifacts to load.")
            return []
        try:
            return os.listdir(ARTIFACTS_DIR)
        except Exception as error:
            logger.error(f"Error: {error}, encountered when loading the cache.")
            return []
    
    def save_data_to_json(self, data) -> None:
        logger.info(f"Saving data to {FILENAME}.")
        file_path = ROCRATE_DATA_DIR / FILENAME

        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
                logger.info(f"Successfully saved data to {FILENAME}.")
        except Exception as error:
            logger.error(f"Error: {error}, encountered when saving data to JSON file.")

    def load_data_from_json(self):
        file_path = ROCRATE_DATA_DIR / FILENAME
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        try:
            logger.info(f"Loading data from {FILENAME}.")
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as error:
            logger.error(f"Error: {error}, encountered when loading {FILENAME} from the cache.")
            return { "version": "0", "rocrates": [] }

    def print_data_from_json(self) -> None:
        logger.info(f"Printing RO-Crate data from the cache.")
        try:
            data = self.load_data_from_json()
            print(json.dumps(data, indent=4))
        except Exception as error:
            logger.error(f"Error: {error}, encountered when printing data from the cache.")
