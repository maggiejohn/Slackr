'''
channel functions for pytest
'''
import re
import jwt
import json
import hashlib
from collections import *
from auth import *
from error import AccessError

channelDatabase = []
#########helper function begins######################
#Create channel ID
def create_channelID(): 
  return len(channelDatabase) + 100000

#given a token, find the user id
def find_id_from_token(token):
    for i in range(len(userDatabase)): 
        if userDatabase[i]['token'] == token:
            u_id = userDatabase[i]['u_id']
            return u_id      
      
#check if the channel to create has invalid name(>20)     
def check_invalid_channelname(name):
    if len(name) > 20: 
     raise ValueError('Invalid channel name')
    
#check if the user is registered/existed
def check_user_existed(u_id):
    if not any(d['u_id'] == int(u_id) for d in userDatabase):
      raise ValueError("user does not exist")
    
#check if a channel id is valid
def check_channel_id(channel_id):
    flag = 0
    for i in range(len(channelDatabase)):
        if int(channel_id) == channelDatabase[i]['channelId']:
            flag = 1
    if flag == 0:
        raise ValueError("Channel ID is not a valid channel") 
#check if the user we wanto add as owner is already an owner of the channel
def check_already_owner(channel_id,u_id):
   for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == int(channel_id):
      if any(d['u_id'] == u_id for d in channelDatabase[i]['owner_members']):
       raise AccessError("Already Owner")

# given a token, find the permission
def find_permission_from_token(token):
    for i in range(len(userDatabase)):
      if userDatabase[i]['token'] == token:
        permission = userDatabase[i]['permission']
        return permission
        
         
#check if the user we wanto invite is already a member of the channel  
def check_already_member(channel_id,u_id):
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id):
        if any(d['u_id'] == int(u_id) for d in channelDatabase[i]['all_members']): 
           raise AccessError("Already member")
          
#check if we are not in the channel we wanto leave
def check_authorized_user(token,channel_id):
    for i in range(len(channelDatabase)):
      if int(channel_id) == channelDatabase[i]['channelId']:
        u_id = find_id_from_token(token)
        if not any(d['u_id'] == u_id for d in channelDatabase[i]['all_members']):
          raise AccessError("u_id is not in this channel")    

#check when the channel is private and i am not
def check_not_autho_join(token,channel_id):
    permission = find_permission_from_token(token)         
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id) and channelDatabase[i]['is_public'] == False and (int(permission) != 1):
        raise AccessError("This channel is private")

#check heck if i am not an admin or owner of this channel so i cannot add others
def check_not_autho_add(token,channel_id):
    permission = find_permission_from_token(token) 
    u_id = find_id_from_token(token)      
    for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id):
        if (int(permission) != 1) and (not any(d['u_id'] == int(u_id) for d in channelDatabase[i]['owner_members'])):
         raise AccessError("Not authorized")  
         
#check the user we wanto remove its owner is not an owner
def check_not_owner(channel_id,u_id):
  for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == channel_id:
     if not any(d['u_id'] == int(u_id) for d in channelDatabase[i]['owner_members']):
      raise AccessError("Not Owner")  
########################helper funtion ends########################################
#Create a channel
def channels_create(token, name, is_public):     
  #check invalid channel_name
  check_invalid_channelname(name)

  for i in range(len(userDatabase)):
    if userDatabase[i]['token'] == token:
      channel_Id = create_channelID()
      channelDatabase.append({
        'channelId' : channel_Id,
        'channelName': name,
        'is_public': is_public,
        'owner_members':[{'u_id':userDatabase[i]['u_id'], 'name_first':userDatabase[i]['name_first'],'name_last': userDatabase[i]['name_last']}],
        'all_members': [{'u_id':userDatabase[i]['u_id'], 'name_first':userDatabase[i]['name_first'],'name_last': userDatabase[i]['name_last']}],
        'messagelist':[]
      })
      userDatabase[i]['channel'].append(channel_Id)
  return {
    'channelId': channel_Id
  } 

 
