import pytest
import re
import os
import jwt
import json
import hashlib
from collections import *
import error_raise 
import auth
import helper
import message
import pickle


def pickle_users(userDatabase):
    with open('User_database.pkl','wb') as f:
        pickle.dump(userDatabase,f)

def pickle_channels(channelDatabase):
    with open('Channel_database.pkl','wb') as f:
        pickle.dump(channelDatabase,f)
        
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

#Create channel ID
def create_channelID(): 
  #return len(channelDatabase) + 100000
  if os.path.exists('Channel_database.pkl') is True:
      d = Load('Channel_database.pkl')
      return len(d) + 100000
  else:
      return 100001

#Create a channel
def channels_create(token, name, is_public): 
  #pickle load
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  # check if channel is existed
  helper.check_channel_name(name)
     
  # check invalid channel_name
  helper.check_invalid_channelname(name)

  for i in range(len(userDatabase)):
    if userDatabase[i]['token'] == token:
      channel_Id = create_channelID()
      channelDatabase.append({
        'channelId' : channel_Id,
        'channelName': name,
        'is_public': is_public,
        'owner_members':[{'u_id':userDatabase[i]['u_id'], 'name_first':userDatabase[i]['name_first'],'name_last': userDatabase[i]['name_last'],'profile_img_url':userDatabase[i]['profile_img_url']}],
        'all_members': [{'u_id':userDatabase[i]['u_id'], 'name_first':userDatabase[i]['name_first'],'name_last': userDatabase[i]['name_last'],'profile_img_url':userDatabase[i]['profile_img_url']}],
        'messagelist':[]
      })
      userDatabase[i]['channel'].append(channel_Id)
      
      #rewrite the new userdatabase and channeldatabase to pkl file
      pickle_channels(channelDatabase)
      pickle_users(userDatabase)

  return {
    'channelId': channel_Id
  } 


def channels_invite(token, channel_id, u_id):
  #pickle load
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')

  #check if the user we wanto invite is registered/existed
  helper.check_user_existed(u_id)
    
  #check if the user we wanto invite is already a member of the channel  
  helper.check_already_member(channel_id,u_id)

  
  for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == int(channel_id):
      for j in range(len(userDatabase)):
        if userDatabase[j]['u_id'] == int(u_id):
          channelDatabase[i]['all_members'].append({
            'u_id' : int(u_id), 'name_first' :userDatabase[j]['name_first'], 'name_last' :userDatabase[j]['name_last'],'profile_img_url':userDatabase[j]['profile_img_url']
          })
          userDatabase[j]['channel'].append(int(channel_id))
          
          #pickle part start
          pickle_channels(channelDatabase)
          #rewrite the new userdatabase to pkl file
          pickle_users(userDatabase)




#Given a channel_id of a channel that the authorised user can join, adds them to that channel
def channel_join(token, channel_id):
  #pickle 
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  
  #check the channel we wanto leave is valid/existed
  helper.check_channel_id(channel_id)

  #check when the channel is private and i am not 
  helper.check_not_autho_join(token,channel_id)
  
  #find the u_id
  u_id = helper.find_id_from_token(token)
  
  
  for i in range(len(channelDatabase)):
     if channelDatabase[i]['channelId'] == int(channel_id):
       for j in range(len(userDatabase)):
         if userDatabase[j]['u_id'] == u_id:
          channelDatabase[i]['all_members'].append({
          'u_id':u_id, 
          'name_first':userDatabase[j]['name_first'],
          'name_last': userDatabase[j]['name_last'],
          'profile_img_url':userDatabase[j]['profile_img_url']
          })
          userDatabase[j]['channel'].append(int(channel_id))
          #rewrite the new userdatabase and channeldatabase to pkl file
          pickle_channels(channelDatabase)
          pickle_users(userDatabase)


#Given a channel ID, the user removed as a member of this channel
def channels_leave(token,channel_id):
  #pickle load
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')

  #check the channel we wanto leave is valid/existed
  helper.check_channel_id(channel_id)
  
  
  #check if we are not in the channel we wanto leave
  helper.check_authorized_user(token,channel_id)

  #remove data
  for i in range(len(userDatabase)):
    if token == userDatabase[i]['token']:
      value = i
      userDatabase[i]['channel'].remove(int(channel_id))
   
  for j in range(len(channelDatabase)):
    if int(channel_id) == channelDatabase[j]['channelId']:
      channelDatabase[j]['all_members'].remove({
        'u_id':userDatabase[value]['u_id'], 
        'name_first':userDatabase[value]['name_first'],
        'name_last': userDatabase[value]['name_last'],
        'profile_img_url':userDatabase[value]['profile_img_url']
        })
      #rewrite the new userdatabase and channeldatabase to pkl file
      pickle_channels(channelDatabase)    
      pickle_users(userDatabase)
      

