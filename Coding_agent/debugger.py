from . import providers

SYSTEM = """You are an expert debugger. Given code and a description of the problem, find the root cause and provide the fix.

Output ONLY a JSON object:
{
  "files": {
    "path/to/file.js": "corrected full file content"
  },
  "root_cause": "Explanation of what caused the bug",
  "explanation": "How the fix resolves it"
}

Rules:
- Identify the exact line or section causing the issue
- Explain why the bug occurs
- Provide the complete corrected file, not just the fix line
- Consider edge cases that might also be broken"""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    files = project.get("files", {})

    if not files:
        return {"files": {}, "root_cause": "No project files to debug.", "explanation": ""}

    parts = [f"Issue: {query}"]
    parts.append("\nProject files:")
    for path, content in files.items():
        parts.append(f"\n--- {path} ---\n{content}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["debugger"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.2)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        import json
        data = json.loads(result)
        return {
            "files": data.get("files", {}),
            "root_cause": data.get("root_cause", ""),
            "explanation": data.get("explanation", ""),
        }
    except Exception as e:
        return {"files": {}, "root_cause": f"Debugger error: {e}", "explanation": ""}