def channels_invite(token, channel_id, u_id):
  #check if the user we wanto invite is registered/existed
  check_user_existed(u_id)
    
  #check if the user we wanto invite is already a member of the channel  
  check_already_member(channel_id,u_id)

  
  for i in range(len(channelDatabase)):
    if channelDatabase[i]['channelId'] == int(channel_id):
      for j in range(len(userDatabase)):
        if userDatabase[j]['u_id'] == int(u_id):
          channelDatabase[i]['all_members'].append({
            'u_id' : int(u_id), 'name_first' :userDatabase[j]['name_first'], 'name_last' :userDatabase[j]['name_last']
          })
          userDatabase[j]['channel'].append(int(channel_id))


#Given a channel ID, the user removed as a member of this channel
def channels_leave(token,channel_id):

  #check the channel we wanto leave is valid/existed
  check_channel_id(channel_id)
   
  #check if we are not in the channel we wanto leave
  check_authorized_user(token,channel_id)

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
        'name_last': userDatabase[value]['name_last']
        })

def channels_join(token, channel_id):
  #check the channel we wanto leave is valid/existed
  check_channel_id(channel_id)

  #check when the channel is private and i am not 
  check_not_autho_join(token,channel_id)
  
  #find the u_id
  u_id = find_id_from_token(token)
  
  
  for i in range(len(channelDatabase)):
     if channelDatabase[i]['channelId'] == int(channel_id):
       for j in range(len(userDatabase)):
         if userDatabase[j]['u_id'] == u_id:
          channelDatabase[i]['all_members'].append({
          'u_id':u_id, 
          'name_first':userDatabase[j]['name_first'],
          'name_last': userDatabase[j]['name_last']
          })
          userDatabase[j]['channel'].append(int(channel_id))


          
#channel add_owner 
def channels_addowner(token, channel_id, u_id):
  #check the channel we wanto add a owner is valid/existed
  check_channel_id(channel_id)
    
  #check the user we want him to be the owner is already an owner
  check_already_owner(channel_id,u_id)
 
  #check if i am not an admin or owner
  check_not_autho_add(token,channel_id)
  
  #find the user
  for k in range(len(userDatabase)): 
    if userDatabase[k]['u_id'] == int(u_id):
     for i in range(len(channelDatabase)):
       if channelDatabase[i]['channelId'] == int(channel_id):
        channelDatabase[i]['owner_members'].append({
          'u_id':int(u_id), 
          'name_first':userDatabase[k]['name_first'],
          'name_last': userDatabase[k]['name_last']
          })



#channel remove owner
def channels_removeowner(token, channel_id, u_id):
  #check the channel we wanto remove an owner is valid/existed
  check_channel_id(channel_id)

  #check the user we wanto remove its owner is not an owner
  check_not_owner(channel_id,u_id)
  
  #check if i am not an admin or owner
  check_not_autho_add(token,channel_id) 
  

  #find the user and rewrite userdatabase
  for k in range(len(userDatabase)): 
    if userDatabase[k]['u_id'] == int(u_id):
     for i in range(len(channelDatabase)):
      if channelDatabase[i]['channelId'] == int(channel_id): 
        channelDatabase[i]['owner_members'].remove({
          'u_id':int(u_id),
          'name_first':userDatabase[k]['name_first'],
          'name_last': userDatabase[k]['name_last']
         })


def channels_detail(token,channel_id):
#Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel
#Channel ID is not a valid channel
#Authorised user is not a member of channel with channel_id
  flag = 0
  for i in range(len(channelDatabase)):
   if channelDatabase[i]['channelId'] == int(channel_id):
    flag = 1
    k = i
    for j in range(len(userDatabase)):
      if userDatabase[j]['token'] == token:
        if not any(d['u_id'] == userDatabase[j]['u_id'] for d in channelDatabase[i]['all_members']):   
          raise AccessError("u_id is not in this channel")
  if flag == 0:
   raise ValueError("Channel ID is not a valid channel")
  else:
   return {
    'name': channelDatabase[k]['channelName'],
    'owner_members':channelDatabase[k]['owner_members'],
    'all_members':channelDatabase[k]['all_members']
   }
'''
#channel_message
def channels_message(token,channel_id,start):
#Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
#Channel ID is not a valid channel
#start is greater than the total number of messages in the channel
#Authorised user is not a member of channel with channel_id
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
'''  
  
def channel_list(token):
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
  all_list = []
  for n in range(len(channelDatabase)):
    all_list.append({
      'channel_id': channelDatabase[n]['channelId'],
      'name': channelDatabase[n]['channelName']
    })
  return {
    'channels': all_list
    }

from message import *