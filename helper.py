'''
helper functions
'''
import pytest
import re
import os
import jwt
import json
import hashlib
from collections import *
import error_raise 
import auth
import message
import channel
from datetime import datetime
import time
from queue import Queue
from datetime import timezone


# Generate token
def create_token(email):
   encoded_jwt = jwt.encode({'email': email}, 'comp1531', algorithm='HS256')
   return encoded_jwt.decode('utf-8')

# check when register if an email is already existed
def check_email_existed(email):
    userDatabase = auth.Load('User_database.pkl')
    for i in range(len(userDatabase)): 
        if str(email) == str(userDatabase[i]['email']):
            error_raise.existed_email()
    return 

# check when login if an email is not in the user database
# if no error is raised, return the index of this user in user database
def check_email_nonexisted(email):
    userDatabase = auth.Load('User_database.pkl')
    index = 0
    flag = 0
    for i in range(len(userDatabase)):
      if str(email) == str(userDatabase[i]['email']):
        index = i
        flag = 1  
    if flag == 0: 
        error_raise.not_registered_email()
    
    return index

# chekc if the email format is correct
def check_email_format(email):
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        error_raise.invalid_email() 
    return

# check the password format
def check_password(password):
    if len(password) < 6:
        error_raise.invalid_password()    
    return

# check if length of firstname is correct
def check_firstname(name_first):
    if len(name_first) > 50 or len(name_first) < 1:
        error_raise.invalid_first_name()  
    return

# check if length of lastname is correct
def check_lastname(name_last):
    if len(name_last) > 50 or len(name_last) < 1:
        error_raise.invalid_last_name()   
    return

# check length of handle
def check_handle(handle_str):
    userDatabase = auth.Load('User_database.pkl')
    if len(handle_str) < 3 or len(handle_str) > 20:
        error_raise.invalid_handle()
    for i in range(len(userDatabase)):
        if userDatabase[i]['handle'] == handle_str:
            error_raise.existed_handle()

# hash a target when needed
def hashing(target):
    hashing = hashlib.sha256(target.encode('utf-8')).hexdigest()
    return hashing

# check if a user id is invalid
# if it is valid, return the indec of this user in database
def check_invalid_user(u_id):
    userDatabase = auth.Load('User_database.pkl')
    flag = 0
    for i in range(len(userDatabase)): 
        if userDatabase[i]['u_id'] == int(u_id):
            flag = 1
            return i
    if flag == 0:
        error_raise.invalid_user() 

# check if the given permission is invalid
def check_invalid_permission(permission_id):
    if permission_id > 3 or permission_id < 1:
        error_raise.invalid_permission()
    return

# given a token, find the user id
def find_id_from_token(token):
    userDatabase = auth.Load('User_database.pkl')
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            return u_id
           
# given a token, find the permission
def find_permission_from_token(token):
    userDatabase = auth.Load('User_database.pkl')
    for i in range(len(userDatabase)):
      if userDatabase[i]['token'] == token:
        permission = userDatabase[i]['permission']
        return permission
     
# check if a channel id is valid
def check_channel_id(channel_id):
    channelDatabase = auth.Load('Channel_database.pkl')
    flag = 0
    for i in range(len(channelDatabase)):
        if int(channel_id) == channelDatabase[i]['channelId']:
            flag = 1
    if flag == 0:
        error_raise.invalid_channelid()
# Check if there is a standup currently
def current_standup(channel_id):
    for i in range(len(standupDatabase)):
        if standupDatabase[i]['channelId'] == channel_id and standupDatabase[i]['is_active'] == True:
            # if there is a standup, return its index in the standup database
            return i
        else:
            return False


### helper functions for messages
def create_messageid(channel_id, message):
    
    messageDatabase = auth.Load('Message_database.pkl')
    
    id = 0
    if len(messageDatabase) == 0: 
        created_mid = 100001 
    else: 
        for i in range(len(messageDatabase)):
            id = int(messageDatabase[i]['message_id'])
        created_mid = id + 1
    return created_mid

def get_time (): 
    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return timestamp

def timerStart(timestart):
    global timer
    timer = timestart

def timerGoing():
    global timer
    now = get_time() - 39600
    if (timer - now) > 0: 
        return True
    else: 
        return False

def check_message_length(message):
    if len(message) > 1000: 
        error_raise.message_too_long()


