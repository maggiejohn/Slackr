import pytest
import re
from datetime import datetime
import time
import error_raise
import helper
import auth
import os
import channel
from queue import Queue
from datetime import timezone
import pickle

tempList=[]
tempQ = Queue(1000)
time_finished = datetime.now()
timer = None


#use for pickle
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


def pickle_message(messageDatabase):
    with open('Message_database.pkl','wb') as f:
        pickle.dump(messageDatabase,f)

def pickle_standup(standupDatabase):
    with open('Standup_database.pkl','wb') as f:
        pickle.dump(standupDatabase,f)

def pickle_users(userDatabase):
    with open('User_database.pkl','wb') as f:
        pickle.dump(userDatabase,f)

def pickle_channels(channelDatabase):
    with open('Channel_database.pkl','wb') as f:
        pickle.dump(channelDatabase,f)


##################MESSAGE_SENDLATER#################
####################################################
def message_sendlater(token, channel_id, message, time_sent): 
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    timesent = int(time_sent)

    helper.check_message_length(message)

    if helper.check_exist(channelDatabase, int(channel_id), 'channelId') == False: 
        error_raise.invalid_channelid()
        
    #check if time is in the past
    elif helper.get_time() < int(timesent): 
        error_raise.time_is_in_past()

    else: 
        u_id = helper.find_id_from_token(token)
        for j in range(len(channelDatabase)):
            if channelDatabase[j]['channelId'] == int(channel_id):
                if helper.check_exist(channelDatabase[j]['all_members'], u_id, 'u_id') == False:
                    error_raise.unable_to_operate()

    helper.timerStart(timesent)

    while helper.timerGoing(): 
        print("still going")
        time.sleep(2) 
    
    return message_send(token, channel_id, message)


################## MESSAGE_SEND#####################
####################################################
#working
def message_send(token, channel_id, message):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    #check if message is more than 1000 characters
    helper.check_message_length(message)

    u_id = helper.find_id_from_token(token)

    for j in range(len(channelDatabase)):
        if channelDatabase[j]['channelId'] == int(channel_id):
            if helper.check_exist(channelDatabase[j]['all_members'], u_id, 'u_id') == True:
                message_id = helper.create_messageid(int(channel_id), message)
                print(messageDatabase)
                #if helper.check_exist(channelDatabase[j]['messagelist'], message_id, 'message_id') == False:
                #if not any(d['messagelist'] == message_id for d in channelDatabase): 
                if message_id not in channelDatabase[j]['messagelist']:
                    channelDatabase[j]['messagelist'].append(message_id)
                messageDatabase.append({
                    'message_id': message_id, 
                    'u_id': u_id,
                    'channel_id': channel_id,
                    'message': message,
                    'time': helper.get_time(), 
                    'react_id': [{'react_id': 1,
                                'u_ids':[], 
                                'is_this_user_reacted': bool(False)}], 
                    'is_pinned': False
                })
                pickle_users(userDatabase)
                pickle_channels(channelDatabase)
                pickle_message(messageDatabase)

                return {'message_id': message_id}
            else: 
                error_raise.user_not_in_channel()

################## MESSAGE_EDIT#####################
####################################################

def message_edit(token, message_id, message): 
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    #Find user_id and permission_id
    u_id = helper.find_id_from_token(token)
    permission_id = helper.find_user_permission(token)

    if helper.check_exist(messageDatabase, int(message_id), 'message_id') == True:
        i = helper.get_index (messageDatabase, int(message_id), 'message_id')
        for j in range(len(channelDatabase)): 
            if channelDatabase[j]['channelId'] == int(messageDatabase[i]['channel_id']): 
                #if not sent by authorised user
                helper.check_if_authorised_toedit(u_id, permission_id, messageDatabase[i]['u_id'], channelDatabase[j]['owner_members'])
                messageDatabase[i]['message'] = message
                pickle_users(userDatabase)
                pickle_channels(channelDatabase)
                pickle_message(messageDatabase)
                print(message)
                return {}      

################## MESSAGE_REACT####################
####################################################

def message_react(token, message_id, react_id):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

   
    #check if react_id is valid and find u_id
    helper.check_react_id(int(react_id))
    u_id = helper.find_id_from_token(token)

    if helper.check_exist(messageDatabase,int(message_id), 'message_id') == True:
        index_d = helper.get_index (messageDatabase,int(message_id), 'message_id')
        if helper.check_exist(channelDatabase, int(messageDatabase[index_d]['channel_id']), 'channelId') == True:
            index_e = helper.get_index(channelDatabase,int(messageDatabase[index_d]['channel_id']), 'channelId')
            if helper.check_exist(channelDatabase[index_e]['all_members'], u_id, 'u_id') == True:
                index_f = helper.get_index(messageDatabase[index_d]['react_id'], 1, 'react_id')
                for key, value in messageDatabase[index_d]['react_id'][index_f].items(): 
                    if key == 'is_this_user_reacted' and value == True:
                        error_raise.already_reacted()
                helper.change_react_append(messageDatabase[index_d]['react_id'][index_f], 'u_ids', 'is_this_user_reacted', u_id)
                pickle_message(messageDatabase)

            else: 
                error_raise.message_invalid()

    #pickle_channels(channelDatabase)
    return {}
