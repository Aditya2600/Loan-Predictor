import pickle
from flask import Flask

app = Flask(__name__)


@app.route("/ping", methods=['GET'])
def ping():
    return{"message": "Hi there, I'm working!!"}