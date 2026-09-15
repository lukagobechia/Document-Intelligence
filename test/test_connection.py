import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


load_dotenv()

endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")

if not endpoint:
    raise ValueError("FOUNDRY_PROJECT_ENDPOINT is missing")

project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

client = project.get_openai_client()

print("Successfully connected to Microsoft Foundry!")