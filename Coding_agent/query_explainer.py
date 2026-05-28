import json
from . import providers

SYSTEM = """You are a query intent classifier for a coding assistant.
Your job is to analyze the user's query in the context of the current project and conversation history, then classify the intent.

Possible intents:
- new_project: User wants to create something new from scratch (app, script, component, etc.)
- edit: User wants to modify existing code (change behavior, style, add feature)
- debug: User has an error or unexpected behavior and needs it fixed
- question: User is asking a general coding question, not requesting code changes
- explain: User wants an explanation of existing code
- unclear: Cannot determine the intent

Respond with a JSON object:
{
  "intent": "new_project|edit|debug|question|explain|unclear",
  "summary": "One-line summary of what the user wants",
  "tech_stack": ["react", "node"] or null,
  "has_existing_context": true|false,
  "clarifying_questions": ["question?"] or []
}

Consider the conversation history and existing project files when classifying.
If the user references previously generated code, that is likely an edit or debug intent.
If no project exists yet, new_project is most likely."""


def run(query: str, session: dict) -> dict:
    project = session.get("project", {})
    has_files = bool(project.get("files"))
    history = session.get("conversation", [])

    context_parts = [f"Current query: {query}"]

    if has_files:
        files_list = "\n".join(project["files"].keys())
        context_parts.append(f"\nExisting project files:\n{files_list}")

    if history:
        last = history[-3:]
        ctx = "\n".join(f"{m['role']}: {m['content'][:200]}" for m in last)
        context_parts.append(f"\nRecent conversation:\n{ctx}")

    context_parts.append(
        "\nDetermine intent considering existing files. "
        "If files exist and query references them, it's edit/debug/explain. "
        "If no files exist, it's new_project."
    )

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(context_parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["explainer"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.1)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(result)
    except Exception as e:
        return {
            "intent": "unclear",
            "summary": query,
            "tech_stack": None,
            "has_existing_context": has_files,
            "clarifying_questions": []
        }
