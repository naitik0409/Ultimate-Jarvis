from . import providers

SYSTEM = """You are a coding assistant that asks clarifying questions when a user's request is ambiguous.

Given the user's query and current project context, generate specific questions to clarify what the user wants.

Output ONLY a JSON object:
{
  "questions": ["Question 1?", "Question 2?"],
  "explanation": "Brief summary of what's unclear"
}

Rules:
- Ask max 3 questions
- Be specific, not generic (not "what do you want?" but "do you want a REST API or GraphQL?")
- If the request is clear, return empty questions array"""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    files = project.get("files", {})
    history = session.get("conversation", [])

    parts = [f"Query: {query}"]

    if files:
        parts.append(f"\nExisting files:\n" + "\n".join(files.keys()))

    if history:
        last = history[-2:]
        ctx = "\n".join(f"{m['role']}: {m['content'][:200]}" for m in last)
        parts.append(f"\nRecent context:\n{ctx}")

    parts.append("\nIf this query is clear enough to act on, return empty questions. Otherwise ask specific questions.")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["asking"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.3)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        import json
        return json.loads(result)
    except Exception:
        return {"questions": [], "explanation": ""}
