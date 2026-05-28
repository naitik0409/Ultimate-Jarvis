from . import providers

SYSTEM = """You are a multi-file project coordinator. When changes span multiple files, you ensure consistency across imports, type references, API contracts, and project structure.

Given a change request and the full project, plan the coordinated changes needed.

Output ONLY a JSON object:
{
  "plan": "Description of all coordinated changes",
  "files_to_modify": ["path/to/file1.js", "path/to/file2.js"],
  "dependency_order": ["file to edit first", "file to edit second"]
}

Rules:
- Identify all files affected by the change
- Ensure imports/exports stay consistent
- Check that function signatures, types, and API calls match across files
- Suggest the correct order of edits to avoid breaking dependencies"""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    files = project.get("files", {})

    parts = [f"Change request: {query}"]
    for path, content in files.items():
        parts.append(f"\n--- {path} ---\n{content}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["colaborator"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.2)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        import json
        return json.loads(result)
    except Exception as e:
        return {
            "plan": f"Coordination error: {e}",
            "files_to_modify": [],
            "dependency_order": []
        }
