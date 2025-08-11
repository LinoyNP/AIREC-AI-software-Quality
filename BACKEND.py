
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask( __name__,)
app.config['SECRET_KEY'] = 'key!secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')
@socketio.on('send_code')
def handle_code(data):
    code = data.get('code')
    print('Received code:', code)
    # ----here we send the code to models and recieved the result, and then
    result = f" checking sendig to web {code}"
    emit('code_result', {'result': result})

if __name__ == '__main__':
    socketio.run(app)