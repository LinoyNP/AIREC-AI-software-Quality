import os
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from openai import OpenAI
from google import genai
import requests

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask( __name__,)
app.config['SECRET_KEY'] = 'key!secret!'
socketio = SocketIO(app)

HFtoken = os.getenv("HUGGINGFACE_API_KEY")


@app.route('/')
def index():
    return render_template('index.html')

# Receiving code as text(string) from the user
@socketio.on('send_code')
def handle_code(data):
    code = data.get('code')
    print('Received code:', code)
    prompt = f"Analyze this code for readability, correctness, and security (both in words and as percentages):\n{code}"

    ###
    # ----here we send the code to models and recieved the result, and then
    ###

    clientGPT = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HFtoken,
    )

    #gpt-oss-120b
    completion = clientGPT.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": prompt}],
    )

    print(completion.choices[0].message)
    result = completion.choices[0].message.content

    #GPT
    # response = client.responses.create(
    #     model="gpt-5",
    #     input=prompt
    # )
    #
    # result = f" checking sendig to web {code}"
    # result = response.output_text

    print(f"{result} \n finish print gpt")
    emit('code_result', {'result': f"GPT:\n{result}"})
    #
    #gemini
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    clientGemini = genai.Client()

    response = clientGemini.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    print(f"{response.text} finish print")
    emit('code_result', {'result': f"GEMINI:\n{response.text}"})

if __name__ == '__main__':
    print(f"To AIREC open: http://localhost:5000/")
    socketio.run(app)