#Make user with user id u_id an owner of this channel
def channels_addowner(token, channel_id, u_id):
  #pickle load
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')

  #check the channel we wanto add a owner is valid/existed
  helper.check_channel_id(channel_id)
    
  #check the user we want him to be the owner is already an owner
  helper.check_already_owner(channel_id,u_id)
 
  #check if i am not an admin or owner
  helper.check_not_autho_add(token,channel_id)
  
  #find the user
  for k in range(len(userDatabase)): 
    if userDatabase[k]['u_id'] == int(u_id):
     for i in range(len(channelDatabase)):
       if channelDatabase[i]['channelId'] == int(channel_id):
        channelDatabase[i]['owner_members'].append({
          'u_id':int(u_id), 
          'name_first':userDatabase[k]['name_first'],
          'name_last': userDatabase[k]['name_last'],
          'profile_img_url':userDatabase[k]['profile_img_url']
          })
        #rewrite the new userdatabase to pkl file
        pickle_channels(channelDatabase)

        



#Remove user with user id u_id an owner of this channel 
def channels_removeowner(token, channel_id, u_id):
  #pickle load
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')

  
  #check the channel we wanto remove an owner is valid/existed
  helper.check_channel_id(channel_id)

  #check the user we wanto remove its owner is not an owner
  helper.check_not_owner(channel_id,u_id)
  
  #check if i am not an admin or owner
  helper.check_not_autho_add(token,channel_id) 
  

  #find the user and rewrite userdatabase
  for k in range(len(userDatabase)): 
    if userDatabase[k]['u_id'] == int(u_id):
     for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id): 
        channelDatabase[i]['owner_members'].remove({
          'u_id':int(u_id),
          'name_first':userDatabase[k]['name_first'],
          'name_last': userDatabase[k]['name_last'],
          'profile_img_url':userDatabase[k]['profile_img_url']
         })
         #rewrite channeldatabase
        pickle_channels(channelDatabase)
         

#Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel
def channel_detail(token,channel_id):
#Channel ID is not a valid channel
#Authorised user is not a member of channel with channel_id

  #pickle start
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  #pickle done
  flag = 0
  for i in range(len(channelDatabase)):
   if channelDatabase[i]['channelId'] == int(channel_id):
    flag = 1
    k = i
    for j in range(len(userDatabase)):
      if userDatabase[j]['token'] == token:
        if not any(d['u_id'] == userDatabase[j]['u_id'] for d in channelDatabase[i]['all_members']):   
          error_raise.invalid_member()
  if flag == 0:
   error_raise.invalid_channelid()
  else:
   return {
    'name': channelDatabase[k]['channelName'],
    'owner_members':channelDatabase[k]['owner_members'],
    'all_members':channelDatabase[k]['all_members']
   }




#Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
def channel_message(token,channel_id,start):
#Channel ID is not a valid channel
#start is greater than the total number of messages in the channel
#Authorised user is not a member of channel with channel_id
  #pickle start
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  messageDatabase = Load('Message_database.pkl')
  #pickle done
  messagelist = []
  count = 0
  flag = 0
  
  #for i in range(len(channelDatabase)):
  if any(d['channelId'] == int(channel_id) for d in channelDatabase):
    flag = 1
    index_channel= next((index for (index, d) in enumerate(channelDatabase) if d["channelId"] == int(channel_id)), None)
    print(index_channel)

  for j in range(len(userDatabase)):
    if userDatabase[j]['token'] == token:
      if not any(d['u_id'] == userDatabase[j]['u_id'] for d in channelDatabase[index_channel]['all_members']):
        error_raise.invalid_authorized()   
  
  if flag == 0:
    error_raise.invalid_channelid()
  if int(start) > len(messagelist):
    error_raise.invalid_start

  for index in range(len(channelDatabase[index_channel]['messagelist'])): 
    if index >= int(start) and count <= 50:
      for count in range(len(messageDatabase)): 
        print(count)
        print ("\n")
        if messageDatabase[count]['message_id'] == channelDatabase[index_channel]['messagelist'][index]:
          messagelist.append({ 
            'message_id': messageDatabase[count]['message_id'], 
            'u_id': messageDatabase[count]['u_id'], 
            'message': messageDatabase[count]['message'],
            'time_created': messageDatabase[count]['time'], 
            'reacts':  messageDatabase[count]['react_id'], 
            'is_pinned':messageDatabase[count]['is_pinned']
            })
          continue

  end = int(start) + count
  return {
   'messages': messagelist,
   'start':start,
   'end': end
  }

def channel_list(token):
  #pickle start
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  #pickle done
  c_list = []
  for i in range(len(userDatabase)):
    if userDatabase[i]['token']==token:
      for n in range(len(channelDatabase)):
        if channelDatabase[n]['channelId'] in userDatabase[i]['channel']:
          c_list.append({
            'channel_id': channelDatabase[n]['channelId'],
            'name': channelDatabase[n]['channelName']
          })

  return {
    'channels': c_list
    }

def channel_listall(token):
  #pickle start
  channelDatabase = Load('Channel_database.pkl')
  userDatabase = Load('User_database.pkl')
  #pickle done
  all_list = []
  for n in range(len(channelDatabase)):
    all_list.append({
      'channel_id': channelDatabase[n]['channelId'],
      'name': channelDatabase[n]['channelName']
    })
  return {
    'channels': all_list
    }

