"""

The plugin shall extract a list of artifacts from the ro-crate-metadata.json file upon detection, 
in this case it will occur after validation.

- The plugin shall recgonize and categorize different types of artifacts (e.g. data files, scripts,
  images, etc.) specified within the RO-Crate.
- The plugin shall include relevant metadata for each artifact while maintaining their provenance 
  (e.g. which step they are related to, which workflow they are part of, etc.).

"""
# TODO
# - ask: is there any difference between an entity and an artifact (AC)?
# - ask: what artifact types should be recognized? so far it's just data files, scripts, and images (AC)


# Artifact Types


# Data Entities:
DATA_ENTITY = ['File', 'Directory', 'Web resource']

# A File Data Entity MUST have
# - @type: MUST be 'File', or an array where 'File' is one of the values.
FILE_TYPE = 'File' # e.g. raw data, processed data, or any file representing research data.

# A Dataset (directory) Data Entity MUST have
# - @type: MUST be 'Dataset', or an array where 'Dataset' is one of the values.
DIRECTORY_TYPE = 'Dataset'

# TODO: Web resource Data Entity


# Workflows and Scripts: 

# A script is a Data Entity which MUST have
# - @type: array with at least File, and SoftwareSourceCode
SCRIPT = ['File', 'SoftwareSourceCode']

# A workflow is Data Entity which MUST have 
# - @type: array with at least File, SoftwareSourceCode, and ComputationalWorkflow
WORKFLOW_TYPE = ['File', 'SoftwareSourceCode', 'ComputationalWorkflow'] 

# TODO contextual entities

IMAGE = '' # e.g. visual representations like figures, charts, or photos
DOCUMENT = '' # e.g. papers, reports, or any text-based documents 


# TODO ask: what do artifacts need to comprise of?

class Artifact:
    def __init__(self, entity):
        self.pseudonym = ''
        self.entity = entity