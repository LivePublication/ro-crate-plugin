"""

The plugin shall parse the metadata of the `ro-crate-metadata.json` file to extract 
information about the RO-Crate instance.

- The plugin shall validate the type of the RO-Crate against a predefined list of
  expected types.
- The plugin shall validate the version of the RO-Crate against a predefiend list of
  expected types.
- The plugin shall notify the user if the RO-Crate type or version is not recognised

note: use the RO-Crate validator (slack)

This file holds the logic for metadata extractiong and validation of the RO-Crate type
and version. It will also notify the user of any discrepancies (e.g., unrecognized type
or invalid version)

CHECK

"""
import os
import subprocess

INSTALLATION_DIR = os.path.join(os.getcwd(), "rocrate-validator")
INSTALLATION_CMD = ["poetry", "install"]
USAGE = ["poetry", "run", "rocrate-validator", "<path_to_rocrate>"]
HELP = ["poetry", "run", "rocrate-validator", "--help"]

# this is essentially the validator (though it just passes them through
# the rocrate-validator package)

def setup():
    # checking if the directory exists
    if not os.path.isdir(INSTALLATION_DIR):
        raise FileNotFoundError("The RO-Crate validator package does not exist.")
    
    os.chdir(INSTALLATION_DIR)
    os.system("pwd")
    
    # installing the dependencies for the RO-Crate validator)
    subprocess.run(["poetry", "install"], check=True)
    
setup()


