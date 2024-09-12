from rocrate.rocrate import ROCrate
import os


class ROCrateManager:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if not self.file_path:
            raise ValueError('Please enter a file path.')
        self.crate = ROCrate(self.file_path)

    def get_root_data_entity(self):
        '''Will return the RO-Crate's root data entity, which will always be present.'''
        return self.crate.root_dataset

    def get_metadata(self):
        '''Will return the RO-Crate's Metadata File, which MUST be present.'''
        return self.crate.metadata
    
    def get_preview(self):
        '''Will return the RO-Crate's Website homepage IF it is present.'''
        if self.crate.preview:
            return self.crate.preview
        return None
    
    def get_entities(self):
        '''Will get the RO-Crate's entities.'''
        return self.crate.get_entities()
    
    def get_entity(self, entity_id):
        '''Will get the specified (by ID) RO-Crate entity.'''
        return self.crate.get(entity_id)
    
    def get_files(self):
        '''Data Entities representing files MUST have "File" as the value for @type. File 
        is an RO-Crate alias for: http://schema.org/MediaObject
        The term File here is liberal, and includes "downloadable" resources where
        @id is an absolute URI.'''
        return self.crate.get_by_type('File')
    
    def get_datasets(self):
        '''Data Entities representing directories MUST have "Dataset" for @type. The term
        directory here includes HTTP file listings where @id is an absolute URI, however
        "external" directories SHOULD have a programmatic listing of their content (e.g. 
        another RO-Crate).'''
        return self.crate.get_by_type('Dataset')
    
    def get_images(self):
        return self.crate.get_by_type('Image')
    

def main():
    crate = ROCrateManager(os.path.abspath('python-scripts/src/ro-crates/ro-crate'))
    print()
    print('root data entity')
    print(crate.get_root_data_entity())

    print()
    print('metadata')
    print(crate.get_metadata())

    print()
    print('preview')
    print(crate.get_preview())

    print()
    print('entities')
    print(crate.get_entities())

    print()
    print('files:')
    print(crate.get_files())
    
    print()
    print('datasets:')
    print(crate.get_datasets())


if __name__ == '__main__':
    main()