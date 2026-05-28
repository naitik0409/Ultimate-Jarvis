from dotenv import dotenv_values
import json
import os
import subprocess
import asyncio
from datetime import datetime

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech, TTS
from Backend.SpeechToText import SpeechRecognition

env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# DefaultMessage = f""" {Username}: Hello {Assistantname}, How are you?
# {Assistantname}: Welcome {Username}. I am doing well. How may I help you? """

subprocess_list = []
tts_process = None

def ensure_data_directory():
    os.makedirs("Data", exist_ok=True)

def initialize_chat_log():
    ensure_data_directory()
    chat_log_path = r'Data\ChatLog.json'

    try:
        if not os.path.exists(chat_log_path):
            with open(chat_log_path, "w", encoding='utf-8') as file:
                json.dump([], file)
            return []

        with open(chat_log_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)
            return chat_data if chat_data else []
    except (FileNotFoundError, json.JSONDecodeError):
        with open(chat_log_path, "w", encoding='utf-8') as file:
            json.dump([], file)
        return []

def save_chat_message(role: str, content: str):
    chat_data = initialize_chat_log()
    chat_data.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

    with open(r'Data\ChatLog.json', 'w', encoding='utf-8') as file:
        json.dump(chat_data, file, indent=2, ensure_ascii=False)

def get_formatted_chat_history() -> str:
    chat_data = initialize_chat_log()
    formatted_history = ""

    for entry in chat_data[-20:]:
        if entry["role"] == "user":
            formatted_history += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_history += f"{Assistantname}: {entry['content']}\n"

    return formatted_history

initialize_chat_log()

async def process_ai_query(query: str) -> str:
    try:
        Decision = FirstLayerDMM(query)

        ImageExecution = False
        ImageGenerationQuery = ""

        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])

        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        if ImageExecution:
            try:
                os.makedirs("Frontend/Files", exist_ok=True)
                with open(r'Frontend\Files\ImageGeneration.data', "w") as file:
                    file.write(f"{ImageGenerationQuery},True")

                subprocess.Popen(
                    ['python', r"Backend\ImageGeneration.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    shell=False,
                )
            except Exception as e:
                print(f"Error starting ImageGeneration.py: {e}")

        if G and R or R:
            chat_data = initialize_chat_log()
            Answer = RealtimeSearchEngine(Merged_query, chat_data)
        else:
            for queries in Decision:
                if "general" in queries:
                    QueryFinal = queries.replace("general", "")
                    Answer = ChatBot(QueryFinal)
                    break
                elif "realtime" in queries:
                    QueryFinal = queries.replace("realtime", "")
                    chat_data = initialize_chat_log()
                    Answer = RealtimeSearchEngine(QueryFinal, chat_data)
                    break
                elif "exit" in queries:
                    Answer = ChatBot("Okay, Bye!")
                    break
            else:
                Answer = ChatBot(query)

        return Answer

    except Exception as e:
        print(f"Error in AI processing: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

async def main():
    # print(f"\n{'='*50}")
    # print(f"ULTRON AI Assistant")
    # print(f"{'='*50}")
    # print(f"\nWelcome, {Username}! Speak 'exit' or 'quit' to end the session.\n")

    # print(DefaultMessage)
    # print()

    while True:
        try:
            print(f"\nListening...")
            user_input = SpeechRecognition().strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"\n{Assistantname}: Goodbye, {Username}! Have a great day!")
                save_chat_message("user", user_input)
                save_chat_message("assistant", "Goodbye! Have a great day!")
                break

            print(f"\n{Username}: {user_input}")
            save_chat_message("user", user_input)

            print(f"\n{Assistantname} is thinking...")

            response = await process_ai_query(user_input)

            save_chat_message("assistant", response)

            print(f"\n{Assistantname}: {response}")

            try:
                await TextToSpeech(response)
            except Exception as e:
                print(f"TTS Error: {e}")

        except KeyboardInterrupt:
            print(f"\n\nGoodbye, {Username}!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())
