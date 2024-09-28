import os
import logging
from rocrate.rocrate import ROCrate
from pathlib import Path
from logic.scanner import scanner
from logic.validator import Validator
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

class ROCratesManager():
    def __init__(self):
        self.validator = None
        self.setup_done = False
        
        if not os.path.exists(ROCRATE_DATA_DIR):
            os.makedirs(ROCRATE_DATA_DIR)
            os.makedirs(ARTIFACTS_DIR)

    def save_data_to_json(self, data, filename):
        logger.info(f"Saving data to {filename}.")
        file_path = ROCRATE_DATA_DIR / filename
        
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as error:
            logger.error(f"Error: {error}")
    
    def load_data_from_json(self, filename):
        logger.info(f"Loading data from {filename}.")
        file_path = ROCRATE_DATA_DIR / filename

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
        logger.info("Storing RO-Crates to the cache.")

        if not self.validator:
            raise RuntimeError("Validator not set up. Call setup() first.")
        
        # The data to be stored to the rocrate_data.json file #TODO: change to ro_crate_data.json
        rocrate_data = {
            "version": "1.0", # TODO: update the version of the cache when needed (in the update function)
            "rocrates": []
        }
        
        rocrates = []

        # Go through all valid rocrates found and store them in the cache.
        for path in self.validator.valid_rocrates:
            # Create the RO-Crate instance from the path
            rocrate = ROCrate(path)
            
            # Need to extract the current RO-Crate's metadata to store it so, create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")

            try:
                rocrates.append({ 
                    "uuid": str(uuid.uuid4()),
                    "path": str(path),
                    "metadata": self.hash_file(str(metadata_file_path)),
                    "artifacts": self.extract_artifacts(rocrate), # TODO: extract the artifacts from the RO-Crate
                    "valid": True
                })
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")
        
        
        for path in self.validator.invalid_rocrates:
            # Need to extract the current RO-Crate's metadata to store it so,
            # create a path to the metadata file
            metadata_file_path = Path.joinpath(Path(path), "ro-crate-metadata.json")

            try: 
                rocrates.append({ 
                    "uuid": str(uuid.uuid4()),
                    "path": str(path),
                    "metadata": self.hash_file(str(metadata_file_path)),
                    "artifacts": None,
                    "valid": False
                })
            except Exception as error:
                logger.error(f"Error reading metadata for {path}: {error}")

        rocrate_data["rocrates"] = rocrates
        # saving the data to a json file
        self.save_data_to_json(rocrate_data, "rocrate_data.json") # TODO: check for previous versions of the rocrate data ?

                
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
        
    def hash(self, data):
        return hashlib.sha256(data).hexdigest()
        
    def extract_artifacts(self, rocrate):
        artifacts = []
        entities = rocrate.data_entities
        for entity in entities:
            logger.info(f'Creating symbolic link for entity: {entity.id}')
            self.create_symlink(Path.joinpath(rocrate.source, entity.id), Path.joinpath(ARTIFACTS_DIR, entity.id))
            
            #TODO: research into the need of the sym link
            #TODO: research into what artifacts need in their storage
            #TODO: when do we need to use the symb link
            #TODO: AC's around the artifacts?
            #TODO: what do we need stored/hashed in the cahce?
            
            print(entity.properties)
            
            artifacts.append({
                "id": entity.id if hasattr(entity, "id") else "",
                "name": entity.name if hasattr(entity, "name") else "",
                "type": entity.type if hasattr(entity, "type") else "",
                "path": rocrate.path if hasattr(rocrate, "path") else "", # change
                "pseudonym": str(self.create_pseudonym(entity)),
                "version": "1.0",
                "provenance:": "",
                "metadata": hash(entity.properties), # hash the metadata
                #"symbolic_link": str(Path.joinpath(rocrate.source, entity.id)), # create a symbolic link to the file
            })
        return artifacts
    
    def clean_string(self, string):
        """Clean the entity name by removing unwanted characters."""
        # Remove any unwanted characters (e.g., special characters, trailing numbers)
        cleaned_name = re.sub(r'[^a-zA-Z0-9 _-]', '', string)
        cleaned_name = re.sub(r'[-_]+', '-', cleaned_name)  # Replace multiple dashes/underscores with a single dash
        return cleaned_name.strip()  # Remove leading/trailing whitespace
    
    def create_pseudonym(self, entity):
        file = "File"
        dataset = "Dataset" # also known as directory
        script = ["File", "SoftwareSourceCode"] 
        workflow = ["File", "SoftwareSourceCode", "ComputationalWorkflow"]
        entity_type = None 
        
        if (entity.type == file) | (entity.type == [file]):
            entity_type = "file"
        elif (entity.type == dataset) | (entity.type == [dataset]):
            entity_type = "dataset"
        elif (entity.type == script):
            entity_type = "script"
        elif (entity.type == workflow):
            entity_type = "workflow"
        elif isinstance(entity.type, list):  # Handle list types
            entity_type = "_".join([str(typ).lower() for typ in entity.type])  # Join types into a readable format
        else:
            entity_type = "unknown"  # Fallback for unknown types
        
        # 1. Check if the entity has a name attribute
        if hasattr(entity, "name") and entity.name:
            pseudonym = str(self.clean_string(entity.name)) + "_" + str(entity_type)
        # 2. If the entity does not have a name attribute, fall back to the description
        elif hasattr(entity, "description") and entity.description:
            pseudonym = str(self.clean_string(entity.description[:20])) + "_" + str(entity_type)
        # 3. If the entity does not have a description, fall back to the ID
        else:
            pseudonym = str(self.clean_string(entity.id)) + "_" + str(entity_type)
        
        # TODO: ensure uniqueness of the pseudonym, maybe add a hash to the end of the pseudonym?
        # pesudoym = pseudonym + "_" + hash(entity) ?
        return pseudonym
    
    def create_symlink(self, original_path, symlink_path):
        try:
            logger.info(f"Creating symlink from {original_path} to {symlink_path}.")
            os.symlink(original_path, symlink_path)
        except OSError as error:
            logger.error(f"Error creating symlink: {error}")
            
    def load_artifacts(self):
        result = []
        for artifact in ARTIFACTS_DIR.iterdir():
            result.append(artifact)
        return result


if __name__ == "__main__":
    # setup stages
    manager = ROCratesManager()
    manager.setup()
    manager.store_rocrates()
    
    # noticing changes
    manager.load_data_from_json("rocrate_data.json")
    manager.print_data()
    print(manager.load_artifacts())
    
    # TODO
    # - extract the data entities from the RO-Crate
    # - store the data entitites in the cache
    # - hash the ro-crate-metadata.json file (for easy comparison)