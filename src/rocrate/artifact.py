"""

The plugin shall parse the metadata of the `ro-crate-metadata.json` file to extract information about the RO-Crate instance.

- The plugin shall validate the type of the RO-Crate against a predefined list of expected types.
- The plugin shall validate the version of the RO-Crate against a predefiend list of expected types.
- The plugin shall notify the user if the RO-Crate type or version is not recognised.

note: use the RO-Crate validator (slack)

This file holds the logic for metadata extractiong and validation of the RO-Crate type and version. It will also notify the 
user of any discrepancies (e.g., unrecognized type or invalid version)

CHECK

"""
# this is essentially the validator (though it just passes them through
# the rocrate-validator package)

import os
import subprocess

# the path to the TEST ro-crate along with their names
ROCRATE_DIR = os.path.join(os.getcwd(), "python-scripts/src/ro-crates")
ROCRATES = ["ro-crate", "ro-crate-with-files", "ro-crate-with-computational-workflow", "ro-crate-with-images", "ro-crate-with-file-author-location", "ro-crate-with-web-resources"]

# the path of the rocrate-validator package
ROCRATE_VALIDATOR_DIR = os.path.join(os.getcwd(), "rocrate-validator")

# Commands available from the rocrate-validator package
INSTALLATION_CMDS = ["poetry", "install"] # install the dependencies
PROFILES = ["poetry", "run", "rocrate-validator", "profiles"] # manage profiles
USAGE = ["poetry", "run", "rocrate-validator", "validate", "<path_to_rocrate>"] # default usage


# Options
DEBUG = ["poetry", "run", "rocrate-validator", "--debug"] # debug
VERSION = ["poetry", "run", "rocrate-validator", "--version", "-v"] # version
ENABLE_INTERACTIVE_MODE = ["poetry", "run", "rocrate-validator", "--no-interactive", "-n"] # enable interactive mode
DISABLE_INTERACTIVE_MODE = ["poetry", "run", "rocrate-validator", "--no-interactive", "-y"] # disable interactive mode
DISABLE_COLOUR = ["poetry", "run", "rocrate-validator", "--disable-color"] # disable coloured output
HELP = ["poetry", "run", "rocrate-validator", "--help"] #help


# TODO make sure the setup is done only once and preferably in the setup.py file
def setup():
    # checking if the directory exists
    if not os.path.isdir(ROCRATE_VALIDATOR_DIR):
        raise FileNotFoundError("The RO-Crate validator package does not exist.")
    
    os.chdir(ROCRATE_VALIDATOR_DIR)
    
    # installing the dependencies for the RO-Crate validator)
    subprocess.run(INSTALLATION_CMDS, check=True)


def get_help():
    '''Prints the help messages from the rocrate-validator package.''' 
    subprocess.run(HELP, check=True)


def validate_rocrate(path_to_rocrate):
    """Validates the rocrate against the rocrate-validator package."""
    # checking if the rocrate's path exists
    # TODO make sure this is the right path or that the right path is provided at all times?
    USAGE[-1] = path_to_rocrate
    subprocess.run(USAGE, check=True)
    

# TODO uncomment the following lines and figure out how to call them when needed
setup()
get_help()

# TODO uncomment the following lines, put them in the tests dir
# def test():
#     for rocrate in ROCRATES:
#         dir_path = os.path.join(ROCRATE_DIR, rocrate)
#         if not os.path.isdir(dir_path):
#             raise FileNotFoundError(f"The directory {dir_path} does not exist.")
#         validate_rocrate(str(dir_path))
        
        
# test()


# TODO validate against all possible types and version + notification to user if not recognised 
# (use the rocrate-validator package for this)

