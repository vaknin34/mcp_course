#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
TEMPLATES_DIR = Path(__file__).parent / "templates"


@mcp.tool()
async def analyze_file_changes(
    base_branch: str = "main",
    include_diff: bool = True,
    max_diff_lines: int = 500,
    last_diff_index: str | None = None,
) -> str:
    """
    Get the full diff and list of changed files in the current git repository.
    Uses pagination to handle large diffs.

    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
        max_diff_lines: Maximum number of diff lines to include (default: 500)
        last_diff_index: Index for pagination, if provided next diff will be fetched
    """
    try:
        # Get working directory - prioritize MCP context, then current working directory
        working_dir = os.getcwd()

        try:
            context = mcp.get_context()
            if context and hasattr(context, "session"):
                roots_result = await context.session.list_roots()
                if roots_result and hasattr(roots_result, "roots") and roots_result.roots:
                    # Use the first root as working directory
                    root_uri = roots_result.roots[0].uri
                    if hasattr(root_uri, "path") and root_uri.path:
                        working_dir = root_uri.path
        except Exception:
            # If MCP context fails, stick with current working directory
            pass

        # Get list of changed files
        files_result = subprocess.run(
            ["git", "diff", "--name-status", base_branch], cwd=working_dir, capture_output=True, text=True
        )

        if files_result.returncode != 0:
            return json.dumps({"error": f"Git command failed: {files_result.stderr}"})

        # Parse changed files
        changed_files = []
        for line in files_result.stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    status = parts[0]
                    filename = parts[1]
                    changed_files.append({"status": status, "file": filename})

        result = {"base_branch": base_branch, "changed_files": changed_files, "total_files": len(changed_files)}

        if include_diff and changed_files:
            # Get the diff
            diff_result = subprocess.run(["git", "diff", base_branch], cwd=working_dir, capture_output=True, text=True)

            if diff_result.returncode == 0:
                diff_lines = diff_result.stdout.split("\n")

                # Handle pagination
                start_line = 0
                if last_diff_index:
                    try:
                        start_line = int(last_diff_index)
                    except ValueError:
                        start_line = 0

                end_line = start_line + max_diff_lines
                paginated_diff = diff_lines[start_line:end_line]

                result["diff"] = "\n".join(paginated_diff)
                result["diff_lines_shown"] = len(paginated_diff)
                result["total_diff_lines"] = len(diff_lines)

                # Add pagination index if there are more lines
                if end_line < len(diff_lines):
                    result["next_diff_index"] = str(end_line)
                    result["has_more_diff"] = True
                else:
                    result["has_more_diff"] = False

                if len(paginated_diff) >= max_diff_lines:
                    result["truncated"] = True
            else:
                result["diff_error"] = diff_result.stderr

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to analyze changes: {str(e)}"})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    templates = {}
    for template_file in TEMPLATES_DIR.glob("*.md"):
        with open(template_file) as f:
            templates[template_file.stem] = f.read()
    return json.dumps({"templates": templates}, indent=4)


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.

    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    templates = await get_pr_templates()
    templates = json.loads(templates)["templates"]

    # Map change_type to templates
    if change_type in templates:
        selected_template = templates[change_type]
        suggestion = {
            "recommended_template": selected_template,
            "reasoning": f"Based on your analysis: '{changes_summary}', this appears to be a {change_type} change.",
            "template_content": selected_template["content"],
            "usage_hint": "Claude can help you fill out this template based on the specific changes in your PR.",
        }
        return json.dumps(suggestion, indent=2)
    else:
        available_types = ", ".join(templates.keys())
        return json.dumps(
            {"error": (f"No template found for change type '{change_type}'. Available types: {available_types}")},
            indent=2,
        )


if __name__ == "__main__":
    mcp.run()
