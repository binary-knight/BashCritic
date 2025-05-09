#!/usr/bin/env python3

import argparse
import sys
import yaml
from analyzer import analyze_script
from utils import load_script_from_file, print_findings
from prompt_templates import load_prompt_template
from spinner import Spinner
from auto_fixer import confirm, show_diff, backup_and_write
import re


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def extract_fixed_code(findings):
    """
    Extracts fixed code block from the LLM output using triple backtick pattern.
    """
    code_blocks = re.findall(r"```(?:bash)?\n(.*?)```", findings, re.DOTALL)
    return code_blocks[0].strip() if code_blocks else None


def main():
    parser = argparse.ArgumentParser(description="BashCritic - AI-powered Bash script reviewer")
    parser.add_argument("--file", help="Path to bash script to analyze")
    parser.add_argument("--stdin", action="store_true", help="Read script from stdin")
    parser.add_argument("--model", help="Override model from config.yaml")
    parser.add_argument("--json", action="store_true", help="Output results in JSON")
    parser.add_argument("--fix", action="store_true", help="Offer to apply suggested fixes to the script")
    args = parser.parse_args()

    config = load_config()
    model = args.model or config.get("model", "mistral")
    host = config.get("ollama_host", "http://localhost:11434")
    timeout = config.get("timeout", 60)

    # Load script
    if args.file:
        script = load_script_from_file(args.file)
    elif args.stdin:
        print("Reading from stdin. Press Ctrl+D when finished.\n")
        script = sys.stdin.read()
    else:
        print("Please specify either --file or --stdin.")
        sys.exit(1)

    prompt = load_prompt_template(script)

    spinner = Spinner("Analyzing script...")
    spinner.start()
    try:
        findings = analyze_script(prompt, model=model, host=host, timeout=timeout)
    finally:
        spinner.stop()

    print_findings(findings, as_json=args.json)

    if args.fix:
        fixed_code = extract_fixed_code(findings)
        if not fixed_code:
            print("\nCould not find valid code block in model response. No changes applied.")
            return

        if confirm("\nPreview and apply suggested changes?"):
            show_diff(script, fixed_code, args.file)
            if confirm("Save changes to file?"):
                backup_and_write(args.file, fixed_code)
            else:
                print("No changes were saved.")
        else:
            print("No changes applied.")


if __name__ == "__main__":
    main()