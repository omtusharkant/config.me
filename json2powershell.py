import json
import re
import os # Import os for path handling
from datetime import datetime # Import datetime for timestamp

# --- Utility Functions (Mostly Unchanged) ---

def findblock(data, block_name):
    """Finds and retrieves a specific block's content (dictionary) from the JSON data."""
    if block_name in data and isinstance(data[block_name], dict):
        return data[block_name]
    print(f"Warning: Block '{block_name}' not found or invalid in provided data.")
    return None

def writescript(script, filename="script.ps1"):
    """Writes the generated PowerShell script to a file."""
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
             os.makedirs(output_dir)
             print(f"Created output directory: {output_dir}")

        with open(filename, "w", encoding='utf-8') as f: # Specify encoding
            f.write(script)
        print(f"PowerShell script written to {filename}")
    except IOError as e:
        print(f"Error writing script to {filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during script writing: {e}")

# --- Core Generation Functions (Modified) ---

def generate_powershell_step(step, loop_variable_map=None):
    """
    Generates PowerShell code for a single step in the JSON data.
    (Handles placeholder replacement and loop variables)
    """
    if loop_variable_map is None:
        loop_variable_map = {}

    powershell_code = ""
    defined_vars = set()

    # 1. Define static variables from 'variables' dict
    for var_name, var_value in step.get("variables", {}).items():
        ps_var_name = f"${var_name}"
        defined_vars.add(var_name)
        if var_name in loop_variable_map:
            pass # Assume mapped variable is used directly where needed
        elif isinstance(var_value, str) and var_value.startswith("{{") and var_value.endswith("}}"):
            pass # Assume placeholder variable is defined elsewhere
        else:
            # Define static variable (ensure proper escaping if needed, simplified here)
            powershell_code += f"{ps_var_name} = \"{str(var_value).replace('\"', '`\"')}\" # Define variable\n" # Basic quote escaping

    # 2. Prepare command and messages
    command = step.get('command', '')
    success_message = step.get('successMessage', '')
    error_message = step.get('errorMessage', '')

    # 3. Generate parameter string
    parameter_string = ""
    parameters = step.get("parameters", {})
    if parameters:
         # Basic parameter generation - assumes simple values
         parameter_string = " ".join([f"-{key} \"{str(value).replace('\"', '`\"')}\"" for key, value in parameters.items()])

    # 4. Assemble the main command line
    full_command = f"{command} {parameter_string}".strip()

    # 5. Replace placeholders {{var_name}} -> $var_name or loop variable
    def replace_placeholder(match):
        var_name = match.group(1)
        if var_name in loop_variable_map:
            return loop_variable_map[var_name]
        return f"${var_name}" # Assume it's a defined PS variable

    full_command = re.sub(r"\{\{(\w+)\}\}", replace_placeholder, full_command)
    success_message = re.sub(r"\{\{(\w+)\}\}", replace_placeholder, success_message)
    error_message = re.sub(r"\{\{(\w+)\}\}", replace_placeholder, error_message)
    error_message = error_message.replace("{{error_message}}", '$_.Exception.Message') # Specific placeholder

    powershell_code += f"{full_command}\n"

    # 6. Add success message handling
    if success_message:
        powershell_code += f"Write-Host \"{success_message}\"\n"

    # 7. Error message handling is deferred to the main try/catch block

    return powershell_code

def generate_steps_code(steps_list, blockname=""):
    """ Generates PowerShell code for a list of steps, without try/catch. """
    powershell_code = ""
    if not isinstance(steps_list, list):
         print(f"Warning: 'steps' for block '{blockname}' is not a list. Skipping step generation.")
         return ""

    for i, step in enumerate(steps_list):
         step_description = step.get('step', f'Step {i+1}')
         powershell_code += f"\t# --- Step: {step_description} ---\n"
         step_code = generate_powershell_step(step) # No loop map needed here
         powershell_code += "\t" + step_code.replace("\n", "\n\t").strip() + "\n\n"
    return powershell_code


