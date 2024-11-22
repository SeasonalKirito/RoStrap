from enums import ENUMS
import os
import shutil
import requests
from zipfile import ZipFile

class Installer:
    def _fetch_version_package_manifest(version):
        url = f"https://setup.rbxcdn.com/{version}-rbxPkgManifest.txt"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch version package manifest from {url}. Status code: {response.status_code}")
            return None

    _versionPackageManifest = _fetch_version_package_manifest(ENUMS.get_latest_version())

    @staticmethod
    def install(version, clean):
        current_roblox = ENUMS.PATHS["ROBLOX_PATH"]
        print(current_roblox)

        if clean:
            for folder_name in os.listdir(current_roblox):
                folder_path = os.path.join(current_roblox, folder_name)
                if os.path.isdir(folder_path):
                    if folder_name != version:
                        shutil.rmtree(folder_path)
                    else:
                        print(f"Folder {folder_name} matches the version.")

        version_path = os.path.join(current_roblox, version)
        if not os.path.exists(version_path):
            os.makedirs(version_path)

            for zip_file, extract_path in Installer.PACKAGE_MAP.items():
                url = f"https://setup.rbxcdn.com/{version}-{zip_file}"
                zip_path = os.path.join(version_path, zip_file)

                # Download the file
                response = requests.get(url)
                if response.status_code == 200:
                    with open(zip_path, 'wb') as file:
                        file.write(response.content)

                    # Unzip the file
                    with ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(version_path, extract_path))

                    # Delete the zip file
                    os.remove(zip_path)
                else:
                    print(f"Failed to download {zip_file} from {url}. Status code: {response.status_code}")

            print(f"Roblox version {version} installed successfully.")
        else:
            print(f"Roblox version {version} already installed.")

Installer.install(ENUMS.get_latest_version(), True)