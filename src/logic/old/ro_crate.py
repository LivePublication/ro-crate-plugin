"""

The plugin shall extract a list of artifacts from the ro-crate-metadata.json file upon detection.

- The plugin shall recgonize and categorize different types of artifacts (e.g. data files, scripts,
  images, etc.) specified within the RO-Crate.
- The plugin shall include relevant metadata for each artifact while maintaining their provenance 
  (e.g. which step they are related to, which workflow they are part of, etc.).

"""
from rocrate.rocrate import ROCrate
from logic.artifact import Artifact
import os

# Data entities primarily exist in their own right as a file or directory (which may by in the RO-Crate Root
# directory or downloadable by URL). All the following information has been taken from the RO-Crate 1.1 Specification.
# The primary purpose for RO-Crate is to gather and describe a set of Data entities in the form of: 
# - Files
# - Directories
# - Web resources

# The data entities can be further described by referencing contextual entities such as persons, organizations and 
# publications.

DATA_ENTITIES = ['File', 'Directory', 'Web resource']

# Contextual entities exist outside the digital spehre (e.g. People, Places) or are conceptual descriptions 
# that primarily exists as meetadata, like GeoCoordinates and ContactPoints.
contextual_entities = ['People']

class ROCrateInstance:
    '''Represents each RO-Crate instants as an object and includes all artifacts associtated with it.'''
    def __init__(self, path):
        self.path = path
        self.rocrate = ROCrate(path)
        self.artifacts = self.extract_artifacts()
        
    def extract_artifacts(self):
        '''Extracts artifacts from the RO-Crate.'''
        artifacts = []
        for entity in self.rocrate.get_entities():
            artifacts.append(Artifact(entity))
        return artifacts
            
            
            
# TODO ask: are we solely looking for workflow-run-crates? or are we looking for any type up to the
# workflow-run-crates
            
ROCRATE_DIR = os.path.join(os.getcwd(), "tests/crates/valid/")
ROCRATE = "workflow-run-crate"
artifacts = ROCrateInstance(os.path.join(ROCRATE_DIR, ROCRATE)).artifacts


for artifact in artifacts:
    print(artifact.pseudonym)
    print(artifact.entity.type)