import json

def load_script_from_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Failed to read file '{path}': {e}")
        return ""

def print_findings(findings, as_json=False):
    if as_json:
        print(json.dumps({"analysis": findings}, indent=2))
    else:
        print("\nAnalysis Result:\n")
        print(findings)

def extract_fixed_code(findings):
    """
    Try to extract fixed script from LLM output if it's wrapped in triple backticks or similar.
    """
    import re
    code_blocks = re.findall(r"```(?:bash)?\\n(.*?)```", findings, re.DOTALL)
    return code_blocks[0].strip() if code_blocks else None
