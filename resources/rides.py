from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.model.manRides import User


api=Namespace("about_rides", description="Rides endpoints")

"""
    User view all rides endpoint
    The route returns all rides created in the database
"""

class Get_rides(Resource):
    def get(self):
        return (User.get_rides())


api.add_resource(Get_rides, '/rides')