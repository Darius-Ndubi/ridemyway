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
    -> test on own ride request creation creation
    -> test on others ride request creation
    -> test on wether a ride request has been created
    -> test on retriving ride requests
    -> Responding to ride request but with on existing id
    -> A test on successful ride request accept
    -> A test on successfull ride request deline
"""
def test_ride_requests_empty_num_seats():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.post('/api/v1/rides/1/requests', data=json.dumps(mock_num_seats[1]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        data_input=json.loads(response.data.decode('utf-8'))
        assert response.json=={'Error': 'The number of  available seats cannot be empty'}
        assert(response.status_code==400)

def test_ride_requests_own_ride():
    with app.app_context():
        tok=mock_login_token(mock_reg[0].get('username'))
        old_resquests_num=requests_num()
        result=app.test_client()
        response=result.post('/api/v1/rides/1/requests', data=json.dumps(mock_num_seats[0]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_requests_num=requests_num()
        assert (new_requests_num==old_resquests_num)
        assert response.json=={"Error":"You cannot request your own ride"}
        assert (response.status_code==403)


def test_ride_requests_others_ride():
    with app.app_context():
        tok=mock_login_token(mock_reg[3].get('username'))
        old_resquests_num=requests_num()
        result=app.test_client()
        response=result.post('/api/v1/rides/1/requests', data=json.dumps(mock_num_seats[0]),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_requests_num=requests_num()
        #new_requests_num=requests_num()
        new_requests_num-1==old_resquests_num
        assert response.json=={"Successful":"Request posted successfull"}
        assert (response.status_code==200) 


def test_ride_requests_no_requests_created():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.get('/api/v1/rides/2/requests',content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        assert response.json=={"Error":"No requests have been made to your ride yet"}
        assert (response.status_code==400)


def test_ride_requests_get_existing_request():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.get('/api/v1/rides/1/requests',content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        assert response.json==[
	    [
		1,
		1,
		"KAC 345T",
		"user",
		"06-06-2018",
		"Troy to Sparta",
		4,
		1500,
		"delight",
        None
        ]
        ]
        assert(response.status_code==200)


def test_ride_response_unfound_id():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.put('/api/v1/rides/respond/20/decline', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json=={'Error': 'Make sure you have entered the correct request id'}
        assert (response.status_code==404)

def test_ride_respond_accept_request():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.put('/api/v1/rides/respond/1/accept', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json=={'Success': 'Your response has been posted successfully'}
        assert (response.status_code==200)

def test_ride_respond_decline_request():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.put('/api/v1/rides/respond/1/decline', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json=={'Success': 'Your response has been posted successfully'}
        assert (response.status_code==200)

"""def test_ride_respond_failed():
    with app.app_context():
        result=app.test_client()
        tok=mock_login_token(mock_reg[0].get('username'))
        response=result.put('/api/v1/rides/respond/1/"<>@#$%#W"', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        assert response.json=={'Error': 'Response not created successfully input not sensible string'}
        assert (response.status_code==400)"""
