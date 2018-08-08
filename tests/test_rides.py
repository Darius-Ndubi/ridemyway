import pytest,psycopg2,json
from flask_jwt_extended import create_access_token
from app import app
from tests.test_signup import mock_login_token,mock_reg
from app.db import connDb


"""
    Mock data to represent a ride to be added to the database
"""
mock_ride=[{
    "car_license": "KAC 345T",
    "title": "Troy to Sparta",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": 1500
    },
    {
    "car_license": "KAC 345T",
    "title": "Ithaca to Sparta",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": 1500,
    },
    
    {
    "car_license": "",
    "title": "Ithaca to Sparta",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": 1500,
    },

    {
    "car_license": "KAC 345T",
    "title": "",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": 1500,
    },

    {
    "car_license": "KAC 345T",
    "title": "Ithaca to Sparta",
    "ride_date": "",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": 1500,
    },

    {
    "car_license": "KAC 345T",
    "title": "Ithaca to Sparta",
    "ride_date": "06-06-2018",
    "num_seats":"" ,
    "start_time": "0700",
    "ride_price": 1500,
    },

    {
    "car_license": "KAC 345T",
    "title": "Ithaca to Sparta",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "",
    "ride_price": 1500,
    },


    {
    "car_license": "KAC 345T",
    "title": "Ithaca to Sparta",
    "ride_date": "06-06-2018",
    "num_seats": 7,
    "start_time": "0700",
    "ride_price": "",
    },
]

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
    Tests on input validation
        -> empty car license
        -> Empty title
        -> Empty ride Date
        -> Empty number of seats
        -> Empty start_time
        -> Empty ride price
"""
def test_Add_ride_empty_car_license():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[2]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Error": "car License field cannot be empty"}
        assert(response.status_code==400)

def test_Add_ride_empty_title():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[3]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Error": "The title cannot be empty"}
        assert(response.status_code==400)

def test_Add_ride_empty_ride_date():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[4]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Error":"The date of the ride cannot be empty"}
        assert(response.status_code==400)

def test_Add_ride_empty_num_seats():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[5]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Error":"The number of  available seats cannot be empty"}
        assert(response.status_code==400)

def test_Add_ride_empty_start_time():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[6]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Error":"Please specify when the ride will start"}
        assert(response.status_code==400)

def test_Add_ride_empty_start_time():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[7]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={"Info":"Filled can't be empty but if ride is free just input 0"}
        assert(response.status_code==400)


"""
Create ride test
    ->A test to test the creation of a new ride
    -> Its tests if the ride exixts then it errors out
           -> When a match in Titles is found
           -> Title should be unique as the same car can be used to many rides over time.
"""

def test_Add_ride_successfully():
    with app.app_context():
        tok=mock_login_token(mock_reg[0].get('username'))
        old_num_rides=ride_get()
        result=app.test_client()
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[0]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_num_rides=ride_get()
        if new_num_rides-1==old_num_rides:
            assert response.json =={"Success":"Your ride has been created and posted"}
            assert (response.status_code==200)


def test_Add_ride_matching_title():
    with app.app_context():
        tok=mock_login_token(mock_reg[0].get('username'))
        old_num_rides=ride_get()
        result=app.test_client()
        response=result.post('/api/v1/rides', data=json.dumps(mock_ride[1]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_num_rides=ride_get()
        if new_num_rides==old_num_rides:
            assert response.json =={"Error":"A Title like the one you want to enter exists,Let it Be unique"}
            assert (response.status_code==406)

"""
    A test on get all rides from db
    A test on finding a specific ride
    A test on finding a specific ride

"""
def test_Get_rides():
    result=app.test_client()
    response=result.get('/api/v1/rides')
    assert(response.status_code==200)


def test_Get_ride_not_created():
    result=app.test_client()
    response=result.get('/api/v1/rides/10')
    assert response.json=={"Error":"Ride does not exist"}
    assert(response.status_code==404)


def test_Get_ride_existing_ride():
    result=app.test_client()
    response=result.get('/api/v1/rides/1')
    assert response.json==[[1,
    "KAC 345T",
    "Troy to Sparta",
    "06-06-2018",
    7,
    "0700",
    1500,
    "delight"
    ]]
     
    assert(response.status_code==200)
