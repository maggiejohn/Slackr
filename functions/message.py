import pytest
import re
import datetime
from error import AccessError
from auth import *
from channel import * 
from queue import Queue

messageDatabase = []
tempList=[]
tempQ = Queue(1000)
time_finished = datetime.datetime.now()
#update

def create_messageid(channel_id, message):
    created_mid = int(channel_id) + 1000 + len(message)
    return created_mid

def get_time (): 
    return datetime.datetime.utcnow()

##################MESSAGE_SENDLATER#################
####################################################

def message_sendlater(token, channel_id, message, time_sent): 
    #check if channelID is valid
    if not any(d['channelId'] == int(channel_id) for d in channelDatabase):  
        raise ValueError("Invalid Channel ID")

    
    #check if message is more than 1000 characters
    elif len(message) > 1000: 
        raise ValueError("Message is too long")

    
    #check if time is in the past
    elif get_time() < time_sent: 
        error_raise.time_is_in_past()
    else: 
        for i in range(len(userDatabase)): 
            if userDatabase[i]['token'] == token:
                u_id = userDatabase[i]['u_id']
                if u_id not in channelDatabase[i]['all_members']:
                    raise AccessError("Not authorized")
    
#not sure how to finish sending..

    pass


################## MESSAGE_SEND#####################
####################################################

def message_send(token, channel_id, message):
    #check if message is more than 1000 characters
    if len(message) > 1000: 
        raise ValueError("Message is too long")
    
    #check if token is a member in channel
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            for j in range(len(channelDatabase)):
                if channelDatabase[j]['channelId'] == int(channel_id):
                    if u_id not in channelDatabase[j]['all_members']:
                        raise AccessError("User not in channel")
    
    #append message to dictionary of dictionaries
    message_id = create_messageid(channel_id, message)
    print(message_id)
    messageDatabase.append({
        'message_id': message_id, 
        'channel_id': channel_id,
        'u_id': u_id, 
        'message': message,
        'time': get_time(), 
        'react_id': 0, 
        'pin_id': 0
    })

    print(messageDatabase)
    return message_id

################## MESSAGE_EDIT#####################
####################################################


def message_edit(token, message_id, message): 
    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            permission_id = userDatabase[i]['permission']

    for i in range(len(messageDatabase)):
        if messageDatabase[i]['message_id'] == int(message_id): 
            #check if owner/admin of channel
            for j in range(len(channelDatabase)): 
                if channelDatabase[j]['channelId'] == int(messageDatabase[i]['channel_id']): 
                    #if not sent by authorised user
                    if ((messageDatabase[i]['u_id'] == u_id) or (permission_id == 1) or (permission_id == 2 ) or (u_id in channelDatabase[j]['owner_members'])): 
                        messageDatabase[i]['message'] = message
                        print(messageDatabase)
                        return None
                    else: 
                        print(messageDatabase)
                        raise AccessError("Not authorized")

    raise ValueError("Message no longer exists")                    
                        
################## MESSAGE_REACT####################
####################################################
def message_react(token, message_id, react_id):
    
    #check if react_id is valid
    if (int(react_id) != 1): 
        raise ValueError("react_id is not valid")

    
    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            permission_id = userDatabase[i]['permission']


    for i in range(len(messageDatabase)): 
        if messageDatabase[i]['message_id'] == int(message_id): 
            if (permission_id != 1 or messageDatabase[i]['react_id'] == 1):
                for l in range(len(channelDatabase)):
                    if channelDatabase[l]['channelId'] == int(messageDatabase[i]['channel_id']):
                        if u_id not in channelDatabase[l]['all_members']:
                            raise ValueError("User not in channel")
                        if int(messageDatabase[i]['react_id']) == 1: 
                            raise ValueError("Message already reacted")
                        else: 
                            messageDatabase[i]['react_id'] = 1
                            return None
            else: 
                messageDatabase[i]['react_id'] = 1
                #print(messageDatabase)
                return None
            
    raise ValueError("Message no longer exists")

################## MESSAGE_UNREACT####################
######################################################

def message_unreact(token, message_id, react_id):

    #check if react_id is valid
    if (int(react_id) != 0): 
        error_raise.invalid_reactID()
    
    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            permission_id = userDatabase[i]['permission']

    for i in range(len(messageDatabase)): 
        if messageDatabase[i]['message_id'] == int(message_id): 
            if (permission_id != 1 or messageDatabase[i]['react_id'] == 0):
                for l in range(len(channelDatabase)):
                    if channelDatabase[l]['channelId'] == int(messageDatabase[i]['channel_id']):
                        if u_id not in channelDatabase[l]['all_members']:
                            raise ValueError("User not in channel")
                        if messageDatabase[i]['react_id'] == 0: 
                            raise ValueError("Message already unreacted")
                        else: 
                            messageDatabase[i]['react_id'] = 0
                            return None
            else: 
                messageDatabase[i]['react_id'] = 0
                print(messageDatabase)
                return None
            
    raise ValueError("Message no longer exists")

