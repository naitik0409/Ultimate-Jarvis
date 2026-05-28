import os

_KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")

TECH_MAP = {
    "python": "Python",
    "flask": "Python",
    "django": "Python",
    "fastapi": "Python",
    "react": "React js",
    "reactjs": "React js",
    "react.js": "React js",
    "node": "Node",
    "nodejs": "Node",
    "express": "Node",
    "javascript": "Javascript",
    "js": "Javascript",
    "typescript": "Typescript",
    "ts": "Typescript",
    "html": "Html",
    "css": "Html",
    "sql": "Database",
    "mongodb": "Database",
    "postgresql": "Database",
    "mysql": "Database",
    "database": "Database",
}


def get_context(tech_stack: list) -> str:
    dirs = set()
    for tech in tech_stack:
        mapped = TECH_MAP.get(tech.lower())
        if mapped:
            dirs.add(mapped)

    for tech in tech_stack:
        for key, mapped in TECH_MAP.items():
            if key in tech.lower():
                dirs.add(mapped)

    parts = []
    for d in sorted(dirs):
        dir_path = os.path.join(_KNOWLEDGE_DIR, d)
        if os.path.isdir(dir_path):
            for fname in sorted(os.listdir(dir_path)):
                if fname.endswith(".md"):
                    fpath = os.path.join(dir_path, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        parts.append(f"--- {d}/{fname} ---\n{content[:4000]}")
                    except Exception:
                        pass

    return "\n\n".join(parts) if parts else ""
