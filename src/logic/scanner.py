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
A function to allow the plugin to automatically scan the current directory for the
presence of an RO-Crate instance.

- It shall detect RO-Crate files with the standard file naming conventions 
  (e.g. ro-crate-metadata.json) and load them into memory.
- It shall notify the user when an RO-Crate is detected in the current directory.
- It shall provide an error message if an RO-Crate file is malformed or unreadable.

This file holds the logic for scanning the directory and detecting RO-Crate files. It
also handles the notification to the user when an RO-Crate is detected.
"""
import os
from logic.logger import Logger

# Logger to help keep a trace of any events that occur.
logger = Logger(__name__).get_logger()


def scanner(directory):
    """
    Scans the given `directory` for RO-Crate files, and returns a list of
    these directories as strings.
    """
    if directory is None:
      logger.warning("Error: provided directory is none")
      return []
    logger.info(f"Scanning directory: {directory} for RO-Crate files.")
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "ro-crate-metadata.json":
                paths.append(root)
                logger.info(f"RO-Crate detected in {root}.")
    return paths
