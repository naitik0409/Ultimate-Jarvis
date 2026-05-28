import os
import shutil

SKIP_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build',
             '.next', '.nuxt', '.cache', 'target', '.tox', '.eggs', '.gitlab',
             '.vscode', '.idea', '.svelte-kit', '.vercel'}
TEXT_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss',
                   '.json', '.md', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf',
                   '.env', '.txt', '.xml', '.svg', '.sql', '.rs', '.go', '.java',
                   '.rb', '.php', '.sh', '.bat', '.ps1', '.vue', '.svelte', '.astro'}


def resolve_path(target: str) -> str:
    return os.path.abspath(target)


def read_file(path: str) -> dict:
    try:
        full = resolve_path(path)
        if not os.path.isfile(full):
            return {"success": False, "error": f"File not found: {path}"}
        with open(full, "r", encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "path": path, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}


def write_file(path: str, content: str) -> dict:
    try:
        full = resolve_path(path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "path": path, "action": "created" if not os.path.exists(full) else "updated"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def edit_file(path: str, old_string: str, new_string: str) -> dict:
    try:
        full = resolve_path(path)
        if not os.path.isfile(full):
            return {"success": False, "error": f"File not found: {path}"}
        with open(full, "r", encoding="utf-8") as f:
            content = f.read()
        if old_string not in content:
            return {"success": False, "error": f"Text not found in {path}"}
        new_content = content.replace(old_string, new_string, 1)
        with open(full, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"success": True, "path": path, "action": "edited"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_file(path: str) -> dict:
    try:
        full = resolve_path(path)
        if not os.path.isfile(full):
            return {"success": False, "error": f"File not found: {path}"}
        os.remove(full)
        return {"success": True, "path": path, "action": "deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_files(directory: str = ".") -> dict:
    try:
        full = resolve_path(directory)
        if not os.path.isdir(full):
            return {"success": False, "error": f"Directory not found: {directory}"}
        files = []
        for root, dirs, filenames in os.walk(full):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in filenames:
                rel = os.path.relpath(os.path.join(root, f), full)
                files.append(rel)
        return {"success": True, "directory": directory, "files": sorted(files)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def read_directory(directory: str = ".") -> dict:
    try:
        full = resolve_path(directory)
        if not os.path.isdir(full):
            return {"success": False, "error": f"Directory not found: {directory}"}
        entries = []
        for item in sorted(os.listdir(full)):
            item_path = os.path.join(full, item)
            entries.append({
                "name": item,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0,
            })
        return {"success": True, "directory": directory, "entries": entries}
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_file(path: str) -> dict:
    try:
        full = resolve_path(path)
        if not os.path.isfile(full):
            return {"success": False, "error": f"File not found: {path}"}
        size = os.path.getsize(full)
        ext = os.path.splitext(full)[1]
        lines = 0
        with open(full, "r", encoding="utf-8") as f:
            lines = sum(1 for _ in f)
        return {
            "success": True,
            "path": path,
            "size_bytes": size,
            "extension": ext,
            "lines": lines,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def move_file(src: str, dst: str) -> dict:
    try:
        src_full = resolve_path(src)
        dst_full = resolve_path(dst)
        if not os.path.isfile(src_full):
            return {"success": False, "error": f"Source file not found: {src}"}
        os.makedirs(os.path.dirname(dst_full), exist_ok=True)
        shutil.move(src_full, dst_full)
        return {"success": True, "source": src, "destination": dst, "action": "moved"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def copy_file(src: str, dst: str) -> dict:
    try:
        src_full = resolve_path(src)
        dst_full = resolve_path(dst)
        if not os.path.isfile(src_full):
            return {"success": False, "error": f"Source file not found: {src}"}
        os.makedirs(os.path.dirname(dst_full), exist_ok=True)
        shutil.copy2(src_full, dst_full)
        return {"success": True, "source": src, "destination": dst, "action": "copied"}
    except Exception as e:
        return {"success": False, "error": str(e)}
