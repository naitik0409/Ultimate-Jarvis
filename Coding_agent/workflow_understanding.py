from . import providers

SYSTEM = """You are a workflow analyst for software projects. Given a user's request, determine:
1. Project type (web app, CLI tool, library, API, script, etc.)
2. Appropriate tech stack and build tools
3. Project structure / file organization
4. Dependencies and packages needed
5. Development workflow (build, test, run commands)

Output ONLY a JSON object:
{
  "project_type": "web_app | cli | library | api | script | component | other",
  "tech_stack": ["react", "node", "express"],
  "build_tools": ["vite", "npm"],
  "structure": {
    "src/": "source code",
    "public/": "static assets"
  },
  "dependencies": {
    "react": "^18.0.0",
    "express": "^4.0.0"
  },
  "dev_commands": {
    "install": "npm install",
    "dev": "npm run dev",
    "build": "npm run build"
  }
}"""


def run(intent: dict, session: dict) -> dict:
    summary = intent.get("summary", "")
    tech_from_intent = intent.get("tech_stack", [])

    parts = [f"Request: {summary}"]
    if tech_from_intent:
        parts.append(f"Mentioned tech: {', '.join(tech_from_intent)}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "\n".join(parts)}
    ]

    models = providers.get_models()
    provider_name, model = models["workflow"]

    try:
        result = providers.query(provider_name, model, messages, temperature=0.2)
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1].rsplit("```", 1)[0]
        import json
        return json.loads(result)
    except Exception:
        return {
            "project_type": "other",
            "tech_stack": tech_from_intent or [],
            "build_tools": [],
            "structure": {},
            "dependencies": {},
            "dev_commands": {}
        }
