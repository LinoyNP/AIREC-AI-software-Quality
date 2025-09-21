import os  # Allows the code to interact with the operating system, e.g., reading environment variables (useful for API keys)
os.environ["EVENTLET_NO_GREENDNS"] = "yes"
import eventlet  # A library for asynchronous networking, allows handling multiple connections efficiently
eventlet.monkey_patch()  # Modifies standard Python libraries to work asynchronously with Eventlet
from flask import Flask, render_template, request, jsonify,send_from_directory   # Flask framework and utilities for web server, templates, handling requests, and returning JSON. Send_from_directory: serves static files (e.g., JavaScript, images, manifest) from a specified directory.
from flask_socketio import SocketIO, emit  # SocketIO enables real-time communication between server and client; emit sends messages to clients
from openai import OpenAI  # OpenAI client library to interact with OpenAI / HuggingFace models
#Noa
import google.generativeai as genai  # Google Generative AI client library for using Gemini and other Google models
import requests  # Standard library for sending HTTP requests, useful for APIs without a dedicated client
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
    """
       Defining engineering programming principles:
       #readability- measure of how easily a person can understand a given code segment, easily one can understand
           how the code actually functions and understanding the intent and purpose of the code.
            •Consistent use of meaningful names to communicate intent rather than just content.
            • Proper software structure, including modular code separated into clear logical blocks.
            • Use comments sparingly- excessive commenting can be a sign of unclear code.
            • Proper formatting, such as indentation, line length, and spacing, which contribute to visual comprehension
            • without code smells- suggest design issues even if the code functions correctly like include unnecessary repetitions, unclear
               variable names, or excessively long functions.
       #Correctness - It refers to the accuracy with which code performs its intended tasks and requires thorough
           verification and testing to guarantee that the code behaves as expected in all scenarios.
           Understanding the task - If the task can be interpreted in multiple ways, ask the user what they mean.
       #Security - ensure that systems can operate normally even under external threats and attacks.
           check that there is no vulnerabilities in code such as bugs, defects, weaknesses,improper data validation or
            incorrect memory allocation which can lead to violations of system security policies and negatively impact the confiden tiality, integrity, and availability of information
           Safe memory management
       """
    return f"""
    Please analyze the following code in detail. The analysis should be written in Hebrew, clearly structured and visually organized.
    Code:
    {code}
    For this code, please provide:
    1. Readability: Give a percentage score (0-100%) and a detailed explanation in Hebrew about how easy it is to read and understand the code. Mention naming conventions, comments, formatting, and clarity.
    2. Correctness: Give a percentage score (0-100%) and explain in Hebrew whether the code works as intended, whether there are potential bugs, logical errors, or edge cases that might fail.
    3. Security: Give a percentage score (0-100%) and explain in Hebrew any security risks, vulnerabilities, or unsafe practices in the code.
    4. Additional Notes: Any suggestions for improvement, refactoring, or best practices, in Hebrew. Be as detailed and precise as possible.
    Format the output neatly with clear headings for each section, percentages, and explanations. Use line breaks and bullet points if needed to make it easy to read.
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


# Receiving code as text(string) from the user
@socketio.on('send_code')
def handle_code(data):
    code = data.get('code')
    print('Received code:', code)

    prompt = build_analysis_prompt(code)

    hf_result = HuggingFaceAPI_GPT(prompt)
    emit('code_result', {'result': f"GPT:\n{hf_result}"})

    gemini_result = GeminiAPI(prompt)
    emit('code_result', {'result': f"GEMINI:\n{gemini_result}"})

    mistral_result = MistralAPI(prompt)
    emit('code_result', {'result': f"MISTRAL:\n{mistral_result}"})

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
    # check_hf_connection()
    print(f"AIREC: http://localhost:5000/")
    socketio.run(app)