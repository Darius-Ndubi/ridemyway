from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.model.manRides import User
from flask_jwt_extended import jwt_required,get_jwt_identity

class Rides_fields(object):
    parser = reqparse.RequestParser()

    def get_ride_fields(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ride_date', required=True,
                            help="Date cannot be blank!")
        self.parser.add_argument('distance', required=True,
                            help="Distance cannot be blank!")
        self.parser.add_argument('title', required=True,
                            help="Title cannot be blank!")
        self.parser.add_argument('num_seats', required=True,
                             help="Number of seats cannot be blank!")
        self.parser.add_argument('start_time', required=True,
                                 help="start_time cannot be blank!")
        self.parser.add_argument('arrival_time', required=True,
                            help="arrival_time cannot be blank!")
        self.parser.add_argument('ride_price', required=True,
                            help="ride_price cannot be blank!")
        self.parser.add_argument('car_license', required=True,
                            help="car_license cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args


R=Rides_fields()

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


"""
    A class to create the ride from a logged in user adn store it in the database
    User is authenticated trough jwt tokens before creating a ride
"""
class Add_ride(Resource):

    #securing endpoint with jwt_required
    @jwt_required
    def post(self):
        args = R.get_ride_fields()
        username=get_jwt_identity()

        #checking if all the fields are entered
        if args['car_license'] == "":
            return ({"Error": "car License field cannot be empty"})
        elif args['title'] == "":
            return ({"Error": "The title cannot be empty"})
        elif args['ride_date']=="":
            return ({"Error":"The date of the ride cannot be empty"})
        elif args['num_seats']=="":
            return ({"Error":"The number of  available seats cannot be empty"})
        elif args['distance']=="":
            return ({"Error":"The Distance to be covered must be filled"})
        elif args['start_time']=="":
            return ({"Error":"Please specify when the ride will start"})
        elif args['arrival_time']=="":
            return ({"Error":"Estimate the time we would arrive"})
        elif args['ride_price']=="":
            return ({"Info":"Filled cant be empty but if ride is free just input 0"})
        
        new_ride=User(car_license=args['car_license'],title=args['title'],ride_date=args['ride_date'],distance=args['distance'],num_seats=args['num_seats'],start_time=args['start_time'],arrival_time=args['arrival_time'],ride_price=args['ride_price'],creator=username)
        
        exist=new_ride.checkRideExistance(args['title'])
        
        #if the ride title exists give user an error message why not to use the title
        if exist:
            return {"Error":"A Title like the one you want to enter exists,Let it Be unique"},406
        
        #if ride is unique let the user post it
        else:
            #save the rides details
            new_ride.create_ride()
            return ({"Success":"Your ride has been created and posted"}),200
        return ({"Error":"Token validation failure"}),403



api.add_resource(Get_rides, '/rides')
api.add_resource(Get_ride, '/rides/<int:id>')
api.add_resource(Add_ride, '/rides')