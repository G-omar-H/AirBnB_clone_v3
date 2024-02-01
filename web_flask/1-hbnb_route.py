#!/usr/bin/python3
"""
python script that starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    display HBNB on route
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run()
