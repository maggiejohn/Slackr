import pytest
import re
import os
import jwt
import json
import hashlib
from collections import *
import error_raise 
import pickle 


userDatabase = []
channelDatabase = []
messageDatabase = []
userAll = []
standupDatabase = []

def pickle_users(userDatabase):
    with open('User_database.pkl','wb') as f:
        pickle.dump(userDatabase,f)

# use of pickle
def Load(filename):
  if os.path.exists(filename) is True:
    if os.path.getsize(filename) > 0:
      with open(filename,'rb') as f:
          a = pickle.load(f)
          return a
    else:
      return []
  else:
      f = open(filename,'wb')
      f.close()
      return []

# Generate user id, increment by 1 every time
def create_uid():
    if os.path.exists('User_database.pkl') is True:
        d = Load('User_database.pkl')
        return len(d) + 1
    else:
        return 1


##################### auth_register #####################
#########################################################

def auth_register(email, password, name_first, name_last):   
    
    # pickle start
    userDatabase = Load('User_database.pkl')    
    
    # check email existence
    helper.check_email_existed(email)

    # check email format 
    helper.check_email_format(email)
    
    # check password
    helper.check_password(password)

    # check frist name
    helper.check_firstname(name_first) 
    
    # check last name 
    helper.check_lastname(name_last)

    user_id = create_uid()
    user_handle = ''.join([name_first, name_last])
    # define permission
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
        'password': helper.hashing(password),
        'token': helper.create_token(email),
        'email': email,
        'hash':'',
        'permission':permission_id,
        'profile_img_url':'',
        'channel':[],
        'is_login': False
    })
    
    #pickle part 
    pickle_users(userDatabase)
    
    return { 
        'u_id': user_id, 
        'token':helper.create_token(email)
    }

####################### auth_login ######################
#########################################################

def auth_login(email,password):
    #pickle start
    userDatabase = Load('User_database.pkl')

    # check the email format
    helper.check_email_format(email)

    # check if the email is in the database
    # if no error is raised, get the index of this user in user database
    index = helper.check_email_nonexisted(email)
    
    # check if the email match the password
    mark = 0
    pass_hash = helper.hashing(password)
    if pass_hash == userDatabase[index]['password'] and userDatabase[index]['is_login'] == False:
        mark = 1
        userDatabase[index]['is_login'] = True
    if mark == 0:            
        error_raise.invalid_password()

    return {
        'u_id': userDatabase[index]['u_id'], 
        'token':helper.create_token(email)
    }


####################### auth_logout #####################
#########################################################

def auth_logout(token):
    #pickle start
    userDatabase = Load('User_database.pkl')
    #pickle done
    if any(d['token'] == token for d in userDatabase):
        return True
    else: 
        return False

############# auth_passwordreset_request ################
#########################################################

def auth_passwordreset_request(email):
    #pickle start
    userDatabase = Load('User_database.pkl')
    #pickle done
    if any(d['email'] == email for d in userDatabase):
        return email


############## auth_passwordreset_reset #################
#########################################################

def auth_passwordreset_reset(reset_code, new_password):
    #pickle start
    userDatabase = Load('User_database.pkl')
    #pickle done
    
    # compare two hashes 
    abc = str(reset_code)
    hash2 = helper.hashing(abc)
    flag = 0
    for i in range(len(userDatabase)):
        if userDatabase[i]['hash'] == hash2:
            userDatabase[i]['password'] = helper.hashing(new_password)
            flag = 1
    pickle_users(userDatabase)  

    # check reset code
    if flag == 0:
        error_raise.invalid_reset_code()
    
    # check password length 
    helper.check_password(new_password)


################## permission_cahnge ####################
#########################################################

def permission_change(token, u_id, permission_id):
    
    #pickle start
    userDatabase = Load('User_database.pkl')
    #pickle done 
    permission_id = int(permission_id)

    # check if a user id is invalid
    # if it is valid, get the index of thid user in database
    index = helper.check_invalid_user(u_id)

    # check if a given permission is invalid
    check_invalid_permission(permission)
    
    for i in range(len(userDatabase)):
        if userDatabase[i]['token'] == token:
            if (userDatabase[i]['permission'] == 1 or userDatabase[i]['permission'] == 2):
                # if user is authorized
                # update permission id
                userDatabase[index]['permission'] = permission_id 
                print(userDatabase[index]['permission'])
            else: 
                # user is not authorized
                error_raise.unable_to_operate()
    pickle_users(userDatabase)
    return  
    

######################## user_all #######################
#########################################################

def user_all(token):
    #pickle start
    userDatabase = Load('User_database.pkl')
    #pickle done 
    for i in range(len(userDatabase)):
      userAll.append({
        'u_id': userDatabase[i]['u_id'],
        'email': userDatabase[i]['email'],
        'name_first':userDatabase[i]['name_first'],
        'name_last':userDatabase[i]['name_last'],
        'handle': userDatabase[i]['handle'],
        'profile_img_url':userDatabase[i]['profile_img_url']
     })
    return {'users':userAll}
import helper