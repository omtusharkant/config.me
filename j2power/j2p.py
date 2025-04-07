import json
import os
import re

import re

def replacevariables(block, replacements: dict):
    """
    Replace variables in the block with the provided replacements.
    
    Args:
        block (str): The block of code as a string.
        replacements (dict): A dictionary where keys are variable names and values are their replacements.
        
    Returns:
        str: The block of code with variables replaced.
    """
    for key, value in replacements.items():
        placeholder = f"{{{{{key}}}}}"  # Matches {{key}}
        
        print(f"Replacing {placeholder} with {value}")
        block = block.replace(placeholder, value)  # Replace the placeholder with the actual value
        #block = re.sub(escaped_placeholder, value, block)  # Replace the placeholder with the actual value
        print(f"Block after replacement: {block}")
    return block

def findBlock(blocks, blockset: list):
    """
    Find and process blocks based on the blockset configuration.
    
    Args:
        blocks (dict): A dictionary containing all blocks.
        blockset (list): A list of block configurations.
        
    Returns:
        str: The combined block code.
    """
    blockcodes = ""
    for blockname in blockset:
        print(blockname['name'])
        start_string = f"#starting of block {blockname['name']} \n"
        end_string = f"\n#ending of block {blockname['name']}\n\n"
        print(blockname['name'], blockname['tag'])
        if blockname['tag'] in blocks and blockname['name'] in blocks[blockname['tag']]:
            if "vars" in blockname and blockname['vars']:
                replacements = blockname['vars']
                blocks[blockname['tag']][blockname['name']]['Block'] = replacevariables(blocks[blockname['tag']][blockname['name']]['Block'], replacements)
            block = start_string + blocks[blockname['tag']][blockname['name']]['Block'] + end_string
            blockcodes = blockcodes + block
    return blockcodes

def load_blocks(directory: str):
    """
    Load all JSON files from the specified directory into a dictionary.
    
    Args:
        directory (str): The directory containing JSON files.
        
    Returns:
        dict: A dictionary of loaded blocks.
    """
    allblocks = {}
    for root, _, filenames in os.walk(os.path.abspath(directory)):
        for filename in filenames:
            if filename.endswith(".json"):
                print(filename.split(".")[0])
                with open(os.path.join(root, filename), 'r') as f:
                    allblocks[f'{filename.split(".")[0]}'] = json.load(f)
    return allblocks

def write_script(script_code: str, output_file: str):
    """
    Write the generated script code to a file.
    
    Args:
        script_code (str): The script code to write.
        output_file (str): The path to the output file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(script_code)
        return True

def main(blocksets: list):
    """
    Main function to execute the script generation process.
    """
    
    blocks_directory = "powershell_codes"
    output_file = "scripts/script.ps1"

    blocksets.insert(0,{'name':'AdminCheck','tag':'base'})
    
    allblocks = load_blocks(blocks_directory)
    script_code = findBlock(allblocks, blocksets)
    
    if write_script(script_code, output_file):
        return True