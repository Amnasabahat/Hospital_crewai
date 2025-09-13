import os
from openai import OpenAI as OpenAIClient
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# 🔑 Clients
openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 Multi-provider response generator
def generate_response(prompt, provider="openai", model=None):
    try:
        if provider == "openai":
            model = model or "gpt-4o-mini"
            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif provider == "groq":
            model = model or "llama-3.1-8b-instant"  # ✅ Updated model
            response = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content


        else:
            raise ValueError(f"❌ Unknown provider: {provider}")

    except Exception as e:
        error_msg = str(e)

        # ⚡ Auto fallback logic
        if provider == "openai":
            return generate_response(prompt, provider="groq")
        elif provider == "groq":
            return generate_response(prompt, provider="huggingface")
        else:
            return f"❌ Error: {error_msg}"

# 🎯 Example agent function
def process_complaint(complaint, provider="openai"):
    steps = []

    try:
        # Step 1: Triage
        triage = generate_response(f"Categorize and prioritize complaint:\n{complaint}", provider)
        steps.append({"agent": "Triage", "status": "completed", "output": triage})

        # Step 2: Investigation
        investigation = generate_response(f"Investigate details:\n{complaint}", provider)
        steps.append({"agent": "Investigation", "status": "completed", "output": investigation})

        # Step 3: Resolution
        resolution = generate_response(f"Propose resolution:\n{complaint}", provider)
        steps.append({"agent": "Resolution", "status": "completed", "output": resolution})

        return {"final": resolution, "steps": steps}

    except Exception as e:
        return {"final": f"Error: {str(e)}", "steps": steps}