def addcodeblock(block_data, blockname):
    """
    Generates PowerShell code for an entire block (try/catch structure).
    Handles specific logic for DownloadPythonLibraries loop.
    """
    if not block_data:
        return "" # Return empty if block data is invalid

    powershell_code = f"# === Start Block: {blockname} ===\n"
    powershell_code += f"# Description: {block_data.get('description', 'N/A')}\n"

    # --- Specific Handling for DownloadPythonLibraries ---
    is_download_block = blockname == "DownloadPythonLibraries"
    if is_download_block:
        # Define libraries and target directory (Consider making these configurable)
        libraries = ["requests", "numpy", "pandas"] # Example list
        target_directory = "C:\\Downloads\\PythonLibs" # Example static path
        powershell_code += f"\n# Defining variables for {blockname}\n"
        powershell_code += f"$target_directory_var = \"{target_directory}\" # Set download directory\n"
        powershell_code += f"$Libraries = @({', '.join([f'\"{lib}\"' for lib in libraries])}) # List of libraries\n\n"
    # Add similar sections here if 'DownloadFile' or 'InstallFile' need specific pre-try setup

    # Start the try block
    powershell_code += "try {\n"
    powershell_code += f"\tWrite-Host \"Executing steps for block: {blockname}\"\n"

    # --- Process Steps ---
    steps = block_data.get("steps", [])
    num_steps = len(steps)

    if not isinstance(steps, list):
        print(f"Warning: 'steps' for block '{blockname}' is not a list. No steps generated inside try block.")
        steps = [] # Ensure loop doesn't fail

    for i, step in enumerate(steps):
        is_last_step = (i == num_steps - 1)
        step_description = step.get('step', f'Step {i+1}')
        powershell_code += f"\t# --- Step: {step_description} ---\n"

        # --- Looping Logic for DownloadPythonLibraries (Last Step) ---
        if is_download_block and is_last_step:
            powershell_code += "\tWrite-Host \"Starting library download loop...\"\n"
            powershell_code += "\tforeach ($lib in $Libraries) {\n"
            powershell_code += f"\t\tWrite-Host \"Attempting to download library: $lib to $target_directory_var\"\n"
            loop_map = {"library_name_var": "$lib"} # Map JSON var to PS loop var
            step_code = generate_powershell_step(step, loop_variable_map=loop_map)
            powershell_code += "\t\t" + step_code.replace("\n", "\n\t\t").strip() + "\n"
            powershell_code += "\t} # End foreach $lib\n"
            powershell_code += "\tWrite-Host \"Library download loop finished.\"\n"
        else:
             # --- Generate code for non-loop steps ---
             step_code = generate_powershell_step(step)
             powershell_code += "\t" + step_code.replace("\n", "\n\t").strip() + "\n"

        powershell_code += "\n" # Add blank line after each step section

    # Close the try block
    powershell_code += "} # End try\n"

    # Add catch and finally blocks
    error_handling = block_data.get("errorHandling", {})
    catch_action = error_handling.get('catch', '')
    finally_action = error_handling.get('finally', None)

    powershell_code += "catch {\n"
    if catch_action == "LogErrorAndContinue":
         powershell_code += "\tWrite-Warning \"An error occurred during block '$($blockname)': $($_.Exception.Message)\" # Error caught\n"
         # Use Write-Warning instead of Write-Error to allow script to potentially continue easier if desired
    elif catch_action:
         powershell_code += f"\t{catch_action}\n" # Use literal code with caution
    else:
         powershell_code += "\tWrite-Warning \"An unexpected error occurred in '$($blockname)' try block: $($_.Exception.Message)\" # Default catch\n"
    powershell_code += "} # End catch\n"

    powershell_code += "finally {\n"
    if finally_action is None or finally_action == "null":
         powershell_code += "\tWrite-Host \"Finished executing block '$($blockname)' (finally).\"\n"
    elif finally_action:
         powershell_code += f"\t{finally_action}\n" # Use literal code with caution
    powershell_code += "} # End finally\n"
    powershell_code += f"# === End Block: {blockname} ===\n\n" # Add separator

    return powershell_code