################## MESSAGE_PIN######################
####################################################
def message_pin(token,message_id):

    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            permission_id = userDatabase[i]['permission']
            
    for j in range(len(messageDatabase)):
        print (j)
        if (messageDatabase[j]['message_id'] == int(message_id)): 
            print(messageDatabase[j]['message_id'])
            print(message_id)
            print('True')
            if (permission_id != 1 or int(messageDatabase[j]['pin_id']) == 1):
                for l in range(len(channelDatabase)):
                    if channelDatabase[l]['channelId'] == int(messageDatabase[j]['channel_id']):
                        if (u_id not in channelDatabase[l]['all_members']) and (int(messageDatabase[j]['pin_id']) != 1):
                            raise AccessError("u_id is not in this channel")
                        elif (u_id in channelDatabase[l]['owner_members']) and (int(messageDatabase[j]['pin_id']) != 1): 
                            messageDatabase[j]['pin_id'] = 1
                            return None
                if int(messageDatabase[j]['pin_id']) == 1:
                    raise ValueError("Message already pinned")
                elif permission_id == 1: 
                    print(messageDatabase)
                    messageDatabase[j]['pin_id'] = 1
                    print(messageDatabase)
                    return None
                else: 
                    raise ValueError("User not an admin")
        
            else: 
                print(j)
                messageDatabase[j]['pin_id'] = 1
                print(messageDatabase)
                return None

    raise ValueError("Message no longer exists")

################## MESSAGE_UNPIN####################
####################################################
def message_unpin(token, message_id):
    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            permission_id = userDatabase[i]['permission']

    for i in range(len(messageDatabase)):
        if (messageDatabase[i]['message_id'] == int(message_id)): 
            if (permission_id != 1 or int(messageDatabase[i]['pin_id']) == 0):
                for j in range(len(channelDatabase)):
                    if channelDatabase[j]['channelId'] == int(messageDatabase[i]['channel_id']):
                        if u_id not in channelDatabase[j]['all_members'] and (int(messageDatabase[i]['pin_id']) != 0):
                            raise AccessError("u_id is not in this channel")
                        elif u_id in channelDatabase[j]['owner_members'] and (int(messageDatabase[i]['pin_id']) != 0): 
                            messageDatabase[i]['pin_id'] = 0
                            return None

                if int(messageDatabase[i]['pin_id'])== 0:
                    raise ValueError("Message already unpinned")
                elif permission_id == 1: 
                    messageDatabase[i]['pin_id'] = 0
                    return None
                else: 
                    raise ValueError("User not an admin")
                    
            else: 
                messageDatabase[i]['pin_id'] = 0
                print(messageDatabase)
                return None

    raise ValueError("Message no longer exists")


################## MESSAGE_SEARCH###################
####################################################

def search(token,query_str): 

    message_dic = []

    for i in range(len(messageDatabase)):
        print(query_str.lower())
        print(messageDatabase[i]['message'].lower())
        if (query_str.lower() in messageDatabase[i]['message'].lower()) == True: 
            print(query_str)
            print(messageDatabase[i]['message'])
            message_dic.append({
                'message_id': messageDatabase[i]['message_id'],
                'u_id': messageDatabase[i]['u_id'],
                'message': messageDatabase[i]['message'], 
                'time_created':  messageDatabase[i]['time'].strftime("%Y-%m-%d %H:%M:%S"), 
                'reacts': messageDatabase[i]['react_id'], 
                'is_pinned': messageDatabase[i]['pin_id']
            })
    print(message_dic)
    return message_dic


################## MESSAGE_REMOVE###################
####################################################

#Remove message
def message_remove(token, message_id):
#check if message_id is exist in the messageDatabase 
    find_flag = 0
#check raise error when non authorised user or the authorised user is not a admin or owner
#1, token 
    admin_flag = 0
    auth_flag = 0
    for i in range(len(messageDatabase)):
      for channel_id in messageDatabase[i]['channel_id']:
         if messageDatabase[i]['message_id'] == message_id:
           find_flag = 1
