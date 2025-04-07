import os

class UserConfig:
    def __init__(self,os):
        self.os = os
        
    def get_existing_users(self):   
        if self.os == "linux":
            return "cut -d: -f1 /etc/passwd"
        elif self.os == "windows":
            return {'name':'Listusers','tag':'Usergroup'}
        else:
            raise ValueError("Unsupported OS")
        

    
    def create_new_user(self, username, password):
        if self.os == "linux":
            return f"sudo useradd {username} -p {password}"
        elif self.os == "windows":
            return {'name':'Createuser','vars':{"username":username,"password":password},'tag':'Usergroup'}
        else:
            raise ValueError("Unsupported OS")
        
    def delete_user(self, username):
        """
        Deletes a user from the Windows OS.
        :param username: The name of the user to delete.
        """
        if self.os == "linux":
            return f"sudo userdel {username}"
        elif self.os == "windows":
            return {'name':'Deleteuser','vars':{"username":username,},'tag':'Usergroup'}
        else:
            raise ValueError("Unsupported OS")