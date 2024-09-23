import os
import logging
from rocrate.rocrate import ROCrate
from pathlib import Path
from logic.scanner import scanner
from logic.validator import Validator
import platformdirs
import json
import uuid
import hashlib

# Logger to help keep a trace of any events that occur.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ROCratesManager():
    def __init__(self):
        self.file_cache = {}
        self.validator = None
        self.setup_done = False

    def save_data_to_json(self, data, filename):
        # TODO: put it into plugin's own folder?
        logger.info(f"Saving data to {filename}.")
        
        user_cache_dir = Path(platformdirs.user_cache_dir())
        file_path = user_cache_dir / filename
        
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            logger.error(f"Error: {error}")
    
    def load_data_from_json(self, filename):
        # TODO: put it into plugin's own folder?
        logger.info(f"Loading data from {filename}.")
        
        user_cache_dir = Path(platformdirs.user_cache_dir())
        file_path = user_cache_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as error:
            logger.error(f"Error: {error}, encounted whilst loading cached JSON file.")

    def setup(self):
        if not self.setup_done:
            try: 
                # TODO: get the cwd of the document from the plugin - talk to Nokome about this!
                paths = scanner(os.getcwd())
                self.validator = Validator()
                self.validator.setup()
                
                # Go through all found RO-Crates and validate them using the rocrate-validator
                for path in paths:
                    self.validator.validate_rocrate(path)
            except Exception as error:
                logger.error(f"Error during setup: {error}")
                raise
    
    def store_rocrates(self):
        logger.info("Storing RO-Crates in users' rocrate_data.json")

        if not self.validator:
            raise RuntimeError("Validator not set up. Call setup() first.")
        
        # The data to be stored to the rocrate_data.json file #TODO: change to ro_crate_data.json
        data = {
            "ro_crates": [],
            "version": 1 # TODO: update the version of the cache when needed (in the update function)
        }
        
        ro_crates = []
        print(self.validator.invalid_rocrates)

        # Go through all valid ro 
        for path in self.validator.valid_rocrates:
            # Create the RO-Crate instance from the path
            rocrate = ROCrate(path)
            
            # Need to extract the current RO-Crate's metadata to store it so,
            # create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")
            print(f"metadata file path: {metadata_file_path}")

            try: 
                with open(metadata_file_path, "r") as f:
                    metadata = json.load(f)
                     
                ro_crates.append({ 
                    "uuid": str(uuid.uuid4()),
                    "path": str(path),
                    "metadata": metadata,  # TODO: hash the metadata for comparison
                    "artifacts": str(rocrate.data_entities), # TODO: extract the artifacts from the RO-Crate
                    "valid": True
                })
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")
        
        
        for path in self.validator.invalid_rocrates:
            # Need to extract the current RO-Crate's metadata to store it so,
            # create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")

            try: 
                with open(metadata_file_path, "r") as f:
                    metadata = json.load(f)
     
                ro_crates.append({ 
                    "uuid": str(uuid.uuid4()),
                    "path": str(path),
                    "metadata": metadata,
                    "artifacts": None,
                    "valid": False
                })
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")

        data["ro_crates"] = ro_crates
        # saving the data to a json file
        self.save_data_to_json(data, "rocrate_data.json") # TODO: check for previous versions of the rocrate data ?

                
    def update(self):
        if self.validator is None:
            raise RuntimeError("Validator has not been set up, call setup() first.")
        
        # TODO: get the cwd of the document from the plugin - talk to Nokome about this!
        paths = scanner(os.getcwd())
        
        # Go through all found RO-Crates and validate them using the rocrate-validator
        for path in paths:
            self.validator.validate_rocrate(path)

        # Go through all valid rocrates found and see if they're identical to the ones in the
        # previous cache
        for path in self.validator.valid_rocrates:
            rocrate = ROCrate(path)
            
            if self.validator.valid_rocrates[path] == rocrate:
                logger.info(f"RO-Crate {path} has not changed.")
            else:
                logger.info(f"RO-Crate {path} has changed.")
                self.validator.valid_rocrates[path] = rocrate

        # Go through all invalid rocrates found and see if they're identical to the ones in the 
        # previous cache
        for rocrate in self.validator.invalid_rocrates:
            # if self.validator.invalid_rocrates[path] == rocrate:
            #     logger.info(f"RO-Crate {path} ")
                
            logger.info(f'')
                
        # TODO: what about the case where rocrates are nowww valid??? or is this part of the linking strat. 
        # how about update the version of the cache ?  
    
    def print_data(self):
        logger.info(f"Printing ROCrate data from cache.")
        try:
            data = self.load_data_from_json("rocrate_data.json")
            print(json.dumps(data, indent=4))
        except Exception as error:
            logger.error(f"Error printing data: {error}")

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

# TODO: ensure this setup happens once the plugin opens
# TODO: ensure an easy way to access the data from the JSON file
# TODO: maybe make the validator more accessible? - not just a hard setup..
    
# - ensure setup happens only once by using a class to manage the setup state and validator 
# - handle file paths more robustly (use os.path.join() or pathlib.Path) to handle cross-platform compatability
# - improve logging and error handling (add more detailed error messages and handle portential exceptions more gracefully)
# - optimize data loading and saving (minimize repeated operations and make data handling more efficient)
# - refactor for readability - separate concerns into functions or methods to make the code more readable and maintainable
 
# TODO: extract data entities from the RO-Crate and store them accordingly
# - look at ACs again
# Is there any better way to store the RO-Crates? - potentially in a database? i'm not sure what's good w/ python
# as for the cached data, how do i ensure that the data is up to data - if it has changed i need to create a new 
# potential cache file so that i can determine if any of the rocrates have been updated or whatever... symbolic linking.

if __name__ == "__main__":
    manager = ROCratesManager()
    manager.setup()
    manager.store_rocrates()
    manager.load_data_from_json("rocrate_data.json")
    manager.print_data()
    
    # TODO
    # - extract the data entities from the RO-Crate
    # - store the data entitites in the cache
    # - hash the ro-crate-metadata.json file (for easy comparison)