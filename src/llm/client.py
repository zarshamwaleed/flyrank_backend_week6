import os
import json
import time
import random
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def load_prompt():
    prompt_path = os.path.join(
        os.path.dirname(__file__), 
        "prompts", 
        "classify-v1.md"
    )
    with open(prompt_path, "r") as f:
        return f.read()

def get_client():
    return OpenAI(
        base_url=os.environ.get("LLM_BASE_URL"),
        api_key=os.environ.get("LLM_API_KEY"),
        timeout=float(os.environ.get("LLM_TIMEOUT", 30)),
        max_retries=0
    )

def call_model(user_text: str):
    client = get_client()
    system_prompt = load_prompt()
    
    response = client.chat.completions.create(
        model=os.environ.get("LLM_MODEL"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        temperature=0.2,
        max_tokens=300
    )
    
    return response.choices[0].message.content