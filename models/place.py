#!/usr/bin/python3
""" Place Module for HBNB project """
from tempfile import gettempprefix
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Float, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column("place_id", String(60),
               ForeignKey("places.id"), primary_key=True),
        Column("amenity_id", String(60),
               ForeignKey("amenities.id"),
               primary_key=True),
    )


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = "places"
    if storage_type == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(128), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []

        reviews = relationship("Review", cascade="all,delete", backref="place")
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities",
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        def __init__(self, *args, **kwargs):
            """initializes Place"""
            super().__init__(*args, **kwargs)

        @property
        def reviews(self):
            """
            Getter attribute reviews that returns the list of Review instances
            with place_id equals
            to the current Place.id => It will be the FileStorage
            relationship between Place and Review
            """
            from models import storage

            reviews_list = []
            for k, v in storage.all():
                if k.partition(".")[0] == "Review":
                    if v.place_id == self.id:
                        reviews_list.append(v)
            return reviews_list

        @property
        def amenities(self):
            """
            Getter attribute amenities that
            returns the list of Amenity instances
            based on the attribute amenity_ids
            that contains all Amenity.id linked to the Place
            """
            from models import storage

            amenins = []
            for k, v in storage.all(Amenity).items():
                if k.partition(".")[0] == "Amenity":
                    if v.id in self.amenity_ids:
                        amenins.append(v)
            return amenins

        @amenities.setter
        def amenities(self, amenity):
            """
            Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids.
            This method should accept only Amenity object, otherwise,
            do nothing.
            """
            if amenity.__class__.__name__ == "Amenity":
                self.amenity_ids.append(amenity.id)
