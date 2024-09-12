"""

The plugin shall extract a list of artifacts from the ro-crate-metadata.json file upon detection.

- The plugin shall recgonize and categorize different types of artifacts (e.g. data files, scripts,
  images, etc.) specified within the RO-Crate.
- The plugin shall include relevant metadata for each artifact while maintaining their provenance 
  (e.g. which step they are related to, which workflow they are part of, etc.).

"""
from rocrate.rocrate import ROCrate


class ROCrateInstance:
    '''Represents each RO-Crate instants as an object and includes all artifacts associtated with it.'''
    def __init__(self, path):
        self.path = path
        self.rocrate = ROCrate(path)
        self.artifacts = self.extract_artifacts()
        
    def extract_artifacts(self):
        '''Extracts artifacts from the RO-Crate.'''
        pass
    

