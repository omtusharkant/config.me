import requests
from bs4 import BeautifulSoup

def get_python_versions():
    url = "https://www.python.org/downloads/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    versions = []
    for release in soup.find_all('span', class_='release-number'):
        version_text = release.get_text(strip=True)
        version = version_text.replace("Python ", "")
        
        # Check if the version is stable or in development
        status_tag = release.find_next_sibling('span', class_='release-enhancements')
        status_text = status_tag.get_text(strip=True) if status_tag else "Stable"
        is_stable = "pre-release" not in status_text.lower()
        
        versions.append((version, "Stable" if is_stable else "Development"))
    
    return versions

if __name__ == "__main__":
    python_versions = get_python_versions()
    print("Python Released Versions:")
    for version, status in python_versions:
        print(f"{version} - {status}")
