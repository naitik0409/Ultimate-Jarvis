import os
import json
from . import providers
from . import query_explainer
from . import workflow_understanding
from . import Reasoning
from . import Code_gen
from . import editing as edit_module
from . import debugger as debug_module
from . import asking
from . import gen_ai
from . import colaborator
from . import workflow as wf


class CodingAgent:
    def __init__(self, project_dir: str = None):
        self.base_dir = os.path.abspath(project_dir or os.getcwd())
        self.session = self._init_session()

    def _init_session(self) -> dict:
        session = {
            "conversation": [],
            "project": {
                "root": self.base_dir,
                "files": self._load_files(),
                "tech_stack": [],
            }
        }
        return session

    def _load_files(self) -> dict:
        result = wf.list_files(self.base_dir)
        files = {}
        seen = 0
        if result["success"]:
            for rel_path in result["files"]:
                ext = os.path.splitext(rel_path)[1].lower()
                if ext not in wf.TEXT_EXTENSIONS:
                    continue
                full = os.path.join(self.base_dir, rel_path)
                try:
                    size = os.path.getsize(full)
                    if size > 500 * 1024:
                        continue
                    with open(full, "r", encoding="utf-8") as f:
                        files[rel_path] = f.read()
                    seen += 1
                    if seen >= 200:
                        break
                except Exception:
                    pass
        return files

    def _write_to_disk(self, files: dict):
        saved = []
        for rel_path, content in files.items():
            full = os.path.join(self.base_dir, rel_path)
            res = wf.write_file(full, content)
            if res["success"]:
                saved.append(rel_path)
        return saved

    def process(self, user_input: str) -> dict:
        self.session["conversation"].append({"role": "user", "content": user_input})
        self.session["project"]["files"] = self._load_files()

        intent = query_explainer.run(user_input, self.session)
        intent_type = intent.get("intent", "unclear")

        if intent_type == "unclear":
            questions = asking.run(user_input, self.session)
            qs = questions.get("questions", [])
            result = {
                "type": "clarify",
                "explanation": questions.get("explanation", "Could you clarify what you need?"),
                "questions": qs,
            }
            self.session["conversation"].append({"role": "assistant", "content": json.dumps(result)})
            return result

        if intent_type == "question" or intent_type == "explain":
            result = gen_ai.run(user_input, self.session)
            response = result.get("response", "")
            self.session["conversation"].append({"role": "assistant", "content": response})
            return {"type": "answer", "response": response}

        if intent_type == "debug":
            return self._handle_debug(user_input)

        if intent_type == "edit":
            return self._handle_edit(user_input)

        return self._handle_new_project(intent)

    def _handle_new_project(self, intent: dict) -> dict:
        workflow = workflow_understanding.run(intent, self.session)
        self.session["project"]["tech_stack"] = workflow.get("tech_stack", [])

        plan = Reasoning.run(intent, self.session)
        explanation = plan.get("plan", "")

        code_result = Code_gen.run(plan, self.session)
        files = code_result.get("files", {})

        saved = []
        if files:
            saved = self._write_to_disk(files)
            self._reload_files()

        result = {
            "type": "new_project",
            "explanation": explanation,
            "files": files,
            "saved": saved,
            "directory": self.base_dir,
            "tech_stack": workflow.get("tech_stack", []),
            "dependencies": workflow.get("dependencies", {}),
            "dev_commands": workflow.get("dev_commands", {}),
        }
        self.session["conversation"].append({"role": "assistant", "content": json.dumps(result)})
        return result

    def _handle_edit(self, user_input: str) -> dict:
        edit_result = edit_module.run(user_input, self.session)
        files = edit_result.get("files", {})
        explanation = edit_result.get("explanation", "")

        saved = []
        if files:
            saved = self._write_to_disk(files)
            self._reload_files()

        result = {
            "type": "edit",
            "explanation": explanation,
            "files": files,
            "saved": saved,
        }
        self.session["conversation"].append({"role": "assistant", "content": json.dumps(result)})
        return result

    def _handle_debug(self, user_input: str) -> dict:
        debug_result = debug_module.run(user_input, self.session)
        files = debug_result.get("files", {})
        root_cause = debug_result.get("root_cause", "")
        explanation = debug_result.get("explanation", "")

        saved = []
        if files:
            saved = self._write_to_disk(files)
            self._reload_files()

        result = {
            "type": "debug",
            "root_cause": root_cause,
            "explanation": explanation,
            "files": files,
            "saved": saved,
        }
        self.session["conversation"].append({"role": "assistant", "content": json.dumps(result)})
        return result
