import os  # Allows the code to interact with the operating system, e.g., reading environment variables (useful for API keys)
os.environ["EVENTLET_NO_GREENDNS"] = "yes"
import eventlet  # A library for asynchronous networking, allows handling multiple connections efficiently
eventlet.monkey_patch()  # Modifies standard Python libraries to work asynchronously with Eventlet
from flask import Flask, render_template, request,send_from_directory   # Flask framework and utilities for web server, templates, handling requests, and returning JSON. Send_from_directory: serves static files (e.g., JavaScript, images, manifest) from a specified directory.
from flask_socketio import SocketIO, emit  # SocketIO enables real-time communication between server and client; emit sends messages to clients
from openai import OpenAI  # OpenAI client library to interact with OpenAI / HuggingFace models
import google.generativeai as genai  # Google Generative AI client library for using Gemini and other Google models
import requests  # Standard library for sending HTTP requests, useful for APIs without a dedicated client
import threading
from dotenv import load_dotenv

load_dotenv()

#-----------------------------------------MAIN
app = Flask( __name__,)
app.config['SECRET_KEY'] = 'key!secret!'
socketio = SocketIO(app)

#-----------------------------------------ENVIRONMENT VARIABLE
HFtoken = os.getenv("HUGGINGFACE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
API_URL = "https://router.huggingface.co/v1/chat/completions"

#--------------------------------CHECK FOR HF
def check_hf_connection():
    """HuggingFace API."""
    headers = {"Authorization": f"Bearer {HFtoken}"}
    data = {"model": "openai/gpt-oss-120b:cerebras", "messages": [{"role": "user", "content": "Hello"}]}
    response = requests.post(API_URL, headers=headers, json=data)
    print("HuggingFace Token status:", response.status_code, response.text)
#--------------------------------END CHECK FOR HF

def build_analysis_prompt(code: str) -> str:
    return f"""
    Please analyze the following code in detail.clearly structured and visually organized.
    Code:
    {code}
    Defining engineering programming principles:
    #readability- measure of how easily a person can understand a given code segment, easily one can understand
        how the code actually functions and understanding the intent and purpose of the code.
        •Consistent use of meaningful names to communicate intent rather than just content.
        • Proper software structure, including modular code separated into clear logical blocks.
        • Use comments sparingly- excessive commenting can be a sign of unclear code.
        • Proper formatting, such as indentation, line length, and spacing, which contribute to visual comprehension
        • without code smells- suggest design issues even if the code functions correctly like include unnecessary repetitions, unclear variable names, or excessively long functions.
    #Correctness - It refers to the accuracy with which code performs its intended tasks and requires thorough
        verification and testing to guarantee that the code behaves as expected in all scenarios.
        Understanding the task - If the task can be interpreted in multiple ways, ask the user what they mean.
    #Security - ensure that systems can operate normally even under external threats and attacks.
        check that there is no vulnerabilities in code such as bugs, defects, weaknesses,improper data validation or
        incorrect memory allocation which can lead to violations of system security policies and negatively impact the confidentiality, integrity, and availability of information
        Safe memory management
    """

def HuggingFaceAPI_GPT(prompt: str) -> str:
    clientGPT = OpenAI(base_url="https://router.huggingface.co/v1",api_key=HFtoken,)
    completion = clientGPT.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

def GeminiAPI(prompt: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def MistralAPI(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}","Content-Type": "application/json", }
    data = {"model": "mistral-tiny","messages": [{"role": "user", "content": prompt}], }
    mistral_response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    return mistral_response.json()['choices'][0]['message']['content']

def GPTJudgeAPI(responses: list, question: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    You are an expert code review judge.
    Use the engineering programming principles defined below for your assessment.
    remember! You are an expert professor tasked with merging multiple AI responses into one unified, high-quality answer.

    Principles:
    # Readability:
    - Measure how easily a person can understand the code segment, its functionality, and intent.
    - Look for consistent meaningful names, proper structure, modular blocks, sparing comments, good formatting, and absence of code smells.

    # Correctness:
    - Accuracy of code in performing intended tasks.
    - Verification and testing to ensure the code behaves as expected.
    - Clarify ambiguous tasks by asking what the user means if needed.

    # Security:
    - Ensure the code is safe under external threats.
    - Check for vulnerabilities: bugs, defects, weaknesses, improper validation, unsafe memory usage.
    - Safe memory management.

    Instructions:
    1. Read all the responses carefully and extract the most accurate and valuable insights from each one.
    2. Combine these insights into a single, coherent explanation that flows naturally, without repeating contradictions or irrelevant details.
    3. Structure the explanation according to the principles of Readability, Correctness, and Security, but present it as one unified answer — not as separate reviews of each response.
    4. The final result should read like a polished academic explanation, as if written by a knowledgeable professor, integrating the best contributions from all responses.

    Question / Code:
    {question}

    Responses:
    {chr(10).join(responses)}
    """
    
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return completion.choices[0].message.content


# Receiving code as text(string) from the user
@socketio.on('send_code')
def handle_code(data):
    code = data.get('code')
    print('Received code:', code)

    prompt = build_analysis_prompt(code)

    hf_result = HuggingFaceAPI_GPT(prompt)
    # emit('code_result', {'result': f"GPT:\n{hf_result}"})

    gemini_result = GeminiAPI(prompt)
    # emit('code_result', {'result': f"GEMINI:\n{gemini_result}"})

    mistral_result = MistralAPI(prompt)
    # emit('code_result', {'result': f"MISTRAL:\n{mistral_result}"})

    all_responses = [hf_result, gemini_result, mistral_result]
    judge_result = GPTJudgeAPI(all_responses, code)
    emit('code_result', {'result': f"Judge:\n{judge_result}"})  

    evaluations = {
    "GPT": hf_result,
    "Gemini": gemini_result,
    "Mistral": mistral_result
    }
    
    #sending to judge
    # final_score, full_assessment_json = send_to_judge(
    # code=code, 
    # evaluations=evaluations, 
    # evaluator_name="CodeReview_JSON_Judge" 
    # )

@app.route('/')
def index():
    return render_template('index.html')

# Flask route to serve the service worker JavaScript file.
# This is used in Progressive Web Apps (PWAs) to enable features like offline support,
# caching, and background sync. The service worker must be accessible from the root scope
# (i.e., '/service_worker.js') to control the entire application.
# Since Flask does not serve files from the root directory by default,
# we manually serve the file using send_from_directory and os.getcwd().
@app.route('/service_worker.js')
def sw():
    return send_from_directory(os.getcwd(), 'service_worker.js')

if __name__ == '__main__':
    #check_hf_connection()
    print(f"AIREC: http://localhost:5000/")
    socketio.run(app)