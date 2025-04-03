from pyconfig.pyconfig import PyConfig
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
            
            # Use the PyConfig module to fetch Python versions
            python_versions = PyConfig.get_python_versions()
            
            version = input("Choose your Python version: ")
            
            download_pyver = PyConfig.download_python_version(version)
            if download_pyver:
                print(f"Downloading Python version {version}...")
            else:
                print(f"Python version {version} is not available for download.")
    else:
        print("Invalid choice. Please choose either '1' or '2'.")
        exit()
else:
    print("Invalid choice. Please choose either 'linux' or 'windows'.")
    exit()