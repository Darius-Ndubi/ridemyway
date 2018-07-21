from flask_restplus import Api,Namespace,Resource,fields,reqparse
from app.model.manUsers import DbManager
from flask import jsonify

class User_fields(object):
    parser = reqparse.RequestParser()

    def get_user_dits(self):

        self.parser.add_argument('username', required=True,
                                    help="Username cannot be blank!")
        self.parser.add_argument('password', required=True,
                                    help="Password cannot be blank!")
        self.parser.add_argument('email', required=True,
                                    help="Email cannot be blank!")

        self.args = self.parser.parse_args()

        return self.args

api = Namespace("signup",  description="user authentication endpoints")

R=User_fields()

"""
    User sign up enpoint
    takes in user:
        ->email
        ->username
        ->password
"""

class Signup(Resource):
    def post (self):
        self.args=R.get_user_dits()

        #validating that  non of the enterd fields is empty
        if self.args['email'] == "":
            return ({"Error": "Email field cannot be empty"}),401
        elif self.args['username'] == "":
            return ({"Error": "Username field cannot be empty"}),401
        elif self.args['password'] == "":
            return ({"Error": "Password fields cannot be empty"}),401
        #check if the email has @ and .com
        elif '@' and '.com' not in self.args['email']:
            return ({"Error": "Email as enterd is not valid"}),401

        self.new_user=DbManager(email=self.args['email'],username=self.args['username'],password=self.args['password'])

        #check if the usr exists
        self.exist=self.new_user.checkUser()
        #if user is found give info why they cant be registerd
        if self.exist:
            return({"Email Error":"Email is already linked to another user, pick another one"}),406
        #if not found allow them to register with us
        else:
            self.new_user.signupUser()
            return({"Successfull":"Proceed to login"})


            


api.add_resource(Signup, '/auth/signup')
