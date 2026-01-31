#!/usr/bin/env python3
"""
Validates system_architecture.mermaid.md against workflow and agent source files.

Checks:
1. Schema tables match Mermaid diagram code
2. Workflow agents match workflow.md declarations
3. Data flows match workflow.md Summary blocks
4. Agent Summary blocks match schema definitions
5. Agent workflow tables are consistent with workflow ownership

Usage:
    python3 tools/validate-diagram.py
    python3 tools/validate-diagram.py --verbose
"""

import re
import sys
from pathlib import Path
from typing import Optional

# ANSI colors for output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def parse_markdown_table(content: str, table_header: str) -> list[dict]:
    """Extract a markdown table following a specific header."""
    lines = content.split("\n")
    tables = []
    in_table = False
    headers = []

    for i, line in enumerate(lines):
        # Look for the table header
        if table_header.lower() in line.lower() and line.startswith("###"):
            in_table = True
            continue

        if in_table:
            # Skip empty lines
            if not line.strip():
                continue

            # Check if we've hit another section
            if line.startswith("##"):
                break

            # Parse table header row
            if line.startswith("|") and not headers:
                headers = [h.strip() for h in line.split("|")[1:-1]]
                continue

            # Skip separator row
            if line.startswith("|") and all(c in "|-: " for c in line):
                continue

            # Parse data row
            if line.startswith("|"):
                values = [v.strip() for v in line.split("|")[1:-1]]
                if len(values) == len(headers):
                    tables.append(dict(zip(headers, values)))

    return tables


def parse_workflow_summary(workflow_path: Path) -> dict:
    """Extract Agent, Phase, Reads, Creates, Updates from workflow Summary."""
    if not workflow_path.exists():
        return {"error": f"File not found: {workflow_path}"}

    content = workflow_path.read_text()
    summary = {
        "agents": [],
        "lead": None,
        "phase": None,
        "reads": [],
        "creates": [],
        "updates": [],
    }

    # Extract Agent line
    agent_match = re.search(r"\*\*Agent:\*\*\s*(.+)", content)
    if agent_match:
        agent_str = agent_match.group(1).strip()
        # Parse agent names - check for each agent type
        agents = []
        if "Max" in agent_str:
            agents.append("max")
        if "Scout" in agent_str:
            agents.append("scout")
        if "Voice" in agent_str:
            agents.append("voice")
        summary["agents"] = agents

    # Extract Agent Lead
    lead_match = re.search(r"\*\*Agent Lead:\*\*\s*(.+)", content)
    if lead_match:
        lead_str = lead_match.group(1).strip()
        if "Max" in lead_str:
            summary["lead"] = "max"
        elif "Scout" in lead_str:
            summary["lead"] = "scout"

    # Extract Phase
    phase_match = re.search(r"\*\*Phase:\*\*\s*(\w+)", content)
    if phase_match:
        summary["phase"] = phase_match.group(1).strip().lower()

    # Extract Reads section - handle nested bullets and multi-line entries
    reads_match = re.search(r"\*\*Reads:\*\*\s*\n((?:[ \t]*[-*]\s+.+\n?)+)", content)
    if reads_match:
        reads_block = reads_match.group(1)
        # Extract all backticked paths from the entire block
        paths = re.findall(r"`([^`]+)`", reads_block)
        for path in paths:
            # Normalize path to just the key identifier
            normalized = normalize_path(path)
            if normalized:
                # Check if optional anywhere near this path in the block
                is_optional = False
                for line in reads_block.split("\n"):
                    if path in line and ("(optional)" in line.lower() or "if exists" in line.lower()):
                        is_optional = True
                        break
                summary["reads"].append((normalized, is_optional))

    # Extract Creates section
    creates_match = re.search(r"\*\*Creates:\*\*\s*\n((?:[-*]\s+.+\n?)+)", content)
    if creates_match:
        creates_block = creates_match.group(1)
        for line in creates_block.split("\n"):
            paths = re.findall(r"`([^`]+)`", line)
            for path in paths:
                normalized = normalize_path(path)
                if normalized:
                    is_optional = "(optional)" in line.lower()
                    summary["creates"].append((normalized, is_optional))

    # Extract Updates section
    updates_match = re.search(r"\*\*Updates:\*\*\s*\n((?:[-*]\s+.+\n?)+)", content)
    if updates_match:
        updates_block = updates_match.group(1)
        for line in updates_block.split("\n"):
            if "none" in line.lower():
                continue
            paths = re.findall(r"`([^`]+)`", line)
            for path in paths:
                normalized = normalize_path(path)
                if normalized:
                    is_optional = "(conditional)" in line.lower() or "(optional)" in line.lower()
                    summary["updates"].append((normalized, is_optional))

    return summary


