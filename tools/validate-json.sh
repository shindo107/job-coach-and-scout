#!/bin/bash
# tools/validate-json.sh

# Purpose: Reads JSON from stdin and validates its syntax.
# Exits with 0 if valid, 1 if invalid.
#
# This script relies on Python's built-in json.tool, which is a reliable,
# deterministic way to validate JSON syntax without relying on an LLM's
# interpretation or external libraries.

# Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed, which is required for validation." >&2
    exit 1
fi

# Read from stdin and attempt to parse using json.tool
# The output is redirected to /dev/null to suppress the pretty-printed JSON.
# We only care about the exit code.
if python3 -m json.tool >/dev/null 2>&1; then
  exit 0
else
  # To get a more useful error message, we can re-run it without redirection
  # and capture stderr. This is optional but helpful for debugging.
  ERROR_MESSAGE=$(python3 -m json.tool 2>&1 >/dev/null)
  echo "JSON validation error: $ERROR_MESSAGE" >&2
  exit 1
fi
