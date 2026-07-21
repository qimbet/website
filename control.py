import os
from accessories.cadFiles.file_management.blender_snapshots import generateThumbnails

webRoot = os.getcwd()


if __name__ == "__main__":
    print(f"Creating thumbnails from root dir: {webRoot}")
    generateThumbnails(projectRoot=webRoot)
