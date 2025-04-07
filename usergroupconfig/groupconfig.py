import os

class groupConfig:
    def __init__(self,os):
        self.os = os
        
    def get_existing_groups(self):   
        """
        Lists all groups on the system.
        """
        try:
            if self.os == "linux":
                # Command to list groups in Linux
                return "cut -d: -f1 /etc/group"
            elif self.os == "windows":
                # Use the 'net localgroup' command to list groups
                return {'name':'Listgroups','tag':'Usergroup'}
            else:
                raise ValueError("Unsupported OS")
        except Exception as e:
            print(f"Error retrieving groups: {e}")
            return []
        

    
    def create_new_group(self, groupname):
        """
        Creates a new group on the Windows OS.
        :param groupname: The name of the group to create.
        """
        try:
            if self.os == "linux":
                return f"sudo groupadd {groupname}"
            elif self.os == "windows":
                return {'name':'Creategroup','vars':{"groupname":groupname},'tag':'Usergroup'}
            else:
                raise ValueError("Unsupported OS")
        except Exception as e:
            print(f"Error creating group: {e}")
            
            
    def delete_group(self, groupname):
        """
        Deletes a group from the system.
        :param groupname: The name of the group to delete.
        """
        try:
            if self.os == "linux":
                # Command to delete a group in Linux
                return f"sudo groupdel {groupname}"
            elif self.os == "windows":
                # Use the 'net localgroup' command to delete a group
                return {'name':'Deletegroup','vars':{"groupname":groupname,},'tag':'Usergroup'}
            else:
                raise ValueError("Unsupported OS")
        except Exception as e:
            print(f"Error deleting group: {e}")