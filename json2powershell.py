import json

def checkcodeblock(data, block: list):
    """
    Validates the JSON data structure to ensure it contains the required keys for each block.
    """
    try:
        for b in block:
            # Check if the JSON data contains the required keys
            if b not in data:
                raise ValueError(f"Missing '{b}' key in JSON data")
            if "steps" not in data[b]:
                raise ValueError(f"Missing 'steps' key in '{b}' section")
            if "errorHandling" not in data[b]:
                raise ValueError(f"Missing 'errorHandling' key in '{b}' section")

            # Check if each step has the required keys
            for step in data["DownloadFile"]["steps"]:
                if "step" not in step or "command" not in step:
                    raise ValueError(f"Missing 'step' or 'command' key in step: {step}")

            print("Code block is valid.")
            return True
    except ValueError as e:
        print(f"Validation Error: {e}")
        return False


def findblock(data, blocks):
    """
    Finds and retrieves a specific block from the JSON data.
    """
    print(blocks)
    print("-----------------")
    if blocks in data:
        # Check if the block is a dictionary and contains the required keys
        if isinstance(data[blocks], dict):
            return {blocks: data[blocks]}
        else:
            print(f"Block '{blocks}' is not a valid dictionary or missing required keys.")


def writescript(script):
    """
    Writes the generated PowerShell script to a file.
    """
    with open("script.ps1", "w") as f:
        f.write(script)


def generate_powershell_step(step):
    """
    Generates PowerShell code for a single step in the JSON data.
    """
    powershell_code = ""
    if "condition" in step:
        powershell_code += f"if ({step['condition']}) {{\n"

    for var_name, var_value in step.get("variables", {}).items():
        powershell_code += f"${var_name} = \"{var_value}\"\n"

    parameter_string = " ".join([f"-{key} \"{value}\"" for key, value in step.get("parameters", {}).items()])
    powershell_code += f"{step['command']} {parameter_string}\n"

    if "successMessage" in step:
        powershell_code += f"Write-Host \"{step['successMessage']}\"\n"

    if "errorMessage" in step:
        if step.get("exitCodeCheck", False):
            powershell_code += "if ($LASTEXITCODE -ne 0) {\n"
            powershell_code += f"Write-Warning \"{step['errorMessage']} with exit code: $LASTEXITCODE\"\n"
            powershell_code += "}\n"
        else:
            powershell_code += f"Write-Error \"{step['errorMessage']}\"\n"

    if "condition" in step:
        powershell_code += "}\n"

    return powershell_code


def addcodeblock(data, blockname, filename):
    """
    Generates PowerShell code for an entire block and writes it to a file.
    """
    print(data, blockname)
    block = findblock(data, blockname)
    print(block)
    block = modify_variables(block, blockname)

    powershell_code = "# Requires elevated privileges (Run as Administrator)\n\n"

    if data[blockname]["requiresAdmin"]:
        powershell_code += "# Admin rights required\n"

    # Start the try block
    powershell_code += "try {\n"

    # Add steps to the try block
    for step in data[blockname]["steps"]:
        powershell_code += f"\t# {step['step']}\n"
        powershell_code += "\t" + generate_powershell_step(step).replace("\n", "\n\t") + "\n"

    # Close the try block
    powershell_code += "}\n"

    # Add catch and finally blocks
    error_handling = data[blockname]["errorHandling"]
    powershell_code += "catch {\n"
    powershell_code += f"\t{error_handling['catch']}\n"
    powershell_code += "}\n"
    powershell_code += "finally {\n"
    powershell_code += f"\t{error_handling['finally']}\n"
    powershell_code += "}"

    # Write the generated PowerShell code to a file
    return powershell_code


def modify_variables(block, blockname):
    """
    Prompts the user to modify variables in the JSON block.
    """
    try:
        # Modify variables
        for step in block[blockname]["steps"]:
            if "variables" in step:
                for var_name in step["variables"]:
                    print(var_name, type(step["variables"][var_name]))
                    if isinstance(step["variables"][var_name], str):
                        print(step["variables"][var_name])
                        # Update the value directly in the dictionary
                        step["variables"][var_name] = input(f"Enter value for {var_name}: ")

        # Convert the modified Python dictionary back to JSON
        modified_json = json.dumps(block, indent=2)
        print(modified_json)
        return modified_json

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")


# Main Execution
# Read the JSON codes
with open("powershell_codes/baseuse.json") as f:
    json_data = f.read()  # JSON data as a string

setblock = ["InstallFile", "DownloadFile"]
powerscript = ""
data = json.loads(json_data)

if checkcodeblock(data, setblock):
    for b in setblock:
        script = addcodeblock(data, b, "scripts/script.ps1")
        powerscript += script + "\n\n"

writescript(powerscript)
print("PowerShell script generated successfully.")
