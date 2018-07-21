import psycopg2
from flask import Response,jsonify
from app.db import connDb

"""
    A class with actions of a user to a ride
    It shows the responsibilities of a user
"""
class User(object):


    #class constructor
    def __init__(self,creator, car_license, title, ride_date,num_seats, distance, start_time, arrival_time, ride_price):
        self.car_license = car_license
        self.title = title
        self.ride_date =ride_date
        self.num_seats=num_seats
        self.distance = distance
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.ride_price = ride_price
        self.creator=creator
        

    #method to find all rides in db
    @staticmethod
    def get_rides():
        connection=connDb()
        curs=connection.cursor()
        curs.execute("SELECT * FROM ride")
        rides=curs.fetchall()
        #print (self.rides)
        curs.close()
        return jsonify(rides)
