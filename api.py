from flask import Flask
from services.user_service import user_blueprint
from services.rooms_service import room_blueprint

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(user_blueprint)
app.register_blueprint(room_blueprint)