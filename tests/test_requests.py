import pytest,psycopg2,json
from flask_jwt_extended import create_access_token
from app import app
from tests.test_signup import mock_login_token
from app.db import connTDb
from app.create_testdb import createall_tables

"""
    Ride requests mock data
"""
mock_req1={'ride_id':1}

"""
    A fuction to find the number of requests in the db
    it returns the found number
"""
def requests_num():
    connection=connTDb()
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
    A test on  ride requests creation
"""
def test_ride_requests():
    with app.app_context():
        tok=mock_login_token()
        old_resquests_num=requests_num()
        result=app.test_client()
        response=result.post('/api/v1/rides/4/requests', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_requests_num=requests_num()
        assert (new_requests_num==old_resquests_num)
        assert response.json=={"Error":"You cannot request your own ride"}
        assert (response.status_code==403)
       
 
def test_ride_requests():
    with app.app_context():
        tok=mock_login_token()
        old_resquests_num=requests_num()
        result=app.test_client()
        response=result.post('/api/v1/rides/4/requests', data=json.dumps(mock_req1),content_type='application/json',headers={ 'Authorization': 'Bearer ' + tok })
        json.loads(response.data.decode('utf-8'))
        new_requests_num=requests_num()
        assert (new_requests_num-1==old_resquests_num)
        assert response.json=={"Successful":"Request posted successfull"}
        assert (response.status_code==200    


