import os
from pathlib import Path
from rocrate.rocrate import ROCrate
from ro_crate_manager import ROCrateManager


def find_ro_crate_files(directory):
    '''Traverses the given directory to find all RO-Crate objects,
    will store them accordingly.'''
    
    ro_crates = {}
    cwd = os.getcwd()
    root_dir = Path(cwd + '/python-scripts/src/' + directory)
    
    if not root_dir.exists():
        print(f"Directory {directory} does not exist.")
        return ro_crates

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "ro-crate-metadata.json":
                try: 
                    crate_manager = ROCrateManager(root)
                    ro_crates[root] = crate_manager
                except Exception as error:
                    print(f"Cannot load RO-Crate from directory: {error}.")
    return ro_crates

    
def main():
    '''Goes through the /data and /ro-crates directory to find all RO-Crates.'''
    print(find_ro_crate_files('data'))
    print(find_ro_crate_files('ro-crates'))
    
if __name__ == "__main__":
    main()
