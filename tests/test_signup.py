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
mock_reg={"email":"yagamidelight@gmail.com","username":"delight","password":"delight"}
mock_reg1={"email":"","username":"delight","password":"delight"}
mock_reg2={"email":"yagamidelight@gmail.com","username":"","password":"delight"}
mock_reg3={"email":"yagamidelight@gmail.com","username":"delight","password":""}

"""
    Mock user data for user login
"""
mock_log={"email":"yagamidelight@gmail.com","password":"delight"}
mock_log1={"email":"yagamidelight@gmail.com","password":"delhight"}

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
    the test tests adding of new user to the data base
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

"""

        A test to test if the email field is empty
    
    def test_signup():
        #old_num_users=registered()
        result=app.test_client()
        response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg1),content_type='application/json')
        #new_num_users=registered()
        data_input=json.loads(response.data.decode('utf-8'))
        if data_input.get('email')=="":
        #assert(old_num_users==new_num_users)
            assert response.json=={'Error': 'Email field cannot be empty'}
            assert(response.status_code==401)

    
        A test to test if username entered is empty
    
    def test_signup():
        #old_num_users=registered()
        result=app.test_client()
        response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg2),content_type='application/json')
        #new_num_users=registered()
        data_input=json.loads(response.data.decode('utf-8'))
        if data_input.get('username')=="":
        #assert(old_num_users==new_num_users)
            assert response.json=={"Error": "Username field cannot be empty"}
            assert(response.status_code==401)

    
        A test to test if password entered is empty
    
    def test_signup():
        #old_num_users=registered()
        result=app.test_client()
        response=result.post('/api/v1/auth/signup', data=json.dumps(mock_reg3),content_type='application/json')
        #new_num_users=registered()
        data_input=json.loads(response.data.decode('utf-8'))
        if data_input.get('password')=="":
        #assert(old_num_users==new_num_users)
            assert response.json=={"Error": "Password fields cannot be empty"}
            assert(response.status_code==401)

"""
"""
    Fuction to create access token on user login
    takes in username data from mock_reg user
"""
def mock_login_token():
    access_token=create_access_token(mock_reg.get('username'))
    return access_token

"""
    A test to test user signin endpoint
"""
def test_login():
    result=app.test_client()
    response=result.post('/api/v1/auth/login', data=json.dumps(mock_log),content_type='application/json')
    log_input=json.loads(response.data.decode('utf-8'))
    if log_input.get('email')=="":
        assert response.json=={"Error": "Email field cannot be empty"}
        assert(response.status_code==401)
    elif log_input.get('password')=="":
        assert response.json=={"Error": "Password field cannot be empty"}
        assert(response.status_code==401)
"""
    A test to test if the entered password matches the one stored
"""

def test_login():
    with app.app_context():
        result=app.test_client()
        response=result.post('/api/v1/auth/login', data=json.dumps(mock_log1),content_type='application/json')
        json.loads(response.data.decode('utf-8'))
        assert (response.json=={"Error":"Invalid password"})
        assert(response.status_code==401)


"""
    A test to check token creation on user login
"""   
        
def test_login():
    with app.app_context():
        result=app.test_client()
        response=result.post('/api/v1/auth/login', data=json.dumps(mock_log),content_type='application/json')
        json.loads(response.data.decode('utf-8'))
        assert (response.json!={mock_reg.get('username'): {"Use this token to create a ride":mock_login_token()}})