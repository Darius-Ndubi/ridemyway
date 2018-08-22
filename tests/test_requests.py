import pytest,psycopg2,json
from flask_jwt_extended import create_access_token
from app import app
from tests.test_signup import mock_login_token,mock_reg
from app.db import connDb


"""
    Ride requests mock data
"""
mock_req1={'ride_id':1}
mock_num_seats=[{"num_seats":4},{"num_seats":""}]

"""
    A fuction to find the number of requests in the db
    it returns the found number
"""
def requests_num():
    connection=connDb()
    curs=connection.cursor()

    curs.execute("SELECT * FROM requestss")
    all=curs.fetchall()
    
    #close the connection
    curs.close()
    connection.commit()
    connection.close()
    #print (len(all))

    return len(all)

"""
Ride requests Tests
    -> test if num of seat is left empty
    #-> test on own ride request creation creation
    -> test on others ride request creation
    -> test on wether a ride request has been created
    -> test on retriving ride requests
    -> Responding to ride request but with on existing id
    -> A test on successful ride request accept
    -> A test on successfull ride request deline
"""
def test_Ride_requests_empty_num_seats():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token('delight')
        response=result.post('/api/v1/rides/1/requests', data=json.dumps(mock_num_seats[1]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json=={'Error': 'The number of  available seats cannot be empty'}
        assert(response.status_code==400)


def test_Ride_requests_no_requests_created():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.get('/api/v1/rides/1/requests',content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        assert response.json=={"Error":"No requests have been made to your ride yet"}
        assert (response.status_code==400)


