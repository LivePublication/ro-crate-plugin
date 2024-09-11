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
from pathlib import Path

class ROCrateDirectoryInformation():
    
    def __init__(self, folder):
        self.folder = folder
        self.files = self.get_files()
        self.images = self.get_images()

    def get_files(self):
        # gets the path of the folder to search
        folder_path = Path('src/ro-crates') / self.folder
        files = set()

        if not folder_path.exists():
            print("The folder given does not exist.")
            return files
        
        # searches through the directory to get all files
        for file in folder_path.rglob('*'):
            if file.is_file():
                files.add(file)

        return files

    def get_images(self):
        # a set of possible image extensions.
        image_extensions = { ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".jfif" }

        # set of images present in the searched directory.
        images = {
            file for file in self.files if Path(file).suffix in image_extensions
        }

        return images
    
    def get_images_names(self):
        return { image.name for image in self.images }


def main():
    print(ROCrateDirectoryInformation('ro-crate-with-images').get_images_names())

if __name__ == "__main__":
    main()


# TODO make the scanner scan the entire directory of where you are, then store any folder's path that has an RO-Crate in it
# (e.g. /ro-crate if /ro-crate has "ro-crate-metadata.json" in it then we store that path)