import pytest,psycopg2,json
from flask_jwt_extended import create_access_token
from app import app
from tests.test_signup import mock_login_token
from app.db import connDb


"""
    Mock data to represent a ride to be added to the database
"""
mock_ride={
    "car_license": "KAC 345T",
    "title": "Troy to Sparta",
    "ride_date": "06-06-2018",
    "distance": 45,
    "num_seats": 7,
    "start_time": "0700",
    "arrival_time": "1700",
    "ride_price": 1500
    }

mock_ride1={
    "car_license": "KAC 345T",
    "title": "Ithacaa to Sparta",
    "ride_date": "06-06-2018",
    "distance": 45,
    "num_seats": 7,
    "start_time": "0700",
    "arrival_time": "1700",
    "ride_price": 1500,
    }

"""
    A fuction to test the successful addition of a ride to the database
"""
def ride_get():
    connection=connDb()
    curs=connection.cursor()

    curs.execute("SELECT * FROM ride")
    all=curs.fetchall()
    
    #close the connection
    curs.close()
    connection.commit()
    connection.close()
    #print (len(all))

    return len(all)



"""
    A test on get all rides from db
"""
def test_Get_rides():
    result=app.test_client()
    response=result.get('/api/v1/rides')
    assert(response.status_code==200)

"""
    A test on finding a specific ride
"""
def test_Get_ride():
    result=app.test_client()
    response=result.get('/api/v1/rides/10')
    assert response.json=={"Error":"Ride does not exist"}
    assert(response.status_code==404)

"""
    A test on finding a specific ride
"""
def test_Get_ride():
    result=app.test_client()
    response=result.get('/api/v1/rides/1')
    assert response.json==[[1,
    "KAC 345T",
    "Athens to Sparta",
    "06-06-2018",
    45,
    7,
    "0700",
    "1700",
    1500,
    "delight"
    ]]
     
    assert(response.status_code==200)

"""
    A test for ride creation endpoint
    Its tests if the ride exixts then it errors out
    When a match in Titles is found
"""
def test_Add_ride():
    with app.app_context():
        tok=mock_login_token()
        result=app.test_client()
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json =={"Error":"A Title like the one you want to enter exists,Let it Be unique"}
        assert (response.status_code==406)

"""
    A test to test the creation of a new ride
"""
def test_Add_ride():
    with app.app_context():
        tok=mock_login_token()
        old_num_rides=ride_get()
        result=app.test_client()
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        new_num_rides=ride_get()
        json.loads(response.data.decode('utf-8'))
        if new_num_rides-1==old_num_rides:
            assert response.json =={"Success":"Your ride has been created and posted"}
            assert (response.status_code==200)