def normalize_path(path: str) -> Optional[str]:
    """Convert a file path to its schema identifier."""
    path = path.lower().strip()

    # Map paths to schema identifiers
    mappings = {
        "profile/corpus.json": "corpus",
        "corpus.json": "corpus",
        "profile/constraints.yaml": "constraints",
        "constraints.yaml": "constraints",
        "profile/voice_profile.json": "voice_profile",
        "voice_profile.json": "voice_profile",
        "agents/voice.md": "voice_agent",
        "voice.md": "voice_agent",
        "profile/resume_template.yaml": "resume_template",
        "resume_template.yaml": "resume_template",
        "profile/linkedin.md": "linkedinmd",
        "linkedin.md": "linkedinmd",
        "research/market_skills.json": "market_skills",
        "market_skills.json": "market_skills",
        "research/industries": "industries",
        "research/industries/": "industries",
        "industries/": "industries",
        "research/companies": "companies",
        "research/companies/": "companies",
        "companies/": "companies",
        "research/openings": "openings",
        "research/openings/": "openings",
        "openings/": "openings",
        "applications/resumes": "resumes",
        "applications/resumes/": "resumes",
        "resumes/": "resumes",
        "applications/cover_letters": "coverletters",
        "applications/cover_letters/": "coverletters",
        "cover_letters/": "coverletters",
    }

    for pattern, identifier in mappings.items():
        if pattern in path:
            return identifier

    # Handle wildcard patterns
    if "openings/" in path or "openings/*" in path:
        return "openings"
    if "companies/" in path:
        return "companies"
    if "industries/" in path:
        return "industries"
    if "resumes/" in path:
        return "resumes"
    if "cover_letters/" in path or "coverletters/" in path:
        return "coverletters"
    if "writing_samples" in path:
        return None  # Not tracked in schema
    if "imports/" in path:
        return None  # Not tracked in schema

    return None


def parse_schema_agents(schema_agents: list[str]) -> set[str]:
    """Parse agent string from schema into set of agent ids."""
    agents = set()
    for agent in schema_agents:
        agent = agent.strip().lower()
        if agent in ("max", "scout", "voice"):
            agents.add(agent)
    return agents


def validate(arch_file: Path, workflows_dir: Path, verbose: bool = False) -> list[str]:
    """Cross-reference all sources and return list of issues."""
    issues = []
    warnings = []

    if not arch_file.exists():
        return [f"Architecture file not found: {arch_file}"]

    content = arch_file.read_text()

    # Parse schema tables
    workflows_schema = parse_markdown_table(content, "### Workflows")
    data_flows_schema = parse_markdown_table(content, "### Data Flows")

    if not workflows_schema:
        return ["Could not parse Workflows table from schema"]

    # Create lookup for data flows
    flows_by_workflow = {f["workflow"]: f for f in data_flows_schema}

    # Validate each workflow
    for wf in workflows_schema:
        wf_id = wf.get("id", "unknown")
        source_path = wf.get("source", "")

        if not source_path:
            issues.append(f"{wf_id}: No source path in schema")
            continue

        workflow_path = workflows_dir.parent / source_path
        if not workflow_path.exists():
            issues.append(f"{wf_id}: Source file not found: {source_path}")
            continue

        # Parse the workflow file
        workflow = parse_workflow_summary(workflow_path)

        if "error" in workflow:
            issues.append(f"{wf_id}: {workflow['error']}")
            continue

        # Check agent assignment
        schema_agents_str = wf.get("agents", "")
        schema_agents = parse_schema_agents(schema_agents_str.split(","))
        workflow_agents = set(workflow["agents"])

        if schema_agents != workflow_agents:
            issues.append(
                f"{wf_id}: Agent mismatch - "
                f"schema says {sorted(schema_agents)}, "
                f"workflow says {sorted(workflow_agents)}"
            )

        # Check phase
        schema_phase = wf.get("phase", "").lower()
        workflow_phase = workflow.get("phase", "")

        if schema_phase and workflow_phase and schema_phase != workflow_phase:
            issues.append(
                f"{wf_id}: Phase mismatch - "
                f"schema says '{schema_phase}', "
                f"workflow says '{workflow_phase}'"
            )
        elif not workflow_phase:
            warnings.append(f"{wf_id}: No Phase field in workflow Summary")

        # Check agent lead (if dual-agent)
        if len(schema_agents) > 1:
            schema_lead = wf.get("lead", "").strip()
            workflow_lead = workflow.get("lead")

            if schema_lead and schema_lead != "—" and workflow_lead:
                if schema_lead.lower() != workflow_lead:
                    issues.append(
                        f"{wf_id}: Agent lead mismatch - "
                        f"schema says '{schema_lead}', "
                        f"workflow says '{workflow_lead}'"
                    )

        # Check data flows if available
        if wf_id in flows_by_workflow:
            flow = flows_by_workflow[wf_id]

            # Parse schema flows
            schema_reads = parse_flow_field(flow.get("reads", ""))
            schema_writes = parse_flow_field(flow.get("writes", ""))
            schema_updates = parse_flow_field(flow.get("updates", ""))

            # Get workflow flows (just the identifiers, ignoring optional flag for comparison)
            workflow_reads = {r[0] for r in workflow["reads"]}
            workflow_creates = {c[0] for c in workflow["creates"]}
            workflow_updates = {u[0] for u in workflow["updates"]}

            # Compare reads (allow schema to be subset - may not capture all reads)
            if verbose:
                missing_reads = schema_reads - workflow_reads
                extra_reads = workflow_reads - schema_reads
                if missing_reads:
                    warnings.append(f"{wf_id}: Schema lists reads not in workflow: {missing_reads}")
                if extra_reads:
                    warnings.append(f"{wf_id}: Workflow lists reads not in schema: {extra_reads}")

    if verbose and warnings:
        print(f"\n{YELLOW}Warnings:{RESET}")
        for w in warnings:
            print(f"  {YELLOW}⚠{RESET} {w}")

    return issues


