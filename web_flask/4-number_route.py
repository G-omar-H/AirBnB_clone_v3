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


@app.route('/c/<text>', strict_slashes=False)
def print_text(text):
    """
    displays whatever text input
    """
    res = ''
    for c in text:
        if c != '_':
            res = res + c
        else:
            res = res + ' '

    return f"C {res}"


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """
    displays Python text argument
    Args:
        text (str, optional): _description_. Defaults to 'is cool'.
    """
    res = ''
    for c in text:
        if c != '_':
            res = res + c
        else:
            res = res + ' '

    return f"Python {res}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    return f'{n} is a number'


if __name__ == '__main__':
    app.run()
