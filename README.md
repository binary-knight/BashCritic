# BashCritic

**BashCritic** is a self-hosted, AI-powered static analysis tool for Bash scripts.  
It leverages a local LLM via [Ollama](https://ollama.com) to identify security issues, stylistic problems, logic bugs, and potential bad practices in Bash code — entirely offline.

While its primary purpose is review and analysis, BashCritic also includes an **experimental feature**: `--fix`, which attempts to apply suggestions to the script automatically.  
This should be used with caution and always reviewed before accepting changes.

---

## Features

- Local, offline-capable Bash static analysis using LLMs
- Identifies:
  - Unquoted or dangerous variables
  - Unsafe commands (e.g., `eval`, `rm -rf`)
  - Syntax errors or logic mistakes
  - Style issues and best practice violations
- Accepts input via file or stdin
- Optional `--fix` mode to apply suggested changes directly
- Clean CLI with optional JSON output
- Configurable:
  - LLM model (Mistral, Phi, etc.)
  - Ollama host (local or remote)
  - Timeout duration
- Backup and safe-diff before file edits
- Includes installation script and sample tests
- Designed for air-gapped, offline, or secure environments

---

## Example Output

```bash
$ python3 bashcritic.py --file install_bashcritic.sh
```

```
Analysis Result:

1. Security Risk (Line 10): Use of unquoted variable $USER may lead to word splitting.
   Suggestion: Wrap with double quotes: "$USER"

2. Style Violation (Line 2): Use of '==' in test command, not POSIX-compliant.
   Suggestion: Use '=' instead.

3. Dangerous Pattern (Line 15): 'rm -rf $1' with no checks or quoting.
   Suggestion: Quote and validate variable: rm -rf "$1"
```

---

## Experimental Feature: `--fix`

If you pass the `--fix` flag, BashCritic will:

1. Show analysis results.
2. Ask if you'd like to preview changes.
3. Display a diff of proposed changes.
4. Ask if you'd like to save the file.
5. Save a `.bak` backup and apply edits if confirmed.

Due to the nature of LLMs, hallucinations are possible.  
Always review diffs and never blindly trust fixes. You assume full responsibility for any modifications.

---

## Configuration (`config.yaml`)

```yaml
# Available models from Ollama:
# - mistral
# - phi
# - llama2
# - tinyllama
# - gemma
# - dolphin-mixtral
# - or any custom pulled model
model: mistral

# Ollama API endpoint (can be remote)
ollama_host: http://localhost:11434

# Timeout in seconds for requests
timeout: 60

# Future settings
use_shellcheck: false
output_format: rich
severity_threshold: warning
```

---

## Installation

```bash
git clone https://github.com/binary-knight/bashcritic
cd bashcritic
chmod +x install_bashcritic.sh
./install_bashcritic.sh
```

This script:
- Creates a virtualenv
- Installs dependencies
- Installs Ollama (if needed)
- Pulls your selected model
- Creates `config.yaml` and `reports/`

---

## Usage

### Analyze from a file

```bash
python3 bashcritic.py --file yourscript.sh
```

### Analyze from stdin

```bash
cat yourscript.sh | python3 bashcritic.py --stdin
```

### Analyze and auto-fix

```bash
python3 bashcritic.py --file yourscript.sh --fix
```

### Output results as JSON

```bash
python3 bashcritic.py --file yourscript.sh --json
```

### Override model from CLI

```bash
python3 bashcritic.py --file yourscript.sh --model phi
```

---

## Output

- Human-readable summary (default)
- JSON output for scripting (`--json`)
- Experimental file rewrite with `--fix` and confirmation steps

---

## Test Scripts

Sample Bash scripts for testing can be found in `tests/`:

```bash
python3 bashcritic.py --file tests/unsafe.sh
```

---

## Roadmap

- ShellCheck integration (optional lint pass)
- Severity scoring and filtering
- Markdown + JSON output formatting
- Editor integration (VS Code / Neovim)
- Git pre-commit and GitHub Actions support

---

## License & Disclaimer

This tool is licensed under the MIT License.

BashCritic is provided *as-is* with no guarantees.  
It is developed independently by the author and not affiliated with any employer or organization.  
Use it at your own discretion and always verify its output — especially when using `--fix`.

---

## Support

If BashCritic saves you time or helps improve your workflow:

- [Sponsor the project on GitHub](https://github.com/sponsors/binary-knight)
- Buy the author a coffee: [https://buymeacoffee.com/binaryknight](https://buymeacoffee.com/binaryknight)

---

## Contributions

Pull requests, feedback, and issues are always welcome.