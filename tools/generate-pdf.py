#!/usr/bin/env python3
"""
tools/generate-pdf.py

Purpose: Generate PDF resumes from Markdown input using auto-detected PDF engines.
Supports WeasyPrint (preferred) and Typst (fallback).

Exit codes:
    0 - Success
    1 - No PDF engine available
    2 - Invalid input (missing file, bad format)
    3 - Template error (invalid or missing template)
    4 - PDF generation failed

Usage:
    python3 tools/generate-pdf.py <input.md> <output.pdf> [--template <template.yaml>]

Arguments:
    input.md        Path to the Markdown resume file
    output.pdf      Path for the generated PDF output
    --template      Optional path to resume_template.yaml (default: profile/resume_template.yaml)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Exit codes
EXIT_SUCCESS = 0
EXIT_NO_ENGINE = 1
EXIT_BAD_INPUT = 2
EXIT_TEMPLATE_ERROR = 3
EXIT_GENERATION_FAILED = 4

# Default paths
DEFAULT_TEMPLATE_PATH = "profile/resume_template.yaml"
SCRIPT_DIR = Path(__file__).parent
WEASYPRINT_TEMPLATE_DIR = SCRIPT_DIR / "templates" / "weasyprint"
TYPST_TEMPLATE_DIR = SCRIPT_DIR / "templates" / "typst"


def check_weasyprint() -> bool:
    """Check if WeasyPrint is available (as module or CLI)."""
    # First check Python module
    try:
        import weasyprint
        return True
    except ImportError:
        pass
    # Fall back to CLI check
    return shutil.which("weasyprint") is not None


def get_weasyprint_mode() -> str | None:
    """Return 'module' if weasyprint is importable, 'cli' if only CLI available, None if neither."""
    try:
        import weasyprint
        return "module"
    except ImportError:
        pass
    if shutil.which("weasyprint"):
        return "cli"
    return None


def check_typst() -> bool:
    """Check if Typst CLI is available."""
    return shutil.which("typst") is not None


def detect_engine() -> str | None:
    """Detect available PDF engine. Returns 'weasyprint', 'typst', or None."""
    if check_weasyprint():
        return "weasyprint"
    elif check_typst():
        return "typst"
    return None


def load_template(template_path: Path) -> dict:
    """Load and parse the resume template YAML file."""
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML not installed. Run: pip install PyYAML", file=sys.stderr)
        sys.exit(EXIT_TEMPLATE_ERROR)

    if not template_path.exists():
        # Return default template configuration
        return get_default_template()

    try:
        with open(template_path, "r") as f:
            template = yaml.safe_load(f)
            if template is None:
                return get_default_template()
            return template
    except yaml.YAMLError as e:
        print(f"Error: Invalid template YAML: {e}", file=sys.stderr)
        sys.exit(EXIT_TEMPLATE_ERROR)


def get_default_template() -> dict:
    """Return default template configuration when no template file exists."""
    return {
        "schema_version": "1.0",
        "layout": {
            "type": "single-column",
            "page_size": "letter",
            "margins": {
                "top": "0.5in",
                "bottom": "0.5in",
                "left": "0.5in",
                "right": "0.5in"
            }
        },
        "header": {
            "name_position": "left",
            "name_size": "large",
            "contact_layout": "single-line",
            "contact_separator": "|"
        },
        "sections": {
            "order": ["summary", "experience", "skills", "education"],
            "experience": {
                "company_title_order": "title-first",
                "date_position": "right",
                "date_format": "MMM YYYY",
                "bullet_style": "-"
            }
        },
        "typography": {
            "style": "modern",
            "font_family": "sans-serif",
            "heading_weight": "bold",
            "body_size": "11pt"
        },
        "colors": {
            "primary": "#2C3E50",
            "secondary": "#7F8C8D",
            "body": "#333333"
        },
        "special_features": {
            "has_dividers": False,
            "has_icons": False,
            "skills_format": "inline"
        }
    }


def read_markdown(input_path: Path) -> str:
    """Read the Markdown input file."""
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error: Could not read input file: {e}", file=sys.stderr)
        sys.exit(EXIT_BAD_INPUT)


def parse_resume_markdown(content: str) -> dict:
    """Parse Markdown resume content into structured data."""
    # Remove YAML frontmatter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    data = {
        "name": "",
        "contact_info": "",
        "sections": []
    }

    lines = content.strip().split("\n")
    current_section = None
    current_content = []

    for line in lines:
        # Check for H1 (name)
        if line.startswith("# ") and not data["name"]:
            data["name"] = line[2:].strip()
            continue

        # Check for H2 (section headers)
        if line.startswith("## "):
            # Save previous section
            if current_section:
                data["sections"].append({
                    "title": current_section,
                    "content": "\n".join(current_content).strip()
                })
            current_section = line[3:].strip()
            current_content = []
            continue

        # Check for contact info (typically first few non-header lines after name)
        if data["name"] and not current_section and line.strip():
            if not data["contact_info"]:
                data["contact_info"] = line.strip()
            elif "|" in line or "@" in line or "linkedin" in line.lower():
                data["contact_info"] += " | " + line.strip()
            continue

        # Accumulate section content
        if current_section:
            current_content.append(line)

    # Don't forget the last section
    if current_section:
        data["sections"].append({
            "title": current_section,
            "content": "\n".join(current_content).strip()
        })

    return data


def markdown_to_html(content: str) -> str:
    """Convert Markdown content to HTML."""
    try:
        import markdown
        return markdown.markdown(content, extensions=['tables', 'fenced_code'])
    except ImportError:
        # Fallback to basic conversion
        return basic_markdown_to_html(content)


def basic_markdown_to_html(content: str) -> str:
    """Basic Markdown to HTML conversion without external library."""
    html = content

    # Convert headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Convert bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Convert bullet lists
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    html = '\n'.join(result)

    # Convert paragraphs (simple approach)
    paragraphs = html.split('\n\n')
    html = '\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)

    return html


def generate_styled_html(resume_data: dict, template: dict) -> str:
    """Generate complete styled HTML from resume data and template."""
    # Read base HTML template
    base_html_path = WEASYPRINT_TEMPLATE_DIR / "base.html"
    css_path = WEASYPRINT_TEMPLATE_DIR / "styles.css"

    if not base_html_path.exists() or not css_path.exists():
        print(f"Error: Template files not found in {WEASYPRINT_TEMPLATE_DIR}", file=sys.stderr)
        sys.exit(EXIT_TEMPLATE_ERROR)

    # Read CSS
    with open(css_path, "r") as f:
        css_content = f.read()

    # Build sections HTML
    sections_html = ""
    for section in resume_data.get("sections", []):
        section_html = markdown_to_html(section["content"])
        sections_html += f'<section><h2>{section["title"]}</h2>{section_html}</section>\n'

    # Get template values with defaults
    layout = template.get("layout", {})
    header = template.get("header", {})
    typography = template.get("typography", {})
    colors = template.get("colors", {})
    special = template.get("special_features", {})

    # Build CSS variables
    css_vars = f"""
        :root {{
            --primary-color: {colors.get('primary', '#2C3E50')};
            --secondary-color: {colors.get('secondary', '#7F8C8D')};
            --body-color: {colors.get('body', '#333333')};
            --body-size: {typography.get('body_size', '11pt')};
            --margin-top: {layout.get('margins', {}).get('top', '0.5in')};
            --margin-bottom: {layout.get('margins', {}).get('bottom', '0.5in')};
            --margin-left: {layout.get('margins', {}).get('left', '0.5in')};
            --margin-right: {layout.get('margins', {}).get('right', '0.5in')};
        }}

        @page {{
            size: {layout.get('page_size', 'letter')};
            margin: var(--margin-top) var(--margin-right) var(--margin-bottom) var(--margin-left);
        }}
    """

    # Build body classes
    body_classes = [
        f"layout-{layout.get('type', 'single-column')}",
        f"style-{typography.get('style', 'modern')}",
        f"font-{typography.get('font_family', 'sans-serif')}"
    ]
    if special.get('has_dividers'):
        body_classes.append('has-dividers')

    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume_data.get('name', 'Resume')} - Resume</title>
    <style>
{css_vars}
{css_content}
    </style>
</head>
<body class="{' '.join(body_classes)}">
    <header class="header name-{header.get('name_position', 'left')}">
        <h1 class="name size-{header.get('name_size', 'large')}">{resume_data.get('name', '')}</h1>
        <div class="contact contact-{header.get('contact_layout', 'single-line')}">
            {resume_data.get('contact_info', '')}
        </div>
    </header>

    <main class="content">
        {sections_html}
    </main>
</body>
</html>"""

    return html


