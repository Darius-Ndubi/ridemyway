import pytest,psycopg2,json
from app import app
from app.db import connTDb

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
    response=result.get('/api/v1/rides/1')
    assert response.json=={"Error":"Ride does not exist"}
    assert(response.status_code==404)