def find_user_permission(token): 
    userDatabase = auth.Load('User_database.pkl')
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            return userDatabase[i]['permission']

def check_exist(database, value, key): 
    if any(d[key] == value for d in database): 
        return  True
    else: 
        return False

def get_index (database, value, key): 
    return next((index for (index, d) in enumerate(database) if d[key] == value), None)

def check_react_id(react_id): 
    if react_id != 1: 
        error_raise.invalid_reactID()
            
def change_react_append(database, user_list_key, check_react_key, u_id): 
    database[check_react_key] = bool(True)
    database[user_list_key].append(u_id)

def change_react_remove(database, user_list_key, check_react_key, u_id):
    database[check_react_key] = bool(False)
    database[user_list_key].remove(u_id)

def check_pin_status (database, boolean): 
    if boolean == False and database == False: 
        error_raise.already_unpinned()
    elif boolean == True and database == True: 
        error_raise.already_pinned()

def check_valid_member(channel_database, member_key, owner_key, pin_id, value): 
    if (value not in channel_database[member_key]) and (pin_id == False): 
        error_raise.invalid_member()
    elif (value in channel_database[owner_key]) and (pin_id == False): 
        return True

def check_if_owner(permission_id): 
    if permission_id != 1: 
        error_raise.not_an_admin()

def check_if_authorised_toedit(value, permission_id, message_database, channel_database): 
    if (message_database == value) or (permission_id == 1) or (permission_id == 2 ) or (value in channel_database): 
        return True
    else: 
        error_raise.unable_to_operate()






#check if the channel to create already has the same name
def check_channel_name(name):
    channelDatabase = auth.Load('Channel_database.pkl')
    if any(d['channelName'] == name for d in channelDatabase): 
      error_raise.channelname_exist() 
      
      
#check if the channel to create has invalid name(>20)     
def check_invalid_channelname(name):
    if len(name) > 20: 
     error_raise.invalid_channelname() 
    
#check if the user is registered/existed
def check_user_existed(u_id):
    userDatabase = auth.Load('User_database.pkl')
    if not any(d['u_id'] == int(u_id) for d in userDatabase):
     error_raise.invalid_user()   
    
    
    
#check if the user we wanto invite is already a member of the channel  
def check_already_member(channel_id,u_id):
    channelDatabase = auth.Load('Channel_database.pkl')
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id):
        if any(d['u_id'] == int(u_id) for d in channelDatabase[i]['all_members']): 
          error_raise.already_member()
  
          
#check if the user we wanto add as owner is already an owner of the channel
def check_already_owner(channel_id,u_id):
   channelDatabase = auth.Load('Channel_database.pkl')
   for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == int(channel_id):
      if any(d['u_id'] == u_id for d in channelDatabase[i]['owner_members']):
        error_raise.already_owner()
        
#check if we are not in the channel we wanto leave
def check_authorized_user(token,channel_id):
    channelDatabase = auth.Load('Channel_database.pkl')
    for i in range(len(channelDatabase)):
      if int(channel_id) == channelDatabase[i]['channelId']:
        u_id = find_id_from_token(token)
        if not any(d['u_id'] == u_id for d in channelDatabase[i]['all_members']):
          error_raise.invalid_member() 
          
#check when the channel is private and i am not
def check_not_autho_join(token,channel_id):
    channelDatabase = auth.Load('Channel_database.pkl')
    permission = find_permission_from_token(token)         
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id) and channelDatabase[i]['is_public'] == "False" and (int(permission) != 1):
        error_raise.private_channel()
        
#check heck if i am not an admin or owner of this channel so i cannot add others
def check_not_autho_add(token,channel_id):
    permission = find_permission_from_token(token) 
    u_id = find_id_from_token(token) 
    channelDatabase = auth.Load('Channel_database.pkl')      
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id):
        if (int(permission) != 1) and (not any(d['u_id'] == int(u_id) for d in channelDatabase[i]['owner_members'])):
         error_raise.unable_to_operate() 
         
#check the user we wanto remove its owner is not an owner
def check_not_owner(channel_id,u_id):
  channelDatabase = auth.Load('Channel_database.pkl')
  for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == channel_id:
     if not any(d['u_id'] == int(u_id) for d in channelDatabase[i]['owner_members']):
      error_raise.not_owner() 