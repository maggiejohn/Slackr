"""Flask server"""
import sys
import hashlib
import jwt
#import json
from random import randint
import flask
from json import dumps
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_mail import Mail, Message

import auth
import channel
from message import *
import user


#AUTH

APP = Flask(__name__,static_url_path = '/static/')
CORS(APP)


APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'smmm1531@gmail.com',
    MAIL_PASSWORD = "smmmsmmm"
)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def send_mail():
    mail = Mail(APP)
    email = request.form.get('email')
    dic = auth.auth_passwordreset_request(email)
    value = str(randint(0,100000))
    hash1 = hashlib.sha256(value.encode('utf-8')).hexdigest()
    for i in range(len(userDatabase)):
     if email == userDatabase[i]['email']:
      userDatabase[i]['hash'] = hash1 
    try:
        msg = Message("Send Mail Test!",
            sender="smmm1531@gmail.com",
            recipients=[dic])
        msg.body = value
        mail.send(msg)
        return dumps({})
    except Exception as e:
        return (str(e))
    
    
@APP.route('/auth/passwordreset/reset',methods = ['POST'])      
def password_reset():
 reset_code = request.form.get('reset_code')
 new_password = request.form.get('new_password')
 auth.auth_passwordreset_reset(reset_code, new_password)
 return dumps({})



@APP.route('/auth/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    dic = auth.auth_register(email, password, name_first, name_last)
    return dumps(dic)


@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    dic = auth.auth_login(email,password)
    return dumps(dic)

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    is_success = auth.auth_logout(token)
    return dumps(is_success)

@APP.route('/users/all', methods=['GET'])
def usersall():
    token = request.args.get('token')
    dic = auth.user_all(token)
    return dumps(dic)


#CHANNELS


@APP.route('/channel/invite', methods = ['POST'])
def channel_invite():
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    channel_id = request.form.get('channel_id')
    dic = channel.channels_invite(token, channel_id, u_id)
    return dumps(dic)



@APP.route('/channels/create', methods = ['POST'])
def create_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    dic = channel.channels_create(token, name, is_public)
    return dumps(dic)


@APP.route('/channel/details', methods=['GET'])
def detail_channel():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    dic = channel.channel_detail(token,channel_id)
    return dumps(dic)

@APP.route('/channel/messages', methods=['GET'])
def message_channel():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    dic = channel.channel_message(token,channel_id,start)
    return dumps(dic)


@APP.route('/channel/leave', methods = ['POST'])
def channel_leave():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    dic = channel.channels_leave(token,channel_id)
    return dumps(dic)

@APP.route('/channel/join', methods = ['POST'])
def join_channel():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    dic = channel.channel_join(token, channel_id)
    return dumps(dic)


@APP.route('/channel/addowner', methods = ['POST'])
def addowner():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    dic = channel.channels_addowner(token,channel_id,u_id)
    return dumps(dic)

@APP.route('/channel/removeowner', methods=['POST'])
def channel_remove():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    dic = channel.channels_removeowner(token,channel_id,u_id)
    return dumps(dic)

@APP.route('/channels/list', methods = ['GET'])
def channels_list():
    token = request.args.get('token')
    c_list = channel.channel_list(token)
    return dumps(c_list)

@APP.route('/channels/listall', methods = ['GET'])
def channels_listall():
    token = request.args.get('token')
    c_list = channel.channel_listall(token)
    return dumps(c_list)
#Message
@APP.route('/message/send', methods = ['POST'])
def send_message(): 
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')    
    message_id = message_send(token, channel_id, message)
    return dumps(message_id)

@APP.route('/message/sendlater', methods = ['POST'])
def send_messagelater(): 
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    time_sent = request.form.get('time_sent')    
    message_id = message_sendlater(token, channel_id, message, time_sent)
    return dumps(message_id)

@APP.route('/message/edit', methods = ['PUT'])
def edit_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message = request.form.get('message')
    message_edit(token, message_id, message)
    return dumps({})

@APP.route('/message/react', methods = ['POST'])
def react_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')
    message_react(token, message_id, react_id)
    return dumps({})

@APP.route('/message/unreact', methods = ['POST'])
def unreact_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')
    message_unreact(token, message_id, react_id)
    return dumps({})

@APP.route('/message/pin', methods = ['POST'])
def pin_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message_pin(token, message_id)
    return dumps({})

@APP.route('/message/unpin', methods = ['POST'])
def unpin_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message_unpin(token, message_id)
    return dumps({})

@APP.route('/message/remove', methods = ['DELETE'])
def remove_message(): 
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message_remove(token, message_id)
    return dumps({})

@APP.route('/message/search', methods = ['GET'])
def search_message(): 
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    message_dictionary = search(token,query_str)
    return json.dumps(message_dictionary)

    
@APP.route('/standup/active', methods = ['GET'])
def active_standup():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    dic = standup_active(token, channel_id)
    return dumps(dic)




# USERS
@APP.route('/user/profile', methods = ['GET'])
def profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    profile_info = user.user_profile(token, u_id)
    return dumps(profile_info)

@APP.route('/user/profile/setname', methods = ['PUT'])
def setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    user.user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route('/user/profile/setemail', methods = ['PUT'])
def setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    user.user_profile_setemail(token, email)
    return dumps({})

@APP.route('/user/profile/sethandle', methods = ['PUT'])
def sethandle():
    token = request.form.get('token')
    handle = request.form.get('handle_str')
    user.user_profile_sethandle(token, handle)
    return dumps({})

@APP.route('/user/profiles/uploadphoto', methods = ['POST'])
def uploadphoto():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')
    return dumps(user.user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end,request.url_root))
 
'''    
@APP.route('/admin/userpermission/change', methods = ['POST'])
def change_permission():
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')
    permission_change(token, u_id, permission_id)
    return dumps({})
'''
    
if __name__ == '__main__':
   APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))