# --- Main Execution ---

# --- Configuration ---
base_json_file = "powershell_codes/baseuse.json"
python_json_file = "powershell_codes/python.json"
output_script_file = "scripts/combined_script.ps1"

# Define target blocks and their source file keys
targets = [
    {"name": "DownloadFile", "source": "base"},
    {"name": "InstallFile", "source": "base"},
    {"name": "DownloadPythonLibraries", "source": "python"}
]
admin_check_block_name = "AdminCheck" # The name of the admin check block in base_json

# --- Load Data ---
all_data = {}
try:
    print(f"Loading base JSON from: {base_json_file}")
    with open(base_json_file, 'r', encoding='utf-8') as f:
        all_data["base"] = json.load(f)
    print(f"Loading python JSON from: {python_json_file}")
    with open(python_json_file, 'r', encoding='utf-8') as f:
        all_data["python"] = json.load(f)
except FileNotFoundError as e:
    print(f"Error: Input JSON file not found. {e}")
    exit(1) # Exit if essential files are missing
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred during data loading: {e}")
    exit(1)

# --- Generate Script ---
combined_powershell_script = f"# Combined PowerShell Script\n"
combined_powershell_script += f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
admin_check_generated = False # Flag to generate admin check only once if needed multiple times (optional optimization)
admin_check_code = "" # Store generated admin check code

# Optional: Pre-generate Admin Check code if it exists
admin_check_block_data = findblock(all_data["base"], admin_check_block_name)
if admin_check_block_data:
    admin_check_steps = admin_check_block_data.get("steps")
    if admin_check_steps:
        print(f"Pre-generating code for '{admin_check_block_name}' block...")
        admin_check_code = f"# --- Start Block: {admin_check_block_name} (Admin Check) ---\n"
        admin_check_code += "# Description: Ensures the script is running with Administrator privileges.\n"
        # Generate steps code without try/catch for the check itself
        admin_check_code += generate_steps_code(admin_check_steps, admin_check_block_name)
        admin_check_code += f"# --- End Block: {admin_check_block_name} ---\n\n"
    else:
        print(f"Warning: '{admin_check_block_name}' block found but has no 'steps'.")
else:
    print(f"Warning: Required '{admin_check_block_name}' block not found in {base_json_file}. Cannot perform admin checks.")


# Process target blocks
print("\n--- Processing Target Blocks ---")
for target in targets:
    blockname = target["name"]
    source_key = target["source"]
    print(f"Processing block: '{blockname}' from source: '{source_key}'")

    if source_key not in all_data:
        print(f"Error: Source key '{source_key}' not found in loaded data. Skipping block '{blockname}'.")
        continue

    source_data = all_data[source_key]
    block_data = findblock(source_data, blockname)

    if not block_data:
        print(f"Skipping block '{blockname}' as it was not found or invalid.")
        continue

    # Basic validation
    if "steps" not in block_data or "errorHandling" not in block_data:
         print(f"Warning: Block '{blockname}' is missing 'steps' or 'errorHandling'. Skipping.")
         continue

    # Check if admin rights are required
    is_admin_required = block_data.get("requiresAdmin", False)

    # Add AdminCheck code if required for this block and available
    if is_admin_required:
        if admin_check_code:
            print(f"Block '{blockname}' requires admin rights. Inserting '{admin_check_block_name}'.")
            combined_powershell_script += admin_check_code
            # Optional: Prevent adding it again immediately if flag optimization is used
            # admin_check_generated = True
        else:
            print(f"Warning: Block '{blockname}' requires admin rights, but '{admin_check_block_name}' code is unavailable.")

    # Generate the main code for the target block
    block_script = addcodeblock(block_data, blockname)
    combined_powershell_script += block_script

# --- Write Output ---
writescript(combined_powershell_script, output_script_file)

print("\n--- Script Generation Complete ---")