################## MESSAGE_UNREACT####################
######################################################

def message_unreact(token, message_id, react_id):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    #check if react_id is valid and find u_id
    helper.check_react_id(int(react_id))
    u_id = helper.find_id_from_token(token)    
    
    if helper.check_exist(messageDatabase, int(message_id), 'message_id') == True:
        index_d = helper.get_index (messageDatabase,int(message_id), 'message_id')
        if helper.check_exist(channelDatabase, int(messageDatabase[index_d]['channel_id']), 'channelId') == True:
            index_e = helper.get_index(channelDatabase,int(messageDatabase[index_d]['channel_id']), 'channelId')
            if helper.check_exist(channelDatabase[index_e]['all_members'], u_id, 'u_id') == True:
                index_f = helper.get_index(messageDatabase[index_d]['react_id'], 1, 'react_id')
                for key, value in messageDatabase[index_d]['react_id'][index_f].items(): 
                    if key == 'is_this_user_reacted' and value == False:
                        error_raise.already_unreacted()
                helper.change_react_remove(messageDatabase[index_d]['react_id'][index_f], 'u_ids', 'is_this_user_reacted', u_id) 
                pickle_message(messageDatabase)
            else: 
                error_raise.message_invalid()

   # pickle_channels(channelDatabase)
    #pickle_message(messageDatabase)
    return {}
################## MESSAGE_PIN######################
####################################################
def message_pin(token,message_id):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')
    
    #Find user_id and permission_id
    u_id = helper.find_id_from_token(token)
    permission_id = helper.find_user_permission(token)

    for j in range(len(messageDatabase)):
        if (messageDatabase[j]['message_id'] == int(message_id)): 
            if (permission_id != 1 or messageDatabase[j]['is_pinned'] == True):
                for l in range(len(channelDatabase)):
                    if channelDatabase[l]['channelId'] == int(messageDatabase[j]['channel_id']):
                        helper.check_valid_member(channelDatabase[l], 'all_members', 'owner_members', messageDatabase[j]['is_pinned'],u_id)
                        messageDatabase[j]['is_pinned'] = True
                        pickle_message(messageDatabase)
                        return {}
                helper.check_pin_status (messageDatabase[j]['is_pinned'], True)
                helper.check_if_owner(permission_id)
                messageDatabase[j]['is_pinned'] = True
                pickle_message(messageDatabase)
                return {}
            else: 
                messageDatabase[j]['is_pinned'] = True
                pickle_message(messageDatabase)
                return {}

    error_raise.invalid_messageID()

################## MESSAGE_UNPIN####################
####################################################
def message_unpin(token, message_id):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    #Find user_id and permission_id
    u_id = helper.find_id_from_token(token)
    permission_id = helper.find_user_permission(token)

    for j in range(len(messageDatabase)):
        if (messageDatabase[j]['message_id'] == int(message_id)): 
            if (permission_id != 1 or messageDatabase[j]['is_pinned'] == False):
                for l in range(len(channelDatabase)):
                    if channelDatabase[l]['channelId'] == int(messageDatabase[j]['channel_id']):
                        helper.check_valid_member(channelDatabase[l], 'all_members', 'owner_members', messageDatabase[j]['is_pinned'],u_id)
                        helper.messageDatabase[j]['is_pinned'] = False
                        pickle_message(messageDatabase)
                        return {}
                helper.check_pin_status (messageDatabase[j]['is_pinned'], False)
                helper.check_if_owner(permission_id)
                messageDatabase[j]['is_pinned'] = False
                pickle_message(messageDatabase)
                return {}
            else: 
                messageDatabase[j]['is_pinned'] = False
                pickle_message(messageDatabase)
                return {}

    error_raise.invalid_messageID()
    
################## MESSAGE_REMOVE###################
####################################################

#Remove message
def message_remove(token, message_id):
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')
    #Find user_id and permission_id
    u_id = helper.find_id_from_token(token)
    permission_id = helper.find_user_permission(token)

    #check if message exists in database
    if helper.check_exist(messageDatabase, int(message_id), 'message_id') == False:
        error_raise.invalid_messageID() 
    
    #check raise error when non authorised user or the authorised user is not a admin or owner
    message_index = helper.get_index (messageDatabase,int(message_id), 'message_id')
    
    channel_id = messageDatabase[message_index]['channel_id']
    
    if helper.check_exist(channelDatabase, int(channel_id), 'channelId') == False:
        error_raise.invalid_channelid()
    
    channel_index = helper.get_index (channelDatabase,int(channel_id), 'channelId')

    print(u_id)
    print(type(u_id))

    print(permission_id)
    print(type(permission_id))

    print(channel_index)
    print(type(channel_index))

    helper.check_if_authorised_toedit(u_id, permission_id, messageDatabase[message_index]['u_id'], channelDatabase[channel_index]['owner_members'])
    channelDatabase[channel_index]['messagelist'].remove(int(message_id))
    a = {}
    a = messageDatabase.pop(message_index)
    pickle_channels(channelDatabase)
    pickle_message(messageDatabase)
    return {}

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
####ALL BELOW NOT WORKING

