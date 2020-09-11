'''
auth functions for pytest
'''
import re
import jwt
import json
import hashlib
from collections import *
from error import AccessError

userDatabase = []

# Given a user's first and last name, email address, and password
# create a new account for them and return a new token for authentication in their session



####helper function begin #######
def create_uid():
    return len(userDatabase) + 1

def create_token(email):
   encoded_jwt = jwt.encode({'email': email}, 'comp1531', algorithm='HS256')
   return encoded_jwt.decode('utf-8')

# check when register if an email is already existed

def check_email_existed(email):
    for i in range(len(userDatabase)): 
        if str(email) == str(userDatabase[i]['email']):
            raise ValueError('Email has been registered')
    return 

# check when login if an email is not in the user database
# if no error is raised, return the index of this user in user database
def check_email_nonexisted(email):
    index = 0
    flag = 0
    for i in range(len(userDatabase)):
      if str(email) == str(userDatabase[i]['email']):
        index = i
        flag = 1  
    if flag == 0: 
        raise ValueError('Email is not registered')
    
    return index

# chekc if the email format is correct
def check_email_format(email):
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        raise ValueError('email is not valid') 
    return

# check the password format
def check_password(password):
    if len(password) < 6:
        raise ValueError('invalid password')    
    return

# check if length of firstname is correct
def check_firstname(name_first):
    if len(name_first) > 50 or len(name_first) < 1:
        raise ValueError('invalid first name')  
    return

# check if length of lastname is correct
def check_lastname(name_last):
    if len(name_last) > 50 or len(name_last) < 1:
        raise ValueError('invalid last name')   
    return

# hash a target when needed
def hashing(target):
    hashing = hashlib.sha256(target.encode('utf-8')).hexdigest()
    return hashing

# check if a user id is invalid
# if it is valid, return the indec of this user in database
def check_invalid_user(u_id):
    flag = 0
    for i in range(len(userDatabase)): 
        if userDatabase[i]['u_id'] == int(u_id):
            flag = 1
            return i
    if flag == 0:
        raise ValueError('invalid u_id') 

# check if the given permission is invalid
def check_invalid_permission(permission_id):
    if permission_id > 3 or permission_id < 1:
        raise ValueError('invalid permission')
    return
    
    
######helper funtion end########    
    
def auth_register(email, password, name_first, name_last):
    
    # check email existence
    check_email_existed(email)
    #check email format
    check_email_format(email)
    
    # check password
    check_password(password)

    # check frist name
    check_firstname(name_first) 
    
    # check last name 
    check_lastname(name_last)

    user_id = create_uid()
    user_handle = ''.join([name_first, name_last])

    if user_id == 1:
        permission_id = 1
    else:
        permission_id = 3

    userDatabase.append({
        'u_id': user_id,
        'email': email,
        'name_first':name_first,
        'name_last':name_last,
        'handle': user_handle,
        'password': hashing(password),
        'token': create_token(email),
        'email': email,
        'hash':'',
        'permission':permission_id,
        'profile_img_url':'',
        'channel':[],
        'is_login': False
    })
    
    
    return { 
        'u_id': user_id, 
        'token':create_token(email)
    }


   

# Given a registered users' email and password 
# And generates a valid token for the user to remain authenticated

def auth_login(email,password):

   # check the email format
    check_email_format(email)

    # check if the email is in the database
    # if no error is raised, get the index of this user in user database
    index = check_email_nonexisted(email)
    
    # check if the email match the password
    mark = 0
    pass_hash = hashing(password)
    if pass_hash == userDatabase[index]['password'] and userDatabase[index]['is_login'] == False:
        mark = 1
        userDatabase[index]['is_login'] = True
    if mark == 0:            
        raise ValueError('Invalid password')

    return {
        'u_id': userDatabase[index]['u_id'], 
        'token':create_token(email)
    }


# Given an active token, invalidates the token to log the user out. 
# Given a non-valid token, does nothing

def auth_logout(token):
    if any(d['token'] == token for d in userDatabase):
        return True
    else: 
        return False

# Given an email address, if the user is a registered user
# send them a an email containing a specific secret code

def auth_passwordreset_request(email):
    pass

# Given a reset code for a user, set that user's new password to the password provided

def auth_passwordreset_reset(reset_code, new_password):  
    # compare two hashes 
    abc = str(reset_code)
    hash2 = hashing(abc)
    flag = 0
    for i in range(len(userDatabase)):
        if userDatabase[i]['hash'] == hash2:
            userDatabase[i]['password'] = hashing(new_password)
            flag = 1 

    # check reset code
    if flag == 0:
        raise ValueError('Wrong reset code')
    
    # check password length 
    check_password(new_password)

# Given a User by their user ID, set their permissions to new permissions described by permission_id

def permission_change(token, u_id, permission_id):

    # check if a user id is invalid
    # if it is valid, get the index of thid user in database
    index = check_invalid_user(u_id)

    # check if a given permission is invalid
    check_invalid_permission(permission_id)
    
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            if (userDatabase[i]['permission'] == 1 or userDatabase[i]['permission'] == 2):
                # if user is authorized
                # update permission id
                userDatabase[index]['permission'] = int(permission_id)
                print(userDatabase[index]['permission'])
            else: 
                # user is not authorized
                raise AccessError('not autho')
    return  

