from enums import ENUMS
import os
import shutil
import requests
from zipfile import ZipFile

class Installer:
    PACKAGE_MAP = {
        "RobloxApp.zip": "",
        "redist.zip": "",
        "shaders.zip": "shaders/",
        "ssl.zip": "ssl/",

        "WebView2.zip": "",
        "WebView2RuntimeInstaller.zip": "WebView2RuntimeInstaller/",

        "content-avatar.zip": "content/avatar/",
        "content-configs.zip": "content/configs/",
        "content-fonts.zip": "content/fonts/",
        "content-sky.zip": "content/sky/",
        "content-sounds.zip": "content/sounds/",
        "content-textures2.zip": "content/textures/",
        "content-models.zip": "content/models/",

        "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
        "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
        "content-terrain.zip": "PlatformContent/pc/terrain/",
        "content-textures3.zip": "PlatformContent/pc/textures/",

        "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
        "extracontent-translations.zip": "ExtraContent/translations/",
        "extracontent-models.zip": "ExtraContent/models/",
        "extracontent-textures.zip": "ExtraContent/textures/",
        "extracontent-places.zip": "ExtraContent/places/"
    }

    @staticmethod
    def _fetch_version_package_manifest(version):
        url = f"https://setup-cfly.rbxcdn.com/{version}-rbxPkgManifest.txt"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch version package manifest from {url}. Status code: {response.status_code}")
            return None

    def _get_packages(version):
        package_manifest = Installer._fetch_version_package_manifest(version)
        if package_manifest:
            return package_manifest
        else:
            return None

    @staticmethod
    def install(version, clean):
        current_roblox = ENUMS.PATHS["ROBLOX_PATH"]
        print(f"Current Roblox path: {current_roblox}")

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
                    print(f"Downloaded {zip_file} successfully.")

                    # Unzip the file
                    with ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(version_path, extract_path))
                    print(f"Extracted {zip_file} successfully.")

                    # Delete the zip file
                    os.remove(zip_path)
                else:
                    print(f"Failed to download {zip_file} from {url}. Status code: {response.status_code}")

            # Create AppSettings.xml
            app_settings_path = os.path.join(version_path, "AppSettings.xml")
            with open(app_settings_path, 'w') as file:
                file.write("""<?xml version="1.0" encoding="UTF-8"?>
<Settings>
    <ContentFolder>content</ContentFolder>
    <BaseUrl>http://www.roblox.com</BaseUrl>
</Settings>""")
                
            print("AppSettings.xml created successfully.")
            print(f"Roblox version {version} installed successfully.")
        else:
            print(f"Roblox version {version} already installed.")

print(Installer._get_packages(ENUMS.get_latest_version()))
Installer.install(ENUMS.get_latest_version(), True)