################## MESSAGE_SEARCH###################
####################################################

def search(token,query_str): 
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')

    u_id = helper.find_id_from_token(token)

    message_dic = []

    for i in range(len(messageDatabase)):
        print(i)
        if (query_str.lower() in messageDatabase[i]['message'].lower()) == True: 
            print("True")
            message_dic.append({
                'message_id': messageDatabase[i]['message_id'], 
                'u_id': messageDatabase[i]['u_id'], 
                'message': messageDatabase[i]['message'],
                'time_created': messageDatabase[i]['time'], 
                'reacts':  messageDatabase[i]['react_id'], #[{ 'react_id': 1, 'u_ids': [1], 'is_this_user_reacted':0 }],
                'is_pinned':messageDatabase[i]['is_pinned']
            })
    print(message_dic)
    return { 'messages': message_dic}



################## STANDUP_ACTIVE ####################
#####################################################

def standup_active(token, channel_id):
    #pickle start
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')
    standupDatabase = Load('Standup_database.pkl')
    #pickle done

    # Check channel id 
    helper.check_channel_id(channel_id)

    for i in range(len(standupDatabase)):

        if standupDatabase[i]['channel_id'] == channel_id and standupDatabase[i]['is_active'] == True:
            return {
                'is_active': True,
                'time_finish': standupDatabase[i]['time_finish']
            }
        else:
            # When a channel have not started any standups
            return {
                'is_active': False,
                'time_finish': None
            }
    

################## STANDUP_START ####################
#####################################################

def standup_start(token, channel_id, length):

    #pickle start
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')
    standupDatabase = Load('Standup_database.pkl')
    #pickle done

    print(type(channel_id))
    # Check channel id
    helper.check_channel_id(channel_id)
    
    # Check if an active standup is currently running in this channel
    u_id = find_id_from_token(token)
    active = current_standup(channel_id)
    if active != False:
        error_raise.already_have_standup()

    now = datetime.datetime.now()
    time_start = now.timestamp
    time_finish = time_start + length
    member_list = []

    # record all the member for this standup
    for i in range(len(channelDatabase)):
        if channelDatabase[i]['channelId'] == channel_id:
            member_list = channelDatabase[i]['all_member']
    
    standupDatabase.append({
        'channel_id': channel_id,
        'length': length,
        'token': token,
        'is_active': True,
        'time_start': time_start,
        'time_finish': time_finish,
        'message': [],
        'member': member_list
    })

    end_time = time.time() + length
    while time.time() < end_time:
        for i in range(len(messageDatabase)):
            if messageDatabase[i]['time'] > time_start and messageDatabase[i]['time'] < time_finish and messageDatabase[i]['channel_id'] == channel_id:
                # find the sender's token of the message send
                sender_token = find_token_from_id(messageDatabase[i]['u_id'])
                standup_send(sender_token, channel_id, messageDatabase[i]['message'])
    
    # when standup finishes, the begginer send the package of message
    index = current_standup(channel_id)
    message_string = ""
    for i in range(standupDatabase[index]['message']):
        message_string += standupDatabase[index]['message'][i]
    message_send(token, channel_id, message_string)
    # change status of standup database
    standupDatabase[index]['is_active'] = False

    pickle_users(userDatabase)
    pickle_channels(channelDatabase)
    pickle_message(messageDatabase)

    return time_finish


################## MESSAGE_STANDUP_SEND##################
#########################################################

def standup_send(token, channel_id, message):

    #pickle start
    channelDatabase = Load('Channel_database.pkl')
    userDatabase = Load('User_database.pkl')
    messageDatabase = Load('Message_database.pkl')
    standupDatabase = Load('Standup_database.pkl')
    #pickle done

    # Check if channelID is valid
    # If not any(d['channelId'] == int(channel_id) for d in channelDatabase):  
    helper.check_channel_id(channel_id)

    # Check if message is more than 1000 characters
    if len(message) > 1000: 
        error_raise.message_too_long()
    
    # Check if there is a standup
    # If there is a standup, its index in the database will be returned, so active == index
    active = current_standup(channel_id)
    if active == False:
        error_raise.have_no_standup()

    # The authorised user is not a member of the channel that the message is within
    u_id = find_id_from_token(token)
    for i in range(len(messageDatabase)):
        if messageDatabase[i]['channel_id'] == channel_id:
           u_id_flag = 1
           if messageDatabase[i]['u_id'] == u_id:
              c_id_flag = 1 
    if c_id_flag == 0:
       error_raise.invalid_member()
    
    # add message into message string in database
    index = active
    handle = find_handle_from_token(token)
    message_string = f"{handle}: {message}/n"
    standupDatabase[index]['message'].append(message_string)

    pickle_users(userDatabase)
    pickle_channels(channelDatabase)
    pickle_message(messageDatabase)

    return {}