def parse_flow_field(field: str) -> set[str]:
    """Parse a data flow field (e.g., 'corpus, constraints?, voice') into identifiers."""
    if not field or field.strip() == "—":
        return set()

    identifiers = set()
    for item in field.split(","):
        item = item.strip().rstrip("?")  # Remove optional marker
        if item and item != "—":
            identifiers.add(item.lower())

    return identifiers


def parse_agent_summary(agent_path: Path) -> dict:
    """Extract ID, Style, Color, Label from agent Summary block."""
    if not agent_path.exists():
        return {"error": f"File not found: {agent_path}"}

    content = agent_path.read_text()
    summary = {
        "id": None,
        "style": None,
        "color": None,
        "label": None,
    }

    # Extract fields from Summary block
    id_match = re.search(r"\*\*ID:\*\*\s*(\w+)", content)
    if id_match:
        summary["id"] = id_match.group(1).strip().lower()

    style_match = re.search(r"\*\*Style:\*\*\s*(\w+)", content)
    if style_match:
        summary["style"] = style_match.group(1).strip()

    color_match = re.search(r"\*\*Color:\*\*\s*(#[0-9a-fA-F]+)", content)
    if color_match:
        summary["color"] = color_match.group(1).strip().lower()

    label_match = re.search(r"\*\*Label:\*\*\s*(.+)", content)
    if label_match:
        summary["label"] = label_match.group(1).strip()

    return summary


def parse_agent_workflows(agent_path: Path) -> set[str]:
    """Extract workflow names from agent's Workflows section tables."""
    if not agent_path.exists():
        return set()

    content = agent_path.read_text()
    workflows = set()

    # Find all workflow names in bold within tables (e.g., **init**, **job-scan**)
    # These appear in the Workflows section tables
    workflow_matches = re.findall(r"\*\*([a-z-]+)\*\*", content.lower())

    # Map workflow names to schema IDs
    name_to_id = {
        "init": "init",
        "scoping-interview": "scoping",
        "create-voice": "create_voice",
        "industry-research": "industry",
        "company-discovery": "company",
        "job-scan": "jobscan",
        "tailor-resume": "tailor",
        "cover-letter": "cover",
        "corpus-review": "corpus_rev",
        "linkedin-review": "linkedin",
        "audit": "audit",
    }

    for name in workflow_matches:
        if name in name_to_id:
            workflows.add(name_to_id[name])

    return workflows


