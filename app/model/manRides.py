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
        connection.commit()
        connection.close()
        return jsonify(rides)

    #method to find specific ride in db
    @staticmethod
    def get_ride(search_id):
        #locate ride with the matching id in the db and return it (email)s",{'email':self.email}
        connection=connDb()
        curs=connection.cursor()
        curs.execute("SELECT * FROM ride WHERE r_id=%(r_id)s",{'r_id':search_id})
        #get the whole row
        found=curs.fetchall()
        #print (self.found)
        curs.close()
        connection.commit()
        connection.close()
        return found

    #method to query if ride exists
    def checkRideExistance(self,title):
        self.title=title
        connection=connDb()
        curs=connection.cursor()
        curs.execute("SELECT * FROM ride WHERE title=%(title)s",{'title':self.title})
        self.existance = curs.fetchone()
        curs.close()
        connection.commit()
        connection.close()
        return self.existance

     
    #create a ride method for user
    def create_ride(self,):
        connection=connDb()
        curs=connection.cursor()
        
        curs.execute("INSERT INTO ride (car_license,title,ride_date,num_seats,distance,start_time,arrival_time,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.car_license,self.title,self.ride_date,self.num_seats,self.distance,self.start_time,self.arrival_time,self.ride_price,self.creator))

        curs.close()
        connection.commit()
        connection.close()
    
    #method to create a ride request
    @staticmethod
    def create_requests(ride_id,car_licence,requester_name,ride_date,title,num_seats,ride_price,creator):
        connection=connDb()
        curs=connection.cursor()
        curs.execute("INSERT INTO requestss (ride_id,car_license,requester_name,ride_date,title,num_seats,ride_price,creator) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(ride_id,car_licence,requester_name,ride_date,title,num_seats,ride_price,creator))
        curs.close()
        connection.commit()
        connection.close()
    
