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
The plugin shall parse the metadata of the `ro-crate-metadata.json` file to extract information about the RO-Crate instance.

- The plugin shall validate the type of the RO-Crate against a predefined list of expected types.
- The plugin shall validate the version of the RO-Crate against a predefiend list of expected types.
- The plugin shall notify the user if the RO-Crate type or version is not recognised.

This file holds all logic required for metadata extracting and validation of the RO-Crate objects. It will also notify the user
of any discrepancies (e.g., unrecognized type or invalid version). This is essentially just the validator, as it is using the 
rocrate-validator package.
"""
import os
import subprocess
from enum import Enum
from pathlib import Path
from logic.logger import Logger

# Setting up the logger
logger = Logger(__name__).get_logger()


# Paths and directories needed for the rocrate-validator
ROCRATE_VALIDATOR_DIR = os.path.join(os.getcwd(), "rocrate-validator")


# Commands for the rocrate-validator package
class ValidatorCommand(Enum):
    INSTALL_DEPENDENCIES = ["poetry", "install"]  # install the dependencies
    VALIDATE = [
        "poetry",
        "run",
        "rocrate-validator",
        "validate",
    ]  # validate the rocrate
    HELP = [
        "poetry",
        "run",
        "rocrate-validator",
        "--help",
    ]  # get help message from the rocrate-validator
    PROFILES = ["poetry", "run", "rocrate-validator", "profiles"]  # manage profiles
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


class Validator:
    def __init__(self):
        self.valid_rocrates = []  # list of valid rocrates, their paths are stored.
        self.invalid_rocrates = []  # list of invalid rocrates, their paths are stored.

        # Set up the RO-Crate validator when the Validator is initialized.
        self.setup()

    def setup(self):
        """
        Sets up the RO-Crate validator by installing any dependencies needed for the package.
        """
        logger.info("Setting up the RO-Crate validator.")

        # Check if the RO-Crate validator package exists
        if not os.path.isdir(ROCRATE_VALIDATOR_DIR):
            raise FileNotFoundError("The RO-Crate validator package does not exist.")

        # Install dependencies for the RO-Crate validator
        os.chdir(ROCRATE_VALIDATOR_DIR)
        logger.info("Installing depdencies for the RO-Crate validator.")
        subprocess.run(ValidatorCommand.INSTALL_DEPENDENCIES.value, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    def get_help(self):
        # TODO: ask - do we need this? it might be better to have it in the README as this is currently not helpful for the user.
        """Prints the help messages from the rocrate-validator package."""
        logger.info("Printing the help messages from the RO-Crate validator.")
        subprocess.run(ValidatorCommand.HELP.value, check=True, 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,)

    def validate_rocrate(self, path_to_rocrate):
        """Validates the rocrate against the rocrate-validator package."""
        if not isinstance(path_to_rocrate, str) or not Path(path_to_rocrate).exists():
            raise FileNotFoundError(f"The path {path_to_rocrate} does not exist.")

        logger.info(f"Validating the RO-Crate {path_to_rocrate}.")

        result = subprocess.run(
            ValidatorCommand.VALIDATE.value + [path_to_rocrate],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode == 0:
            logger.info(f"The RO-Crate {path_to_rocrate} is valid.")
            self.valid_rocrates.append(path_to_rocrate)
        else:
            # TODO: give the user a reason as to why the RO-Crate is invalid, so they could fix it.
            logger.warning(f"The RO-Crate at {path_to_rocrate} is invalid.")
            self.invalid_rocrates.append(path_to_rocrate)
