import os
from typing import Dict, List 

my_sounds = "F:/My Packs" # Choose the directory you wanna give the LLM access to

# returns in a dict the files and folders in the main dir
def list_files(path: str) -> Dict[str, List[str]]:
    return {"items": os.listdir(path)}


