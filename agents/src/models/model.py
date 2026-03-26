import getpass
import os
from langchain_openai import ChatOpenAI

if not os.environ.get("MODEL_API_KEY"):
    os.environ["MODEL_API_KEY"] = getpass.getpass("Enter your model API key: ")

if not os.environ.get("MODEL_ENDPOINT"):
    os.environ["MODEL_ENDPOINT"] = getpass.getpass("Enter your model endpoint e.g. https://api.openai.com: ")

if not os.environ.get("MODEL_NAME"):
    os.environ["MODEL_NAME"] = getpass.getpass("Enter your model name e.g. gpt-5-nano: ")

OPENAI_MODEL = ChatOpenAI(
    model=os.environ.get("MODEL_NAME"),
    max_retries=2,
    base_url=os.environ.get("MODEL_ENDPOINT"),
    api_key=os.environ.get("MODEL_API_KEY")
)