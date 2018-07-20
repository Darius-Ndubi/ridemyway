import pytest,psycopg2,json

from app import app
from app.db import connTDb
from app.create_testdb import createall_tables

#create tables if no exists
createall_tables()

"""
    Mock user data to be used to fill the required tables columns
    The data will mock a real user
"""
mock_reg={"email":"yagamidelight@gmail.com","username":"delight","password":"delight"}

"""
    A fuction to find users signed in
    The method helps to validate if a user signup is successfull
    It compares the number of users before signup and after signup 
"""
def registered():

    connection=connTDb()
    curs=connection.cursor()

    curs.execute("SELECT * FROM new_user")
    all=curs.fetchall()
    
    #close the connection
    curs.close()
    connection.commit()
    connection.close()
    #print (len(all))

    return len(all)
"""
    A test to indicate on user signup 
    The test tests if the user is signed up
"""
def test_signup():
    old_num_users=registered()
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    new_num_users=registered()
    json.loads(response.data.decode('utf-8'))
    assert(old_num_users==new_num_users)
    assert response.json=={"Email Error": "Email is already linked to another user, pick another one"}
    assert(response.status_code==406)

"""
    A test on user signup 
    the test tests dding of new user to the data base
"""
def test_signup():
    old_num_users=registered()
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    new_num_users=registered()
    #print (new_num_users)
    if new_num_users-1==old_num_users:
        assert response.json=={"Successfull":"Proceed to login"}
        assert(response.status_code==200)


