import sys
import os
from .agentic_ai import CodingAgent
from . import workflow as wf


def print_banner(dir_path):
    print()
    print("  ULTRON Coding Agent")
    print("  " + "-" * 50)
    print(f"  Working in: {dir_path}")
    print("  Commands: /exit  /read  /write  /list  /delete  /help")
    print()


def print_help():
    print("  Natural language: describe what you want to build/edit/debug")
    print("  Commands:")
    print("    /exit              Exit the coding agent")
    print("    /read <file>       Read a file's contents")
    print("    /write <file>      Write content to a file (then paste, Ctrl+Z to end)")
    print("    /list [dir]        List files in directory")
    print("    /delete <file>     Delete a file")
    print("    /analyze <file>    Show file stats (size, lines, extension)")
    print("    /help              Show this help")
    print()


def handle_command(cmd: str, agent: CodingAgent):
    parts = cmd.split(maxsplit=1)
    action = parts[0].lower()
    target = parts[1].strip() if len(parts) > 1 else "."

    if action == "/read":
        result = wf.read_file(target)
        if result["success"]:
            print(f"\n  --- {target} ---")
            print(f"  {result['content']}")
            if not result["content"].endswith("\n"):
                print()
        else:
            print(f"\n  Error: {result['error']}")
        return True

    if action == "/write":
        print(f"\n  Paste the file content. Press Enter, then Ctrl+Z then Enter to finish:")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        content = "\n".join(lines)
        result = wf.write_file(target, content)
        if result["success"]:
            print(f"  \u2713 {target} written")
        else:
            print(f"  Error: {result['error']}")
        return True

    if action == "/list":
        result = wf.list_files(target)
        if result["success"]:
            print(f"\n  Files in {target}/:")
            for f in result["files"]:
                print(f"    {f}")
            if not result["files"]:
                print("    (empty)")
        else:
            # Try as read_directory
            r2 = wf.read_directory(target)
            if r2["success"]:
                print(f"\n  {target}/:")
                for e in r2["entries"]:
                    marker = "/" if e["type"] == "directory" else ""
                    print(f"    {e['name']}{marker}")
            else:
                print(f"  Error: {r2['error']}")
        return True

    if action == "/delete":
        result = wf.delete_file(target)
        if result["success"]:
            print(f"  \u2713 {target} deleted")
        else:
            print(f"  Error: {result['error']}")
        return True

    if action == "/analyze":
        result = wf.analyze_file(target)
        if result["success"]:
            print(f"\n  {target}:")
            print(f"    Size: {result['size_bytes']} bytes")
            print(f"    Lines: {result['lines']}")
            print(f"    Type: {result['extension'] or '(no extension)'}")
        else:
            print(f"  Error: {result['error']}")
        return True

    return False


def display_result(result: dict):
    rtype = result.get("type", "")

    if rtype == "clarify":
        print(f"\n  I need some clarification:")
        for q in result.get("questions", []):
            print(f"    ? {q}")
        print()
        return

    explanation = result.get("explanation") or result.get("response") or result.get("root_cause", "")

    if rtype == "answer":
        print(f"\n  {explanation}\n")
        return

    if result.get("root_cause"):
        print(f"\n  Root cause: {result['root_cause']}")

    if explanation:
        for line in explanation.split("\n"):
            if line.strip():
                print(f"  {line}")

    saved = result.get("saved", [])
    if saved:
        print(f"\n  \u2713 Written to disk ({len(saved)} files):")
        for path in saved:
            print(f"    {path}")
        print()

    files = result.get("files", {})
    if files and not saved:
        print(f"\n  Generated {len(files)} files:")
        for path in files:
            print(f"    {path}")
        print()


def main():
    start_dir = os.getcwd()
    agent = CodingAgent(project_dir=start_dir)
    print_banner(start_dir)
    sys.stdout.flush()

    while True:
        try:
            raw = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye!")
            break

        if not raw:
            continue

        if raw == "/exit":
            print("\n  Goodbye!")
            break

        if raw == "/help":
            print_help()
            continue

        if raw.startswith("/"):
            handled = handle_command(raw, agent)
            if handled:
                continue
            print(f"  Unknown command: {raw.split()[0]}. Type /help")
            continue

        print()
        result = agent.process(raw)
        display_result(result)


if __name__ == "__main__":
    main()
