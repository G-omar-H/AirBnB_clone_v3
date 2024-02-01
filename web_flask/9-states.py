#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template
from models import State, City, storage
from jinja2 import Environment
from os import getenv


storageType = getenv("HBNB_TYPE_STORAGE")

l_flag = {" flag": False}


def set_flag_true(l_flag):
    l_flag["flag"] = True
    pass


def set_flag_false(l_flag):
    l_flag["flag"] = False
    pass


app = Flask(__name__)
app.jinja_env.globals["set_flag_true"] = set_flag_true
app.jinja_env.globals["set_flag_false"] = set_flag_false


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


@app.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states():
    """
     display a HTML page: (inside the tag BODY)

    H1 tag: “States”
    UL tag: with the list of all State objects present
     in DBStorage sorted by name (A->Z) tip
        LI tag: description of one State: <state.id>: <B><state.name></B>
    """
    return render_template("7-states_list.html", obj=storage.all(State))


@app.route("/states/<id>", strict_slashes=False, methods=["GET", "POST"])
def state(id):
    """
     display a HTML page: (inside the tag BODY)

    If a State object is found with this id:
        H1 tag: “State: ”
        H3 tag: “Cities:”
        UL tag: with the list of City objects linked to
        he State sorted by name (A->Z)
            LI tag: description of one City: <city.id>: <B><city.name></B>
    Otherwise:
        H1 tag: “Not found!”

    """

    return render_template(
        "9-states.html",
        obj=storage.all(State),
        storageType=storageType,
        id=id,
        l_flag=l_flag,
    )


if __name__ == "__main__":
    app.run()
