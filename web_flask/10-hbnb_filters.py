#!usr/bin/python3
"""
script to start a flask web application
"""

from models import State, City, Amenity, Place, storage
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(Exception):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False, methods=["GET", "POST"])
def last():
    """

    /hbnb_filters: display a HTML page like 6-index.html,
    which was done during the project 0x01. AirBnB clone - Web static
        State, City and Amenity objects must be loaded
        from DBStorage and sorted by name (A->Z)
    """
    return render_template(
        "10-hbnb_filters.html",
        states=storage.all(State),
        amenities=storage.all(Amenity),
        place=storage.all(Place())
    )


if __name__ == "__main__":
    app.run()
