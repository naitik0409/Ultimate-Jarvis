import openai
import itertools
from dotenv import dotenv_values

env = dotenv_values(".env")

providers = {}
_round_robin = {}

deepseek_key = env.get("DeepSeekAPIKey")
if deepseek_key:
    providers["deepseek"] = openai.OpenAI(
        api_key=deepseek_key,
        base_url="https://api.deepseek.com"
    )

openrouter_keys = [env.get(f"OpenRouterAPIKey{i}") for i in range(1, 7)]
openrouter_keys = [k for k in openrouter_keys if k]
if openrouter_keys:
    clients = [
        openai.OpenAI(api_key=k, base_url="https://openrouter.ai/api/v1")
        for k in openrouter_keys
    ]
    _round_robin["openrouter"] = itertools.cycle(clients)
    providers["openrouter"] = clients[0]

coding_groq_key = env.get("CodingGroqAPIKey") or env.get("GroqAPIKey")
if coding_groq_key:
    providers["groq"] = openai.OpenAI(
        api_key=coding_groq_key,
        base_url="https://api.groq.com/openai/v1"
    )

DEFAULT_MODELS = {
    "orchestrator":       ("openrouter", "deepseek/deepseek-chat"),
    "explainer":          ("groq",       "llama-3.3-70b-versatile"),
    "workflow":           ("openrouter", "deepseek/deepseek-r1"),
    "reasoning":          ("openrouter", "deepseek/deepseek-r1"),
    "code_gen":           ("openrouter", "qwen/qwen-2.5-coder-32b-instruct"),
    "editing":            ("openrouter", "qwen/qwen-2.5-coder-32b-instruct"),
    "debugger":           ("groq",       "llama-3.3-70b-versatile"),
    "asking":             ("groq",       "llama-3.3-70b-versatile"),
    "gen_ai":             ("openrouter", "deepseek/deepseek-chat"),
    "colaborator":        ("openrouter", "deepseek/deepseek-chat"),
}

ENV_MODEL_MAP = {
    "explainer":     "AgentExplainer",
    "workflow":      "AgentWorkflow",
    "reasoning":     "AgentReasoning",
    "code_gen":      "AgentCodeGen",
    "editing":       "AgentEditing",
    "debugger":      "AgentDebugger",
    "asking":        "AgentAsking",
    "gen_ai":        "AgentGenAI",
    "colaborator":   "AgentColaborator",
    "orchestrator":  "AgentOrchestrator",
}


def get_models():
    models = {}
    for module, (prov, model) in DEFAULT_MODELS.items():
        env_var = ENV_MODEL_MAP.get(module)
        if env_var and env.get(env_var):
            parts = env.get(env_var).split("/", 1)
            if len(parts) == 2:
                models[module] = (parts[0], parts[1])
            else:
                models[module] = (prov, parts[0])
        else:
            models[module] = (prov, model)
    return models


def _get_client(provider_name: str):
    if provider_name in _round_robin:
        return next(_round_robin[provider_name])
    client = providers.get(provider_name)
    if not client:
        raise ValueError(f"Provider '{provider_name}' is not configured. Check your API keys.")
    return client


def query(provider_name: str, model: str, messages: list, stream: bool = False, **kwargs):
    client = _get_client(provider_name)

    if stream:
        return client.chat.completions.create(
            model=model, messages=messages, stream=True, **kwargs
        )
    else:
        response = client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        return response.choices[0].message.content


def stream_to_console(provider_name: str, model: str, messages: list, **kwargs):
    stream = query(provider_name, model, messages, stream=True, **kwargs)
    full = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full += content
    print()
    return full
