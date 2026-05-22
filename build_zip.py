#!/usr/bin/env python3
"""Build a Kodi-installable zip for plugin.video.catchuptvandmore."""

import os
import zipfile
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ADDON_ID = "plugin.video.catchuptvandmore"
DIST_DIR = os.path.join(REPO_ROOT, "dist")

# Only these root-level files are included
ROOT_FILES = {"addon.py", "addon.xml", "fanart.jpg", "icon.png", "LICENSE.txt", "service.py"}

# Exclude from inside the resources/ folder
EXCLUDE_EXTS = {".pyc", ".pyo", ".bak", ".DS_Store"}


def get_version():
    tree = ET.parse(os.path.join(REPO_ROOT, "addon.xml"))
    return tree.getroot().get("version")


def main():
    version = get_version()
    zip_name = f"{ADDON_ID}-{version}.zip"

    os.makedirs(DIST_DIR, exist_ok=True)
    zip_path = os.path.join(DIST_DIR, zip_name)

    print(f"Building {zip_path} ...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        # Add whitelisted root files
        for filename in ROOT_FILES:
            abs_path = os.path.join(REPO_ROOT, filename)
            if os.path.exists(abs_path):
                zip_entry = f"{ADDON_ID}/{filename}"
                zf.write(abs_path, zip_entry)
            else:
                print(f"  WARNING: {filename} not found, skipping")

        # Add entire resources/ folder
        resources_dir = os.path.join(REPO_ROOT, "resources")
        for dirpath, dirnames, filenames in os.walk(resources_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1] in EXCLUDE_EXTS:
                    continue
                abs_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(abs_path, REPO_ROOT)
                zip_entry = f"{ADDON_ID}/{rel_path.replace(os.sep, '/')}"
                zf.write(abs_path, zip_entry)

    size_mb = os.path.getsize(zip_path) / 1024 / 1024
    print(f"Done: {zip_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
