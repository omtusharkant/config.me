import requests
from bs4 import BeautifulSoup
from packaging import version as pkg_version  # Alias the 'version' module to avoid name clashes
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
        url = "https://www.python.org/downloads/"
        response = requests.get(url)
        
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
        destination_folder = "python_downloads"

        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        file_path = os.path.join(destination_folder, file_name)

        try:
            print(f"Downloading Python {version} from {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for HTTP issues

            # Get the total file size from headers
            total_size = int(response.headers.get('content-length', 0))

            # Use tqdm to display the progress bar
            with open(file_path, "wb") as file, tqdm(
                desc=f"Downloading {file_name}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

            print(f"Python {version} downloaded successfully to {file_path}")
            return file_path

        except requests.exceptions.RequestException as e:
            print(f"Failed to download Python {version}: {e}")
            return None

# Example usage
# PyConfig.download_python_version("3.12.3")

