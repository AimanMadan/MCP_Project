#mcp_tools
import os
from typing import Dict, List, Union

my_sounds = "F:/My Packs" # Choose the directory you wanna give the LLM access to

# returns in a dict of the files and folders in the main dir
def list_files_implementation(path: str) -> Dict[str, Union[List[str], str]]:
    try:
# Prevent escaping the base directory, No LLM going Skynet
#         
#                        ______
#                      <((((((\\\
#                      /      . }\
#                      ;--..--._|}
#   (\                 '--/\--'  )
#    \\                | '-'  :'|
#     \\               . -==- .-|
#      \\               \.__.'   \--._
#      [\\          __.--|       //  _/'--.
#      \ \\       .'-._ ('-----'/ __/      \
#       \ \\     /   __>|      | '--.       |
#        \ \\   |   \   |     /    /       /
#         \ '\ /     \  |     |  _/       /
#          \  \       \ |     | /        /
#           \  \      \        /


        if ".." in path.split(os.path.sep):
            return {"error": "Invalid path: '..' sequence not allowed."}

        # Join the base path with the relative path
        # If path is ".", it refers to the base directory itself
        if path == ".":
            target_path = my_sounds
        else:
            target_path = os.path.join(my_sounds, path)
        
        # Normalize the path to resolve any redundant separators or "." components
        target_path = os.path.normpath(target_path)

        # Ensure the resolved path is still within the base directory
        if not target_path.startswith(os.path.normpath(my_sounds)):
            return {"error": "Invalid path: Attempt to access outside the base directory."}

        if not os.path.exists(target_path):
            return {"error": f"Path not found: {target_path}"}
        
        if not os.path.isdir(target_path):
            return {"error": f"Path is not a directory: {target_path}"}
            
        items = os.listdir(target_path)
        return {"items": items}
        
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
    
    
# Teshting Teshing  
# print(list_files_implementation(my_sounds))
    
    


