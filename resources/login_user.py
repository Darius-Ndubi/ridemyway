from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.model.manUsers import DbManager
from flask import jsonify

class User_fields(object):
    parser = reqparse.RequestParser()

    def get_user_login(self):

        self.parser.add_argument('email', required=True,
                            help="email cannot be blank!")
        self.parser.add_argument('password', required=True,
                            help="password cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args

api = Namespace("login",  description="user login endpoint")

R=User_fields()

"""
    User login endpoint
    takes in user:
        ->email
        ->password
"""

class Login(Resource):
    def post (self):
        args = R.get_user_login()

        #validating that  non of the enterd fields is empty
        if args['email'] == "":
            return ({"Error": "Email field cannot be empty"}),400
        elif args['password'] == "":
            return ({"Error": "Password field cannot be empty"}),400

        elif '@' not in args['email']:
            return ({"Error": "Email as enterd is not valid"}),400
        elif '.com' not in args['email']:
            return ({"Error": "Email as enterd is not valid"}),400

        return (DbManager.login(args['email'],args['password']))


api.add_resource(Login, '/auth/login')