import requests
from bs4 import BeautifulSoup
from packaging import version as pkg_version  # Alias the 'version' module to avoid name clashes
#import json2powershell as j2p  # Importing the json2powershell library for JSON to PowerShell conversion

from tqdm import tqdm  # Progress bar library
import os

class PyConfig:
    @staticmethod
    def get_python_versions():
        """
        Fetches the list of Python versions from the official Python website.
        Returns:
            list: A list of tuples containing version and status (Stable/Development).
        """
        try:
            url = "https://www.python.org/downloads/"
            try:
                response = requests.get(url)
            except requests.ConnectionError as e:
                print(f"Connection error: {e}")
                return []
            
            if response.status_code != 200:
                print("Failed to retrieve the webpage")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            versions = []
            for release in soup.find_all('span', class_='release-number'):
                version_text = release.get_text(strip=True)
                version_str = version_text.replace("Python ", "")
                
                # Check if the version is stable or in development
                status_tag = release.find_next_sibling('span', class_='release-enhancements')
                status_text = status_tag.get_text(strip=True) if status_tag else "Stable"
                is_stable = "pre-release" not in status_text.lower()
                
                # Only add valid versions (skip any non-version strings like 'Release version')
                try:
                    pkg_version.parse(version_str)  # This will raise an error if version_str is invalid
                    versions.append((version_str, "Stable" if is_stable else "Development"))
                except pkg_version.InvalidVersion:
                    print(f"Skipping invalid version: {version_str}")
            
            # Debugging: Print the raw versions before sorting
            print("Raw Versions (before sorting):")
            for version_str, status in versions:
                print(f"{version_str} - {status}")
            
            # Sort versions using 'packaging.version' to handle comparisons properly
            try:
                sorted_versions = sorted(versions, key=lambda v: pkg_version.parse(v[0]), reverse=True)
            except Exception as e:
                print(f"Error during sorting: {e}")
                return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        # Print the sorted versions
        latest_version = sorted_versions[0]
        print("Latest Python Version:")
        print(f"{latest_version[0]} - {latest_version[1]}")

        print("\nAll Python Versions:")
        for version, status in sorted_versions:
            print(f"{version} - {status}")
        
            
    @staticmethod
    def download_python_version(version):
        """
        Downloads the specified Python version for Windows 64-bit with a progress bar.

        Args:
            version (str): The Python version to download (e.g., "3.12.3").
        """
        # Ensure the version is in the correct format (e.g., "3.12.3")
        if not version or not version.replace('.', '').isdigit():
            print("Invalid version format. Please provide a version like '3.12.3'.")
            return

        url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
        file_name = f"python-{version}-amd64.exe"
        


        blocks = {'name':"DownloadFile",'vars':{"download_url ":url,"file_name":file_name},'tag':'base'}
        return blocks
    
    @staticmethod
    def install_python_version(path):
        ...
        blocks = {'name':"InstallFile",'vars':{"install_file_path":path},'tag':'base'}
        return blocks
    
    def install_library(libname):
        """
        Generates a script block for installing a Python library using pip.

        Args:
            libname (str): The name of the library to install.

        Returns:
            dict: A dictionary representing the script block.
        """
        blocks = {'name':"DownloadPythonLibraries",'vars':{"library_name":libname},'tag':'python'}
        return blocks
# Example usage
# PyConfig.download_python_version("3.12.3")

