from flask_restplus import Api
from flask import Flask
from flask_jwt_extended import JWTManager



"""
    Create an instace of flask
"""
app=Flask(__name__)
api=Api(app)
jwt = JWTManager(app)

"""
    Add a secret key for the app
"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'
app.config['JWT_SECRET_KEY'] = '\xe7\x06K\x86\xe5\x98/\x11\x06\xfbJA\x86'

from resources.signup_user import api as signup
api.add_namespace(signup, path='/api/v1')

from resources.login_user import api as login
api.add_namespace(login, path='/api/v1')


"""from endpoints.rides import api as rides
api.add_namespace(rides, path='/api/v1')
"""