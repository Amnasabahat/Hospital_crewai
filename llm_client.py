import os
import requests
from dotenv import load_dotenv
import openai

load_dotenv()

provider = os.getenv("PROVIDER", "huggingface")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

def call_api(messages):
    if provider == "openai":
        return call_openai(messages)
    elif provider == "groq":
        return call_groq(messages)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# 🔹 OpenAI
def call_openai(messages):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=512
    )
    return response["choices"][0]["message"]["content"]

# 🔹 Groq
def call_groq(messages):
    openai.api_key = GROQ_API_KEY
    user_input = "\n".join([m["content"] for m in messages if m["role"] == "user"])
    response = openai.ChatCompletion.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": user_input}],
        temperature=0.2,
        max_tokens=512
    )
    return response["choices"][0]["message"]["content"]

def generate_response(messages):
    return call_api(messages)
