'''
user functions for pytest
'''
import pytest
import re
import jwt
import json
import hashlib
from collections import *
from auth import *

###### helper function begin #######

# check if length of firstname is correct
def check_firstname(name_first):
    if len(name_first) > 50 or len(name_first) < 1:
        raise ValueError("Invalid first name")  
    return

# check if length of lastname is correct
def check_lastname(name_last):
    if len(name_last) > 50 or len(name_last) < 1:
        raise ValueError("Invalid last name") 
    return

def check_email_format(email):
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        raise ValueError("Email is not valid")
    return

def check_email_existed(email):
    for i in range(len(userDatabase)): 
        if str(email) == str(userDatabase[i]['email']):
            raise ValueError("Email has been registered")
    return 
    
# check length of handle
def check_handle(handle_str):
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise ValueError("Handle must be between 3 and 50 characters")
    for i in range(len(userDatabase)):
        if userDatabase[i]['handle'] == handle_str:
            raise ValueError("Handle is used by another user")

###### helper function end #######

# For a valid user, returns information about their email, first name, last name, and handle
def user_profile(token, u_id):
    
    # check error
    flag = 0
    for i in range(len(userDatabase)): 
        if userDatabase[i]['u_id'] == int(u_id):
            flag = 1
            email = userDatabase[i]['email']
            name_first = userDatabase[i]['name_first']
            name_last = userDatabase[i]['name_last']
            handle = userDatabase[i]['handle']
    if flag == 0:
        raise ValueError("User does not exist")
    
    # return new profile
    else:
        return { 
            'email': email, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': handle
        }

# Update the authorised user's first and last name
def user_profile_setname(token, name_first, name_last):
    
    # check error
    check_firstname(name_first)
    check_lastname(name_last)

    # update name
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['name_first'] = name_first 
            userDatabase[i]['name_last'] = name_last

    return {}

# Update the authorised user's email address
def user_profile_setemail(token, email):

    # check error
    check_email_format(email)
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token and userDatabase[i]['email'] != email:
            check_email_existed(email)

    # update email
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['email'] = email
    
    return {}

# Update the authorised user's handle (i.e. display name)
def user_profile_sethandle(token, handle_str):

    # check error
    check_handle(handle_str)

    # update handle
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['handle'] =  handle_str

    return {}

# untestable
# Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). 
# Position (0,0) is the top left.
def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    pass

