import requests
from dotenv import load_dotenv #For loaddinf API's key from .env file
from langfuse import Langfuse # Importing Langfuse SDK to connect with the cloud-based LLM evaluator ("the judge"). pip install langfuse
load_dotenv()
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
host = os.getenv("LANGFUSE_HOST")

langfuse = Langfuse(
    secret_key=secret_key,
    public_key=public_key,
    host=host
)

# def send_to_judge(response_text):
#     payload = {
#         "trace": {
#             "input": " the task ",
#             "output": response_text
#         }
#     }
#     headers = {
#         "Authorization": "Bearer YOUR_SECRET_KEY"
#     }
#     r = requests.post("https://cloud.langfuse.com/api/evaluate", json=payload, headers=headers)
#     return r.json()
