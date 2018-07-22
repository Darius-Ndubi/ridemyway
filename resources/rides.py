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

"""
    User view a specific ride
"""
class Get_ride(Resource):
    def get(self,id):
        self.id=id

        search_ride=User.get_ride(self.id)

        #if ride is found show the ride to user
        if search_ride:
            return search_ride
        else:
            return ({"Error":"Ride does not exist"}),404


api.add_resource(Get_rides, '/rides')
api.add_resource(Get_ride, '/rides/<int:id>')