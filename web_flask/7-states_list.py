#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


@app.route("/states_list", strict_slashes=False, methods=["GET", "POST"])
def states():
    """
     display a HTML page: (inside the tag BODY)

    H1 tag: “States”
    UL tag: with the list of all State objects present
     in DBStorage sorted by name (A->Z) tip
        LI tag: description of one State: <state.id>: <B><state.name></B>
    """
    return render_template("7-states_list.html", obj=storage.all(State))


if __name__ == "__main__":
    app.run()
