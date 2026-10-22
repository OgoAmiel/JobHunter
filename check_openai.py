
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Create the OpenAI client
client = OpenAI()

# Send our first request
response = client.responses.create(
    model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
    instructions=(
        "You are JobHunter AI, a career assistant "
        "for South African graduate developers. "
        "Be helpful, concise, and never invent job listings."
    ),
    input=(
        "Introduce yourself and explain how you "
        "can help a junior Python developer find "
        "suitable employment opportunities."
    ),
)

# Display the response
print(response.output_text)
