from . import providers

SYSTEM = """You are an expert code editor. Given a user's edit request and the current file contents, modify the code precisely.

Output ONLY a JSON object:
{
  "files": {
    "path/to/file.js": "updated full file content"
  },
  "explanation": "Brief description of what changed and why"
}

Rules:
- Preserve all existing functionality unless the edit explicitly changes it
- Follow the existing code style
- Make minimal, targeted changes
- Return the COMPLETE updated file, not just the diff"""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    files = project.get("files", {})

    if not files:
        return {"files": {}, "explanation": "No project files to edit."}

    parts = [f"Edit request: {query}"]
    parts.append("\nCurrent project files:")
    for path, content in files.items():
        parts.append(f"\n--- {path} ---\n{content}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["editing"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.2)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        import json
        data = json.loads(result)
        return {
            "files": data.get("files", {}),
            "explanation": data.get("explanation", ""),
        }
    except Exception as e:
        return {"files": {}, "explanation": f"Error applying edit: {e}"}
