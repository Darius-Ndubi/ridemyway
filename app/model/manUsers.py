import psycopg2
from flask_jwt_extended import create_access_token
from flask import abort,Response,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from app.db import connDb


"""
    A class to handle the registration of users
    The login of users to the site
"""
class DbManager(object):
    def __init__(self,email,username,password):
        self.email=email
        self.password=password
        self.username=username

    def checkUser(self):
        """
            Method to check if a user is registered
            The check is performed through matching emails in  the database
        """
        connection=connDb()
        curs=connection.cursor()
        
        curs.execute("SELECT * FROM new_user WHERE email = %(email)s",{'email':self.email})
        
        self.exists=curs.fetchall()
        
        curs.close()
        connection.commit()
        connection.close()
        
        return (self.exists)


    def signupUser(self):
        """
            Method to add a validated user to the database
            If all checks have passed add the user
        """
        connection=connDb()
        curs=connection.cursor()

        self.passwd_hash=generate_password_hash(self.password)

        curs.execute("INSERT INTO new_user (email,username,password) VALUES(%s,%s,%s)",(self.email,self.username,self.passwd_hash))

        curs.close()
        connection.commit()
        connection.close()

    @staticmethod
    def login(email,password):
        exist=signinusercheck(email)
        if exist:
            #print (self.exist[0][3])
            #compare the has with the one entered
            if check_password_hash(exist[0][3],password):
                #if there is a match give user an access token using there registered username
                access_token = create_access_token(exist[0][2])
                return({exist[0][2]: {"Use this token to create a ride":access_token}})
            #if the hashes dont match
            else:
               return ({"Error":"Invalid password"}),401
        else:
            return({"Error":"User does not exist please register"}),401

       
def signinusercheck(email):
        """
            Email check when user wants to sign in
        """
        connection=connDb()
        curs.connection.cursor()
        #check if email exists 
        curs.execute("SELECT * FROM new_user WHERE email =%(email)s",{'email':email})
        #find the whole row
        existance = curs.fetchall()
        #print (existance)
        curs.close()
        connection.commit()
        connection.close()

        return existance