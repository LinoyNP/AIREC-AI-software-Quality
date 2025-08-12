import os
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from openai import OpenAI
import requests
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    #HuggingFace GPT-OSS 120b
    #result = queryHuggingfaceApi(prompt)

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HFtoken,
    )

    #gpt-oss-120b
    completion = client.chat.completions.create(
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

    print(result)
    emit('code_result', {'result': result})

if __name__ == '__main__':
    socketio.run(app)