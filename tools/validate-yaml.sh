#!/bin/bash
# tools/validate-yaml.sh

# Purpose: Reads YAML from stdin and validates its syntax.
# Exits with 0 if valid, 1 if invalid.
#
# This script relies on Python and the PyYAML library, which are common
# in environments where YAML is used. It's a reliable, deterministic
# way to validate YAML syntax without relying on an LLM's interpretation.

# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed, which is required for validation." >&2
    exit 1
fi

# Check if PyYAML is installed
if ! python3 -c "import yaml" &> /dev/null
then
    echo "Error: PyYAML library not found. Please install it using 'pip install PyYAML'." >&2
    exit 1
fi

# Read from stdin and attempt to parse
python3 -c '
import yaml, sys

try:
    yaml.safe_load(sys.stdin)
    sys.exit(0)
except (yaml.YAMLError, ValueError) as e:
    print(f"YAML validation error: {e}", file=sys.stderr)
    sys.exit(1)
'