#find is admin or owner
           for j in range(len(userDatabase)):
               if userDatabase[j]['token']==token:
                  u_id = userDatabase[j]['u_id']
                  if (u_id  in channelDatabase[j]['all_members'])or (u_id  in channelDatabase[j]['owner_members']):
                      auth_flag = 1
                  if userDatabase[j]['permission'] == 1:
                      admin_flag = 1
#check error
    if auth_flag == 0 and admin_flag == 0:
       raise AccessError("not authorized user or not an admin or owner")     
    if find_flag == 0:
       raise ValueError("Message (based on ID) no longer exists") #Message (based on ID) no longer exists
#remove
    for i in range(len(messageDatabase)):
      for channel_id in messageDatabase[i]['channel_id']:
         if messageDatabase[i]['message_id'] == message_id:
           #remove message here
           #messageDict = messageDatabase[i]
           messageDatabase.pop(i)#drop the dict with messageid from [channelid] 


################## MESSAGE_STANDUP###################
#####################################################

def standup_start(token, channel_id):
#Channel ID is not a valid channel
  flag = 0
  u_id_flag = 0
  c_id_flag = 0
  for i in range(len(channelDatabase)):
   if int(channel_id) == channelDatabase[i]['channelId']:
    flag = 1
  if flag == 0:
   raise AccessError("no channelID")
#Find u_id
  for i in range(len(userDatabase)): 
      if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
#rewrite version
#The authorised user is not a member of the channel that the message is within
  for i in range(len(messageDatabase)):
      if messageDatabase[i]['channel_id'] == channel_id:
         u_id_flag = 1
         if messageDatabase[i]['u_id'] == u_id:
            c_id_flag = 1 
  if c_id_flag == 0:
     raise ValueError("Channel ID is not a valid channel")
#one more error:An active standup is currently running in this channel

  for j in range(len(channelDatabase)):
     if channelDatabase[i]['channelId'] == channel_id:
       if channelDatabase[i]['standup'] != False:
#error raise
          raise ValueError("an active standup is currently running")
       else:
#do the job

#call the send function when the message_id is the newest in the channels
          for i in reversed(range(len(messageDatabase))):
             if messageDatabase[i]['channel_id'] == channel_id:
#active the standup
               for j in range(len(channelDatabase)):
                  if channelDatabase[i]['channelId'] == channel_id:
                     channelDatabase[i]['standup'] = True
                     standup_send(token, channel_id,messageDatabase[i]['message'])
          #time_finish = datetime.datetime.now() + datetime.timedelta(minutes = 15)
          #put the grobol list into channel
          return time_finished


################## MESSAGE_STANDUP_SEND##################
#########################################################


def standup_send(token, channel_id,message):
    #check if channelID is valid
    if not any(d['channelId'] == int(channel_id) for d in channelDatabase):  
        raise ValueError("Channel ID is not a valid channel")
    #check if message is more than 1000 characters
    elif len(message) > 1000: 
        raise ValueError("Message is too long")
    #Find u_id
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
           u_id = userDatabase[i]['u_id']
#The authorised user is not a member of the channel that the message is within
    for i in range(len(messageDatabase)):
        if messageDatabase[i]['channel_id'] == channel_id:
           u_id_flag = 1
           if messageDatabase[i]['u_id'] == u_id:
              c_id_flag = 1 
    if c_id_flag == 0:
       raise AccessError("the user is not a member of channels")
    for j in range(len(channelDatabase)):
       if channelDatabase[i]['channelId'] == channel_id:
         if channelDatabase[i]['standup'] != True:
#error raise
            raise ValueError("No active standup is currently running")

#send  part
    now = datetime.datetime.now()
    time_to_send = now + datetime.timedelta(minutes = 15)
    tempQ.put(message)
    message_id_wait = message_send(token, channel_id, message)
    while  datetime.datetime.now < time_to_send:
        time.sleep(60)
        if message_id_wait != messageDatabase[len(messageDatabase)]['message_id'] and channel_id == messageDatabase[len(messageDatabase)]['channel_id']:
           time_to_send = time_to_send + datetime.timedelta(minutes = 1)
           tempQ.put = messageDatabase[len(messageDatabase)]['message'] # find the newest message
    while tempQ.empty() is not true:
        tempList.append(tempQ.get())
    
    time_finished = time_to_send
    for i in range(len(channelDatabase)):
        if channelDatabase[i]['channelId'] == channel_id:
           channelDatabase[i]['messagelist'] = tempList
    for j in range(len(channelDatabase)):
       if channelDatabase[i]['channelId'] == channel_id:
           channelDatabase[i]['standup'] = False  #turn it off again
# send end
    return {}

