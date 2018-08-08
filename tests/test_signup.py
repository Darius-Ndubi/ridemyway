import pytest,psycopg2,json
from flask_jwt_extended import create_access_token
from app import app
from app.db import connTDb
from app.create_testdb import createall_tables

#create tables if no exists
createall_tables()

"""
    Mock user data to be used to fill the required tables columns
    The data will mock a real user
"""
mock_reg=[{"email":"yagamidelight@gmail.com","username":"delight","password":"delight"},
          #incorrect user data
          {"email":"","username":"delight","password":"delight"},
          {"email":"yagamidelight@gmail.com","username":"","password":"delight"},
          #another data of a user
          {"email":"e@g.com","username":"user","password":"usedall"},
          {"email":"yagamidelight@gmail.com","username":"delight","password":""},
          #incorrect user data
          {"email":"yagamidelightgmail.com","username":"delight","password":"delight"},
          {"email":"yagamidelight@gmail","username":"delight","password":"delight"}
]
"""
    Mock user data for user login
"""
mock_log=[{"email":"yagamidelight@gmail.com","password":"delight"},
            #incorrect user data
          {"email":"yagamidelight@gmail.com","password":"delhight"},
          {"email":"","password":"delhight"},
          {"email":"yagamidelight@gmail.com","password":""},
          {"email":"yagamidelightgmail.com","password":"delight"},
          {"email":"yagamidelight@gmail","password":"delight"},
            #second correct user data
          {"email":"e@g.com","password":"usedall"}
]

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
    Tests on invalid user data(Validation tests)
        ->A test to test if the email field is empty
        ->A test to test if username entered is empty
        ->A test to test if password entered is empty
        ->A test if the email entered meets logic if.com is there
        -> if thw email as @ in it

"""  
def test_signup_empty_email():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[1]),content_type='application/json')
    data_input=json.loads(response.data.decode('utf-8'))
    assert response.json=={'Error': 'Email field cannot be empty'}
    assert(response.status_code==400)


def test_signup_empty_username():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[2]),content_type='application/json')
    data_input=json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Username field cannot be empty"}
    assert(response.status_code==400)


def test_signup_empty_password():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[4]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Password fields cannot be empty"}
    assert(response.status_code==400)

def test_signup_wrong_email1():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[5]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Email as enterd is not valid"}
    assert(response.status_code==400)

def test_signup_wrong_email2():
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[6]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Email as enterd is not valid"}
    assert(response.status_code==400)

"""
    A tests on user signup 
        ->The test tests if the user is signed up
        ->the test tests adding of new user to the data base
            1 -> user delight
            2 -> user user
"""

#test registration for a first user
def test_signup_user_unkown1():
    old_num_users=registered()
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[0]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    new_num_users=registered()
    if new_num_users-1==old_num_users:
        assert response.json=={"Successfull":"Proceed to login"}
        assert(response.status_code==200)


#test registration for a second user
def test_signup_user_unkown2():
    old_num_users=registered()
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[3]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    new_num_users=registered()
    if new_num_users-1==old_num_users:
        assert response.json=={"Successfull":"Proceed to login"}
        assert(response.status_code==200)

#test registration for known user
def test_signup_user_known():
    old_num_users=registered()
    result=app.test_client()
    response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg[0]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    new_num_users=registered()
    if old_num_users==new_num_users:
        assert(response.status_code==409)
    assert response.json=={"Email Error": "Email is already linked to another user, pick another one"}


"""
    Fuction to create access token on user login
    takes in username data from mock_reg user
"""
def mock_login_token(uname):
    access_token=create_access_token(uname)
    return access_token

"""
    A test to test user signin endpoint
        -> Empty email field
        -> Empty password field
        -> Wrong user email (no @)
        -> Wrong user email (no .com)

"""
def test_login_empty_email():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[2]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Email field cannot be empty"}
    assert(response.status_code==400)

def test_login_empty_password():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[3]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Password field cannot be empty"}
    assert(response.status_code==400)

def test_login_wrong_email1():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[4]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Email as enterd is not valid"}
    assert(response.status_code==400)

def test_login_wrong_email2():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[5]),content_type='application/json')
    json.loads(response.data.decode('utf-8'))
    assert response.json=={"Error": "Email as enterd is not valid"}
    assert(response.status_code==400)

"""
    -> A test to test if the entered password matches the one stored
    -> A test to check token creation on user login
        -> 1 for the first user

"""
def test_login_wrong_password():
    with app.app_context():
        result=app.test_client()
        response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[1]),content_type='application/json')
        json.loads(response.data.decode('utf-8'))
        assert (response.json=={"Error":"Invalid password"})
        assert(response.status_code==401)
        
def test_login_success():
    with app.app_context():
        result=app.test_client()
        response=result.post('/api/v1/auth/login', data=json.dumps(mock_log[0]),content_type='application/json')
        json.loads(response.data.decode('utf-8'))
        assert (response.json!={mock_reg[0].get('username'): {"Use this token to create a ride":mock_login_token(mock_reg[0].get('username'))}})
