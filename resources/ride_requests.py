from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.model.manRides import User
from flask_jwt_extended import jwt_required,get_jwt_identity


api=Namespace("about_requests", description="Ride requests endpoints")

"""
    An endpoint for creating ride requests
    The endpoint requires only the ride id of the ride a user wants to request
    All other details are picked from users details as per registration
    The enpoint is secured with A token so that only known users can create a riquest and only after login
"""

class Ride_requests(Resource):
    @jwt_required
    def post(self,id):
        self.id=id
        requester_name=get_jwt_identity()
        
        #find the ride if the ride exists
        search_ride=User.get_ride(self.id)
        #user cant request there own ride
        #print (search_ride)
        if requester_name==search_ride[0][9]:
            return ({"Error":"You cannot request your own ride"}),403
        
        User.create_requests(ride_id=self.id,car_licence=search_ride[0][1],title=search_ride[0][2],requester_name=get_jwt_identity(),ride_date=search_ride[0][3],num_seats=search_ride[0][5],ride_price=search_ride[0][8],creator=search_ride[0][9])

        return({"Successful":"Request posted successfull"})


api.add_resource(Ride_requests,'/rides/<int:id>/requests')