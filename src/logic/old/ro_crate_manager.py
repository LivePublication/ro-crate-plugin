"""

"""
from rocrate.rocrate import ROCrate
import os

class ROCrateManager:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if not self.file_path:
            raise ValueError('Please enter a file path.')

        metadata_file = os.path.join(self.file_path, 'ro-crate-metadata.json')
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"No RO-Crate metadata file found in {self.file_path}")
        
        try:
            self.crate = ROCrate(self.file_path)
            print(f"RO-Crate detected in {self.file_path}")
        except Exception as e:
            raise ValueError(f"Failed to load RO-Crate: {e}")

    def get_root_data_entity(self):
        '''Returns the RO-Crate's root data entity, which will always be present.'''
        return self.crate.root_dataset

    def get_metadata(self):
        '''Returns the RO-Crate's Metadata File, which MUST be present.'''
        return self.crate.metadata
    
    def get_preview(self):
        '''Returns the RO-Crate's Website homepage IF present.'''
        return self.crate.preview if self.crate.preview else None
    
    def get_entities(self):
        '''Gets the RO-Crate's entities.'''
        return self.crate.get_entities()
    
    def get_entity(self, entity_id):
        '''Gets the specified (by ID) RO-Crate entity.'''
        return self.crate.get(entity_id)
    
    def get_files(self):
        '''Returns Data Entities representing files with @type "File".'''
        return self.crate.get_by_type('File')
    
    def get_datasets(self):
        '''Returns Data Entities representing directories with @type "Dataset".'''
        return self.crate.get_by_type('Dataset')
    
    def get_images(self):
        '''Returns Data Entities representing images.'''
        return self.crate.get_by_type('Image')

    def validate_rocrate(self):
        '''Validates the RO-Crate type and version.'''
        root = self.get_root_data_entity()
        expected_types = ["Dataset"]
        expected_versions = ["1.0", "1.1"]

        # Validate the type
        if root.type not in expected_types:
            raise ValueError(f"Unexpected RO-Crate type: {root.type}")
        
        # Validate the version
        if root["version"] not in expected_versions:
            raise ValueError(f"Unsupported RO-Crate version: {root['version']}")
        print(f"RO-Crate version {root['version']} validated.")
    
    def extract_artifacts(self):
        '''Extracts and categorizes artifacts such as files and images.'''
        files = self.get_files()
        images = self.get_images()

        print("Files:")
        for file in files:
            print(f"- {file.name}")
        
        print("Images:")
        for image in images:
            print(f"- {image.name}")
