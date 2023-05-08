#!/usr/bin/env python3
import os
import re
import sys
import json
import shutil
import zipfile
import requests
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup


class UpdateAPI():
    '''Updates the API module version for all or a specified platform.'''
    def __init__(self, version, branch, coins):
        self.version = version
        self.base_url = "http://54.170.62.22:8000/"
        self.api_branch = branch
        self.coins = coins
        self.platform = "wasm"
        # Get the absolute path of the project root directory
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.temp_folder = f"{self.project_root}/temp"
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

    def get_zip_file_url(self, platform, branch):
        '''Returns the URL of the zip file for the requested version / branch / platform.'''
        response = requests.get(f"{self.base_url}/{self.api_branch}")
        response.raise_for_status()

        # Configure the HTML parser
        soup = BeautifulSoup(response.text, "html.parser")        
        keywords = [self.platform]
        extensions = [".zip"]  # Assuming that the extensions are the same for all platforms

        # Parse the HTML and search for the zip file
        for link in soup.find_all("a"):
            file_name = link.get("href")
            if all(keyword in file_name for keyword in keywords) \
                    and any(file_name.endswith(ext) for ext in extensions) \
                    and self.version in file_name:
                return f"{self.base_url}/{self.api_branch}/{file_name}"
        return None

    def download_api_file(self):
        '''Downloads the API version zip file for a specific platform.'''
        # Get the URL of the zip file in the main directory
        print(f"Downloading API {self.platform} module [{self.version}] from {self.api_branch} branch")
        zip_file_url = self.get_zip_file_url(self.platform, self.api_branch)

        # If the zip file is not found in the main directory, search in all directories
        if not zip_file_url:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a"):
                branch = link.get("href")
                zip_file_url = self.get_zip_file_url(self.platform, branch)

                if zip_file_url:
                    print(f"'{self.platform}': Found zip file in '{branch}' folder.")
                    break

        if not zip_file_url:
            raise ValueError(f"Could not find zip file for version '{self.version}' on '{self.platform}' platform in branch {self.api_branch}!")

        # Download the zip file
        print(f"Downloading '{self.version}' API module for [{self.platform}]...")
        response = requests.get(zip_file_url, stream=True)
        response.raise_for_status()

        zip_file_name = os.path.basename(zip_file_url)
        zip_file_path = os.path.join(self.temp_folder, zip_file_name)

        # Save the zip file to the specified folder
        with open(zip_file_path, "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)

        print(f"Saved to '{zip_file_path}'")
        return zip_file_path
    
    def copy_file(self, source, target):
        try:
            shutil.copy(source, target)
            print(f"Copied {source} to {target}!")
        except IOError as e:
            print(f"IOError Error copying file: {e}")
        except:
            print("Unexpected error copying file:", sys.exc_info())

    def copy_folder(self, source, target):
        try:
            shutil.copytree(source, target, dirs_exist_ok=True)
            print(f"Copied {source} to {target}!")
        except IOError as e:
            print(f"IOError Error copying file: {e}")
        except:
            print("Unexpected error copying file:", sys.exc_info())

    def update_coins(self):
        '''Updates the coins file.'''
        coins = requests.get(f"https://raw.githubusercontent.com/KomodoPlatform/coins/{self.coins}/coins").json()
        with open(f"{self.project_root}/public/coins", "w") as f:
            json.dump(coins, f, indent=4)

    def update_api(self):
        '''Updates the API module.'''
        # Download the API file for the platform
        zip_file_path = self.download_api_file()

        # Unzip the downloaded file
        print(f"Extracting...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_folder)

        # Delete the zip file after extraction
        os.remove(zip_file_path)

        # Copy the API module file to the folders they need to be in
        self.copy_file(f"{self.temp_folder}/mm2lib_bg.wasm", f"{self.project_root}/public/mm2_bg.wasm")
        self.copy_file(f"{self.temp_folder}/mm2lib.js", f"{self.project_root}/src/js/mm2.js")
        self.copy_folder(f"{self.temp_folder}/snippets", f"{self.project_root}/src/js/snippets")

        # Delete the temp folder
        shutil.rmtree(self.temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download API module file for specified version and platform.")
    # Optional arguments
    parser.add_argument("-a", "--api", help="commit hash of the API module to download.", required=True)
    parser.add_argument("-b", "--branch", help="branch of the API module to download.", default="main")
    parser.add_argument("-c", "--coins", help="branch of the coins file to download.", default="master")
    args = parser.parse_args()

    try:
        updateAPI = UpdateAPI(args.api, args.branch, args.coins)
        updateAPI.update_api()
        updateAPI.update_coins()

    except Exception as e:
        print(f"Error: {e}")