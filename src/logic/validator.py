"""

The plugin shall parse the metadata of the `ro-crate-metadata.json` file to extract information about the RO-Crate instance.

- The plugin shall validate the type of the RO-Crate against a predefined list of expected types.
- The plugin shall validate the version of the RO-Crate against a predefiend list of expected types.
- The plugin shall notify the user if the RO-Crate type or version is not recognised.

note: use the RO-Crate validator (Slack)

This file holds the logic for metadata extractiong and validation of the RO-Crate type and version. It will also notify the 
user of any discrepancies (e.g., unrecognized type or invalid version)

CHECK

"""

# this is essentially the validator (though it just passes them through
# the rocrate-validator package)

import os
import subprocess
import rocrate.rocrate as rocrate
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Paths and directories
# the path to the TEST ro-crates along with their corresponding names
ROCRATE_DIR = os.path.join(os.getcwd(), "python-scripts/src/ro-crates")
ROCRATES = [
    "ro-crate",
    "ro-crate-invalid",
    "ro-crate-with-files",
    "ro-crate-with-computational-workflow",
    "ro-crate-with-images",
    "ro-crate-with-file-author-location",
    "ro-crate-with-web-resources",
]

# the path of the rocrate-validator package
ROCRATE_VALIDATOR_DIR = os.path.join(os.getcwd(), "rocrate-validator")

# Commands available from the rocrate-validator package
INSTALLATION_CMDS = ["poetry", "install"]  # install the dependencies
PROFILES = ["poetry", "run", "rocrate-validator", "profiles"]  # manage profiles
USAGE = [
    "poetry",
    "run",
    "rocrate-validator",
    "validate",
    "<path_to_rocrate>",
]  # default usage

# Options
DEBUG = ["poetry", "run", "rocrate-validator", "--debug"]  # debug
VERSION = ["poetry", "run", "rocrate-validator", "--version", "-v"]  # version
ENABLE_INTERACTIVE_MODE = [
    "poetry",
    "run",
    "rocrate-validator",
    "--no-interactive",
    "-n",
]  # enable interactive mode
DISABLE_INTERACTIVE_MODE = [
    "poetry",
    "run",
    "rocrate-validator",
    "--no-interactive",
    "-y",
]  # disable interactive mode
DISABLE_COLOUR = [
    "poetry",
    "run",
    "rocrate-validator",
    "--disable-color",
]  # disable coloured output
HELP = ["poetry", "run", "rocrate-validator", "--help"]  # help

# def setup():
#     # checking if the directory exists
#     if not os.path.isdir(ROCRATE_VALIDATOR_DIR):
#         raise FileNotFoundError("The RO-Crate validator package does not exist.")

#     os.chdir(ROCRATE_VALIDATOR_DIR)

#     # installing the dependencies for the RO-Crate validator)
#     subprocess.run(INSTALLATION_CMDS, check=True)

# def get_help():
#     """Prints the help messages from the rocrate-validator package."""
#     subprocess.run(HELP, check=True)

# def validate_rocrate(path_to_rocrate):
#     """Validates the rocrate against the rocrate-validator package."""
#     if not os.path.exists(path_to_rocrate):
#         raise FileNotFoundError(f"The path {path_to_rocrate} does not exist.")

#     USAGE[-1] = path_to_rocrate
#     result = subprocess.run(USAGE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     USAGE[-1] = "<path_to_rocrate>"

#     if result.returncode == 0:
#         print(f"The RO-Crate {path_to_rocrate} is valid.")
#     else:
#         print(f"The RO-Crate {path_to_rocrate} is invalid.")

# Converting the validator into a validator class!

class Validator:
    def __init__(self):
        self.valid_rocrates = []
        self.invalid_rocrates = []

    def setup(self):
        logger.info("Setting up the RO-Crate validator.")
        
        # checking if the directory exists
        if not os.path.isdir(ROCRATE_VALIDATOR_DIR):
            raise FileNotFoundError("The RO-Crate validator package does not exist.")
        os.chdir(ROCRATE_VALIDATOR_DIR)
        
        # installing the dependencies for the RO-Crate validator)
        logger.info("Installing depdencies for the RO-Crate validator.")
        subprocess.run(INSTALLATION_CMDS, check=True)

    def get_help(self):
        """Prints the help messages from the rocrate-validator package."""
        # TODO: ask - do we need this? it might be better to have it in the README and 
        #       this is not exaclty useful for the users.
        logger.info("Printing the help messages from the RO-Crate validator.")
        subprocess.run(HELP, check=True)

    def validate_rocrate(self, path_to_rocrate):
        """Validates the rocrate against the rocrate-validator package."""
        logger.info(f"Validating the RO-Crate {path_to_rocrate}.")
        
        if not os.path.exists(path_to_rocrate):
            raise FileNotFoundError(f"The path {path_to_rocrate} does not exist.")

        USAGE[-1] = path_to_rocrate
        result = subprocess.run(USAGE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        USAGE[-1] = "<path_to_rocrate>"

        if result.returncode == 0:
            logger.info(f"The RO-Crate {path_to_rocrate} is valid.")
            self.valid_rocrates.append(path_to_rocrate)
        else:
            # TODO: give the user a reason as to why the RO-Crate is invalid, so they could fix it.
            logger.info(f"The RO-Crate {path_to_rocrate} is invalid.")
            self.invalid_rocrates.append(path_to_rocrate)


# # TODO: print what specification the RO-Crate is following
# # potentially be the 'ROCrateEntity' class
# class ValidatedROCrate:
#     def __init__(self, path):
#         self.path = path
#         self.rocrate = rocrate.ROCrate(path)
        
#     def to_dict(self): 
#         return {
#             "path": self.path,
#             "metadata": self.rocrate.metadata,
#         }
        
#     def from_dict(self):
#         pass

# # TODO uncomment the following lines, put them in the tests dir
def test():
    validator = Validator()
    validator.setup()
    
    for rocrate in ROCRATES:
        dir_path = os.path.join(ROCRATE_DIR, rocrate)
        if not os.path.isdir(dir_path):
            raise FileNotFoundError(f"The directory {dir_path} does not exist.")
        validator.validate_rocrate(str(dir_path))
        
    print(validator.valid_rocrates)
    print(validator.invalid_rocrates)

test()
