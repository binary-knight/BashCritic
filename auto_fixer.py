
import difflib
import os
from datetime import datetime

def confirm(prompt):
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response == "y"

def show_diff(original: str, fixed: str, filename: str):
    print(f"\n--- {filename} (original)")
    print(f"+++ {filename} (proposed fix)")
    print("")

    diff = difflib.unified_diff(
        original.splitlines(), 
        fixed.splitlines(), 
        lineterm="", 
        fromfile=filename,
        tofile=f"{filename} (fixed)"
    )

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            print(f"\033[92m{line}\033[0m")  # green for additions
        elif line.startswith("-") and not line.startswith("---"):
            print(f"\033[91m{line}\033[0m")  # red for removals
        else:
            print(line)

def backup_and_write(filename: str, new_content: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{filename}.bak_{timestamp}"
    os.rename(filename, backup_file)
    print(f"Backup saved as {backup_file}")
    
    with open(filename, "w") as f:
        f.write(new_content)
    print(f"File updated: {filename}")