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
