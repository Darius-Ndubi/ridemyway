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

