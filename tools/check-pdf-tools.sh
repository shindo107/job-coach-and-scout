#!/bin/bash
# tools/check-pdf-tools.sh
#
# Purpose: Detect available PDF generation engines (WeasyPrint and/or Typst).
# Outputs JSON with availability status for each tool.
#
# Exit codes:
#   0 - At least one PDF tool is available
#   1 - No PDF tools available (still outputs JSON)
#
# Usage: ./tools/check-pdf-tools.sh

# Check for WeasyPrint (Python package or CLI via pipx)
weasyprint_available=false
if python3 -c "import weasyprint" &> /dev/null || command -v weasyprint &> /dev/null; then
    weasyprint_available=true
fi

# Check for Typst (CLI tool)
typst_available=false
if command -v typst &> /dev/null; then
    typst_available=true
fi

# Determine if any tool is available
any_available=false
if [ "$weasyprint_available" = true ] || [ "$typst_available" = true ]; then
    any_available=true
fi

# Determine recommended tool (WeasyPrint preferred, Typst fallback)
recommended="null"
if [ "$weasyprint_available" = true ]; then
    recommended="\"weasyprint\""
elif [ "$typst_available" = true ]; then
    recommended="\"typst\""
fi

# Output JSON
cat << EOF
{
  "weasyprint": $weasyprint_available,
  "typst": $typst_available,
  "any_available": $any_available,
  "recommended": $recommended
}
EOF

# Exit with appropriate code
if [ "$any_available" = true ]; then
    exit 0
else
    exit 1
fi
