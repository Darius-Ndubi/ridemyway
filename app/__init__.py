from flask_restplus import Api
from flask import Flask
#from flask_jwt_extended import JWTManager



"""
    Create an instace of flask
"""
app=Flask(__name__)
api=Api(app)
#jwt = JWTManager(app)

"""
    Add a secret key for the app
"""
app.secret_key = '\xaa\x98\xfb\xf7\xcb\xce\xd3\xdf\x96'
#app.config['JWT_SECRET_KEY'] = '\xe7\x06K\x86>\xe5\x98/\x11\x06\xfbJA\x$

from resources.users import api as users
api.add_namespace(users, path='/api/v1')

"""from endpoints.rides import api as rides
api.add_namespace(rides, path='/api/v1')
"""