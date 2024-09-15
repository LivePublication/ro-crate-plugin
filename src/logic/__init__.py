import os
import logging
from rocrate.rocrate import ROCrate
from pathlib import Path
from logic.scanner import scanner
from logic.validator import Validator
import platformdirs
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

file_cache = {}

SETUP = False # TODO:: can i ensure that the setup only happens once? but also that i am still in the correct dir
VALIDATOR = None

VALID_ROCRATES = {}
INVALID_ROCRATES = {}

def save_data_to_json(data, filename):
    logger.info(f"Saving data to {filename}.")
    
    user_cache_dir = Path(platformdirs.user_cache_dir())
    file_path = user_cache_dir / filename
    
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as error:
        logger.error(f"Error: {error}")


def load_data_from_json(filename):
    logger.info(f"Loading data from {filename}.")
    
    user_cache_dir = Path(platformdirs.user_cache_dir())
    file_path = user_cache_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    with open(file_path, "r") as f:
        return json.load(f)


def setup():
    # TODO: get the cwd of the document from the plugin - talk to Nokome about this!
    paths = scanner(os.getcwd())
    validator = Validator()

    try:
        validator.setup()
        for path in paths:
            validator.validate_rocrate(path)
    except Exception as error:
        logger.error(f"Error: {error}")

    return validator


def store_rocrates(validator):
    valid_rocrate_data = []
    invalid_rocrate_data = []
    
    for path in validator.valid_rocrates:
        # Create the RO-Crate instance from the path
        rocrate = ROCrate(path)
        # Store the RO-Crate instance inside VALID_ROCRATES for easy access throughout the plugin
        VALID_ROCRATES[path] = rocrate
        
        # Need to extract the current RO-Crate's metadata to store it so,
        # create a path to the metadata file
        metadata_file_path = Path(path) / "ro-crate-metadata.json" # TODO: check this for other operating systems
        
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
        
        # Appending the JSON data to the valid_rocrate_data_list        
        valid_rocrate_data.append({ 
            "path": path,
            "ro-crate-metadata.json": metadata,  
        })
    
    for path in validator.invalid_rocrates:
        INVALID_ROCRATES[path] = None
        invalid_rocrate_data.append({ "path": path })
    
    # creating the data to be saved to the json file
    data = {
        "valid_rocrates": valid_rocrate_data,
        "invalid_rocrates": invalid_rocrate_data,
    }

    # saving the data to a json file
    save_data_to_json(data, "rocrate_data.json")


# TODO: implement an update function that updates the json when needed.
# def update():
#     pass

# TODO: ensure this setup happens once the plugin opens
# TODO: ensure an easy way to access the data from the JSON file
# TODO: maybe make the validator more accessible? - not just a hard setup..
if __name__ == "__main__":
    if VALIDATOR is None:
        VALIDATOR = setup()
        
    store_rocrates(VALIDATOR)
    
    # Load the data
    data = load_data_from_json("rocrate_data.json")
    # TODO: pretty print the data from the JSON file
    print(data)