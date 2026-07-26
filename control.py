import os
from pathlib import Path
from z_controlFuncs import sidebar, sitemanager
#from accessories.cadFiles.file_management.blender_snapshots import generateThumbnails



def create_thumbnails(site):
    print(
        f"Creating thumbnails from root dir: {site.site_root}"
    )

    print("Under development, nothing done!")
    return 0

    generateThumbnails(
        projectRoot=site.site_root
    )


def update_sidebar(site):
    manager = sidebar.SidebarManager(site)
    manager.build()


def full_update(site):
    create_thumbnails(site)
    update_sidebar(site)


def main():

    site = sitemanager.Website()

    options = {
        "1": ("Create thumbnails", create_thumbnails),
        "2": ("Update sidebar", update_sidebar),
        "3": ("Full update", full_update),
    }

    print("\nWebsite Control\n")

    for key, (name, _) in options.items():
        print(f"{key}: {name}")

    choice = input("\nSelect option: ")

    if choice in options:
        _, function = options[choice]
        function(site)
    else:
        print("Invalid selection")


if __name__ == "__main__":
    main()