def get_pdf_page_count(pdf_path: Path) -> int:
    """Get the number of pages in a PDF file."""
    try:
        # Try pypdf first
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except ImportError:
        pass

    # Fall back to pdfinfo command
    try:
        result = subprocess.run(
            ['pdfinfo', str(pdf_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Pages:'):
                    return int(line.split(':')[1].strip())
    except FileNotFoundError:
        pass

    # Can't determine page count
    return -1


def generate_with_weasyprint(html_content: str, output_path: Path, max_pages: int = 0) -> bool:
    """Generate PDF using WeasyPrint (module or CLI). Optionally auto-scale to fit max_pages."""
    mode = get_weasyprint_mode()
    if not mode:
        print("Error: WeasyPrint not available", file=sys.stderr)
        return False

    # Font size scaling factors to try (start at 100%, decrease)
    scale_factors = [1.0, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70] if max_pages > 0 else [1.0]

    for scale in scale_factors:
        # Inject scale factor into HTML
        if scale != 1.0:
            scaled_html = html_content.replace(
                'body {',
                f'body {{ font-size: calc(var(--body-size, 11pt) * {scale});'
            ).replace(
                'font-size: calc(var(--body-size, 11pt) * {scale});',
                f'font-size: calc(var(--body-size, 11pt) * {scale}); /* scaled */'
            )
            # Also scale line-height slightly
            scaled_html = scaled_html.replace(
                'line-height: 1.4;',
                f'line-height: {max(1.2, 1.4 * scale)};'
            )
        else:
            scaled_html = html_content

        try:
            if mode == "module":
                from weasyprint import HTML
                HTML(string=scaled_html).write_pdf(str(output_path))
            else:
                # CLI mode - write HTML to temp file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                    f.write(scaled_html)
                    temp_html = f.name

                result = subprocess.run(
                    [shutil.which("weasyprint"), temp_html, str(output_path)],
                    capture_output=True,
                    text=True
                )
                os.unlink(temp_html)

                if result.returncode != 0:
                    print(f"Error: WeasyPrint CLI failed: {result.stderr}", file=sys.stderr)
                    return False

            # Check page count if max_pages specified
            if max_pages > 0:
                page_count = get_pdf_page_count(output_path)
                if page_count > 0 and page_count <= max_pages:
                    print(f"PDF fits in {page_count} page(s) at {int(scale * 100)}% scale")
                    return True
                elif page_count > 0:
                    print(f"PDF has {page_count} pages at {int(scale * 100)}% scale, trying smaller...")
                    continue

            return True

        except Exception as e:
            print(f"Error: WeasyPrint generation failed: {e}", file=sys.stderr)
            return False

    # Exhausted all scale factors
    print(f"Warning: Could not fit resume in {max_pages} pages. Using smallest scale.", file=sys.stderr)
    return True


def generate_typst_source(resume_data: dict, template: dict) -> str:
    """Generate Typst source from resume data and template."""
    colors = template.get("colors", {})
    typography = template.get("typography", {})
    layout = template.get("layout", {})

    # Convert colors from hex to Typst format
    primary = colors.get("primary", "#2C3E50").lstrip("#")
    secondary = colors.get("secondary", "#7F8C8D").lstrip("#")

    # Build sections
    sections_typ = ""
    for section in resume_data.get("sections", []):
        section_content = section["content"]
        # Convert markdown bullets to Typst list
        section_content = re.sub(r'^- (.+)$', r'- \1', section_content, flags=re.MULTILINE)
        section_content = re.sub(r'\*\*(.+?)\*\*', r'*\1*', section_content)
        sections_typ += f"""
== {section["title"]}
{section_content}
"""

    typst_source = f"""#set page(
  paper: "{layout.get('page_size', 'us-letter')}",
  margin: (
    top: {layout.get('margins', {}).get('top', '0.5in')},
    bottom: {layout.get('margins', {}).get('bottom', '0.5in')},
    left: {layout.get('margins', {}).get('left', '0.5in')},
    right: {layout.get('margins', {}).get('right', '0.5in')},
  ),
)

#set text(
  font: "{"Helvetica" if typography.get('font_family') == 'sans-serif' else "Georgia"}",
  size: {typography.get('body_size', '11pt')},
)

#let primary = rgb("#{primary}")
#let secondary = rgb("#{secondary}")

#align({layout.get('header', {}).get('name_position', 'left')})[
  #text(size: 24pt, weight: "bold", fill: primary)[{resume_data.get('name', '')}]
]

#text(fill: secondary)[{resume_data.get('contact_info', '')}]

#line(length: 100%, stroke: 0.5pt + secondary)

{sections_typ}
"""
    return typst_source


def generate_with_typst(resume_data: dict, template: dict, output_path: Path) -> bool:
    """Generate PDF using Typst."""
    try:
        typst_source = generate_typst_source(resume_data, template)

        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.typ', delete=False) as f:
            f.write(typst_source)
            temp_path = f.name

        # Run Typst
        result = subprocess.run(
            ['typst', 'compile', temp_path, str(output_path)],
            capture_output=True,
            text=True
        )

        # Clean up
        os.unlink(temp_path)

        if result.returncode != 0:
            print(f"Error: Typst compilation failed: {result.stderr}", file=sys.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error: Typst generation failed: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF resume from Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit codes:
  0 - Success
  1 - No PDF engine available
  2 - Invalid input
  3 - Template error
  4 - Generation failed

Examples:
  python3 tools/generate-pdf.py resume.md output.pdf
  python3 tools/generate-pdf.py resume.md output.pdf --template custom-template.yaml
        """
    )
    parser.add_argument("input", help="Path to input Markdown file")
    parser.add_argument("output", help="Path for output PDF file")
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help=f"Path to template YAML (default: {DEFAULT_TEMPLATE_PATH})"
    )
    parser.add_argument(
        "--engine",
        choices=["weasyprint", "typst", "auto"],
        default="auto",
        help="PDF engine to use (default: auto-detect)"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Maximum number of pages. Auto-scales font to fit. (default: 0 = no limit)"
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    template_path = Path(args.template)

    # Detect or validate engine
    if args.engine == "auto":
        engine = detect_engine()
        if not engine:
            print("Error: No PDF engine available.", file=sys.stderr)
            print("Install one of:", file=sys.stderr)
            print("  - WeasyPrint: pip install weasyprint", file=sys.stderr)
            print("  - Typst: https://typst.app/", file=sys.stderr)
            sys.exit(EXIT_NO_ENGINE)
    else:
        engine = args.engine
        if engine == "weasyprint" and not check_weasyprint():
            print("Error: WeasyPrint not available. Install with: pip install weasyprint", file=sys.stderr)
            sys.exit(EXIT_NO_ENGINE)
        if engine == "typst" and not check_typst():
            print("Error: Typst not available. Install from: https://typst.app/", file=sys.stderr)
            sys.exit(EXIT_NO_ENGINE)

    print(f"Using PDF engine: {engine}")

    # Load template
    template = load_template(template_path)

    # Read and parse Markdown
    markdown_content = read_markdown(input_path)
    resume_data = parse_resume_markdown(markdown_content)

    if not resume_data.get("name"):
        print("Warning: Could not extract name from resume. Using filename.", file=sys.stderr)
        resume_data["name"] = input_path.stem

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate PDF
    success = False
    if engine == "weasyprint":
        html_content = generate_styled_html(resume_data, template)
        success = generate_with_weasyprint(html_content, output_path, max_pages=args.max_pages)
    elif engine == "typst":
        success = generate_with_typst(resume_data, template, output_path)

    if success:
        print(f"PDF generated: {output_path}")
        sys.exit(EXIT_SUCCESS)
    else:
        sys.exit(EXIT_GENERATION_FAILED)


if __name__ == "__main__":
    main()
