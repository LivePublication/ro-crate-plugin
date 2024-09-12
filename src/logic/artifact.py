"""

The plugin shall extract a list of artifacts from the ro-crate-metadata.json file upon detection.

- The plugin shall recgonize and categorize different types of artifacts (e.g. data files, scripts,
  images, etc.) specified within the RO-Crate.
- The plugin shall include relevant metadata for each artifact while maintaining their provenance 
  (e.g. which step they are related to, which workflow they are part of, etc.).

""" 


class Artifact:
    def __init__(self, name, path, type, pesudonym, metadata):
        pass