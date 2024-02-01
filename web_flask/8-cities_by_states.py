#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template
from models import State, City, storage
from os import getenv

app = Flask(__name__)

storageType = getenv("HBNB_TYPE_STORAGE")


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


@app.route("/cities_by_states", strict_slashes=False, methods=["GET", "POST"])
def cbs():
    """
    display a HTML page: (inside the tag BODY)

    H1 tag: “States”
    UL tag: with the list of all State objects
    present in DBStorage sorted by name (A->Z) tip
        LI tag: description of one State: <state.id>: <B><state.name></B> +
        UL tag: with the list of City objects linked to
        the State sorted by name (A->Z)
            LI tag: description of one City: <city.id>: <B><city.name></B>

    """
    return render_template(
        "8-cities_by_states.html",
        obj=storage.all(State),
    )


if __name__ == "__main__":
    app.run()
