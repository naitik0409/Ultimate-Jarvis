from . import providers

SYSTEM = """You are a versatile generative AI assistant for coding tasks.
You can write documentation, generate tests, add comments, refactor code, suggest improvements, or answer general coding questions.

Respond naturally. If the user asks a question, answer it clearly.
If they ask you to generate something (docs, tests, etc.), produce the full output."""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    files = project.get("files", {})
    history = session.get("conversation", [])

    parts = [f"Query: {query}"]

    if files:
        ctx = "\n".join(f"--- {path} ---\n{content[:500]}" for path, content in files.items())
        parts.append(f"\nProject files:\n{ctx}")

    if history:
        last = history[-4:]
        ctx = "\n".join(f"{m['role']}: {m['content'][:300]}" for m in last)
        parts.append(f"\nRecent conversation:\n{ctx}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["gen_ai"]

    try:
        response = providers.query(provider_name, model, messages, temperature=0.5)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {e}"}
