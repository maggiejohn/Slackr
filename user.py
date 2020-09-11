'''
functions for user part
'''
import requests
from flask import request
import os
import pytest
import re
import jwt
import json
import hashlib
from collections import *
import error_raise 
from auth import *
from channel import *
from message import *
import helper
import img

####################### user_profile ####################
#########################################################

def user_profile(token, u_id):

    #pickle load
    userDatabase = Load('User_database.pkl')
    
    # check if the user with u_id is not valid
    flag = 0
    for i in range(len(userDatabase)): 
        if userDatabase[i]['u_id'] == int(u_id):
            flag = 1
            email = userDatabase[i]['email']
            name_first = userDatabase[i]['name_first']
            name_last = userDatabase[i]['name_last']
            handle = userDatabase[i]['handle']
            profile_img_url = userDatabase[i]['profile_img_url']
    if flag == 0:
        error_raise.invalid_user()
    
    # return new profile
    else:
        return { 
            'u_id': u_id,
            'email': email, 
            'name_first': name_first,
            'name_last': name_last, 
            'handle_str': handle,
            'profile_img_url':profile_img_url
        }


####################### user_setname ####################
#########################################################

def user_profile_setname(token, name_first, name_last):
    #pickle load 
    userDatabase = Load('User_database.pkl')
    
    # check if first_name and last_name is valid
    helper.check_firstname(name_first)
    helper.check_lastname(name_last)
    
    # update name
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['name_first'] = name_first 
            userDatabase[i]['name_last'] = name_last

    #rewrite userDatabase
    pickle_users(userDatabase)
    return


###################### user_setemail ####################
#########################################################

def user_profile_setemail(token, email):
    #pickle load
    userDatabase = Load('User_database.pkl')


    # check is email is existed
    helper.check_email_format(email)
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token and userDatabase[i]['email'] != email:
            helper.check_email_existed(email)

    # update email
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['email'] = email

    #pickle part 
    pickle_users(userDatabase)
    return


##################### user_sethandle ####################
#########################################################

def user_profile_sethandle(token, handle_str):
    #pickle load
    userDatabase = Load('User_database.pkl')
 

    # check error
    helper.check_handle(handle_str)

    # update handle
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            userDatabase[i]['handle'] =  handle_str
    
    #pickle part 
    pickle_users(userDatabase)
    return 


#################### user_uploadphoto ###################
#########################################################

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end,backurl):
    userDatabase = Load('User_database.pkl')
    r = requests.get(img_url)
    if r.status_code != 200:
        error_raise.invalid_status()
    for i in range(len(userDatabase)):
     if userDatabase[i]['token'] == token:
      u_id = userDatabase[i]['u_id']
      img.image_process(token, img_url, x_start, y_start, x_end, y_end,u_id)
    for i in range(len(userDatabase)):
     if userDatabase[i]['token'] == token:
      userDatabase[i]['profile_img_url'] = backurl + f"static/icon{u_id}.jpg"
      pickle_users(userDatabase)
    return {}