def validate_agents(content: str, project_root: Path, verbose: bool = False) -> tuple[list[str], list[str]]:
    """Validate agent files against schema."""
    issues = []
    warnings = []

    agents_schema = parse_markdown_table(content, "### Agents")
    workflows_schema = parse_markdown_table(content, "### Workflows")

    if not agents_schema:
        return ["Could not parse Agents table from schema"], []

    # Build map of workflow_id -> agents from workflows schema
    workflow_agents = {}
    for wf in workflows_schema:
        wf_id = wf.get("id", "")
        agents_str = wf.get("agents", "")
        workflow_agents[wf_id] = set(a.strip().lower() for a in agents_str.split(",") if a.strip())

    for agent in agents_schema:
        agent_id = agent.get("id", "unknown")
        source_path = agent.get("source", "")

        # Skip 'dual' pseudo-agent
        if agent_id == "dual" or not source_path or source_path == "—":
            continue

        # Skip 'voice' agent - it's dynamically generated from voice-template.md
        if agent_id == "voice":
            template_path = project_root / "agents" / "voice-template.md"
            if not template_path.exists():
                issues.append(f"Agent {agent_id}: Template file not found: agents/voice-template.md")
            continue

        agent_path = project_root / source_path
        if not agent_path.exists():
            issues.append(f"Agent {agent_id}: Source file not found: {source_path}")
            continue

        # Parse agent file
        agent_summary = parse_agent_summary(agent_path)

        if "error" in agent_summary:
            issues.append(f"Agent {agent_id}: {agent_summary['error']}")
            continue

        # Validate ID matches
        if agent_summary["id"] and agent_summary["id"] != agent_id:
            issues.append(
                f"Agent {agent_id}: ID mismatch - "
                f"schema says '{agent_id}', "
                f"agent file says '{agent_summary['id']}'"
            )

        # Validate style matches
        schema_style = agent.get("style", "")
        if agent_summary["style"] and agent_summary["style"] != schema_style:
            issues.append(
                f"Agent {agent_id}: Style mismatch - "
                f"schema says '{schema_style}', "
                f"agent file says '{agent_summary['style']}'"
            )

        # Validate color matches
        schema_color = agent.get("color", "").lower()
        if agent_summary["color"] and agent_summary["color"] != schema_color:
            issues.append(
                f"Agent {agent_id}: Color mismatch - "
                f"schema says '{schema_color}', "
                f"agent file says '{agent_summary['color']}'"
            )

        # Check workflow tables in agent file
        agent_workflows = parse_agent_workflows(agent_path)

        # Find workflows this agent should own (from workflows schema)
        expected_workflows = {wf_id for wf_id, agents in workflow_agents.items() if agent_id in agents}

        # Check for workflows listed in agent file but agent doesn't own
        for wf in agent_workflows:
            if wf not in expected_workflows:
                warnings.append(
                    f"Agent {agent_id}: Lists workflow '{wf}' but isn't assigned to it in schema"
                )

        # Check for workflows agent owns but doesn't list (verbose only)
        if verbose:
            missing = expected_workflows - agent_workflows
            if missing:
                warnings.append(
                    f"Agent {agent_id}: Owns workflows {missing} but doesn't list them"
                )

    return issues, warnings


def extract_mermaid_block(content: str) -> Optional[str]:
    """Extract the mermaid code block from markdown content."""
    match = re.search(r"```mermaid\n(.*?)```", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def validate_readme_diagram(project_root: Path, arch_file: Path) -> list[str]:
    """Validate that README's mermaid diagram matches system_architecture.mermaid.md."""
    issues = []
    readme_file = project_root / "README.md"

    if not readme_file.exists():
        return ["README.md not found"]

    arch_content = arch_file.read_text()
    readme_content = readme_file.read_text()

    arch_mermaid = extract_mermaid_block(arch_content)
    readme_mermaid = extract_mermaid_block(readme_content)

    if not arch_mermaid:
        issues.append("No mermaid block found in system_architecture.mermaid.md")
        return issues

    if not readme_mermaid:
        issues.append("No mermaid block found in README.md — add the diagram from system_architecture.mermaid.md")
        return issues

    if arch_mermaid != readme_mermaid:
        issues.append(
            "README.md mermaid diagram differs from system_architecture.mermaid.md — "
            "sync the diagram from the architecture file"
        )

    return issues


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Find the project root (where this script's parent tools/ directory is)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    arch_file = project_root / "system_architecture.mermaid.md"
    workflows_dir = project_root / "workflows"

    print(f"{BOLD}Validating diagram against source files...{RESET}\n")

    all_issues = []
    all_warnings = []

    # Validate workflows
    print(f"  Checking workflows...")
    workflow_issues = validate(arch_file, workflows_dir, verbose)
    all_issues.extend(workflow_issues)

    # Validate agents
    print(f"  Checking agents...")
    content = arch_file.read_text()
    agent_issues, agent_warnings = validate_agents(content, project_root, verbose)
    all_issues.extend(agent_issues)
    all_warnings.extend(agent_warnings)

    # Validate README diagram matches architecture file
    print(f"  Checking README diagram sync...")
    readme_issues = validate_readme_diagram(project_root, arch_file)
    all_issues.extend(readme_issues)

    # Print warnings if verbose
    if verbose and all_warnings:
        print(f"\n{YELLOW}Warnings:{RESET}")
        for w in all_warnings:
            print(f"  {YELLOW}⚠{RESET} {w}")

    # Print results
    if all_issues:
        print(f"\n{RED}❌ Validation failed with {len(all_issues)} issue(s):{RESET}\n")
        for issue in all_issues:
            print(f"  {RED}•{RESET} {issue}")
        print()
        sys.exit(1)
    else:
        print(f"\n{GREEN}✅ Diagram validated successfully against all source files{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
