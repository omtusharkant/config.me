from pyconfig.pyconfig import PyConfig
from j2power import j2p
import os
import re

scriptblocks = []



def GenerateScript(scriptblocks):
    if j2p.main(scriptblocks):
        print("Script generated successfully.")
    
Choice = input("choose your os(linux/windows): ")

if Choice == "linux":
    ...
elif Choice == "windows":
    

    setconfigfor = input("Choose configuration type: \n1. Hosting\n2. Development\n")
    if setconfigfor == "1":
        print("You chose Hosting configuration.")
        # Add hosting configuration code here
        
    elif setconfigfor == "2":
        print("You chose Development configuration.")
        
        #add ide configuration code here
        ide = input("Choose your IDE: \n1. VSCode\n2. PyCharm\n3. IntelliJ\n4. Eclipse\n5. Android Studio\n")
        if ide == "1":
            print("You chose VSCode.")
        elif ide == "2":
            print("You chose PyCharm.")
        elif ide == "3":
            print("You chose IntelliJ.")
        elif ide == "4":
            print("You chose Eclipse.")
        elif ide == "5":
            print("You chose Android Studio.")
        else:
                print("Invalid choice. Please choose a valid IDE.")
        
        
        # Add development configuration code here
        devenv = input("Choose your development environment: \n1. Python\n2. C/C++\n3. Web development\n4. Java development\n5. Go\n6. Rust\n7. Shell scripting\n8. SQL\n9. Android\n")
        if devenv == "1":
                downloadcho = input("Do you want to download Python? (y/n): ")
                if downloadcho.lower() == "y":
                    # Use the PyConfig module to fetch Python versions
                    python_versions = PyConfig.get_python_versions()
                    
                    version = input("Choose your Python version: ")
                    
                    download_pyver = PyConfig.download_python_version(version)
                    scriptblocks.append(download_pyver)
                    installpyver = PyConfig.install_python_version(download_pyver['vars']['file_name'])
                    scriptblocks.append(installpyver)
                    print("script block added successfully")
                    
                virtenv = input("do you want virtual enviroment(y/n)")
                if virtenv == "y":
                    fullp=""
                    path = re.split(r"[\\]",input("enter your project path"))
                    VIrname = input("enter your virtual enviroment name")
                    for p in path:
                        fullp=os.path.join(fullp,p)
                    print(path)
                    print(fullp)
                    
                    scriptblocks.append(PyConfig.createvirtualenv(fullp,VIrname))
                    
                    
                library = input("Do you want to install any libraries? (yes/no): ")
                if library.lower() == "yes":
                    libnames = input("Enter the library names (comma-separated): ")
                    lib_list = [lib.strip() for lib in libnames.split(",")]  # Split and strip whitespace
                    for libname in lib_list:
                        scriptblocks.append(PyConfig.install_library(libname))
                    print("Library installation scripts added successfully.")
                else:
                    print("No library installation script added.")
                
                
                
    else:
        print("Invalid choice. Please choose either '1' or '2'.")
        exit()
else:
    print("Invalid choice. Please choose either 'linux' or 'windows'.")
    exit()

print(scriptblocks)
GenerateScript(scriptblocks)