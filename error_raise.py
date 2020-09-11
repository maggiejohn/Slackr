import jwt
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from json import dumps

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.register_error_handler(Exception, defaultHandler)
CORS(app)

class ValueError(HTTPException):
    code = 400
    message = 'No message specified'

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'


# Post
@app.route('/invalidemail')
def invalid_email():
    raise ValueError("email is not valid")

@app.route('/existedemail')
def existed_email():
    raise ValueError("Email has been registered")

@app.route('/invalidpassword')
def invalid_password():
    raise ValueError("invalid password")
    
@app.route('/invalidfirstname')
def invalid_first_name():
    raise ValueError("invalid first name")

@app.route('/invalidlastname')
def invalid_last_name():
    raise ValueError("invalid last name")
  
@app.route('/notregisteredemail')
def not_registered_email():
    raise ValueError("Email not registered")

@app.route('/incorrectpassword')
def incorrect_password():
    raise ValueError("password is incorrect")

@app.route('/invalidrestcode')
def invalid_reset_code():
    raise ValueError("reset_code is invalid") 

@app.route('/channelnameexist')
def channelname_exist():
    raise ValueError("channel name is existed")

@app.route('/invalidchannelname')
def invalid_channelname():
    raise ValueError("channel name is invalid")


@app.route('/notauthorized')
def invalid_authorized():
    raise ValueError("user is not authorized")

@app.route('/notmember')
def invalid_member():
    raise AccessError("u_id is not in this channel")

@app.route('/nonexistence_user')
def invalid_user():
    raise ValueError("user does not exist")

@app.route('/notauthorizedtoaction')
def unable_to_operate():
    raise AccessError("Not authorized")

@app.route('/alreadyowner')
def already_owner():
    raise AccessError("Already Owner")

@app.route('/alreadyowner')
def already_member():
    raise AccessError("Already member")

@app.route('/notowner')
def not_owner():
    raise AccessError("Not Owner")

@app.route('/nomessage')
def invalid_messageid():
    raise ValueError("Message no longer exists")

@app.route('/messagetoolong')
def message_too_long():
    raise ValueError("Message is too long")

@app.route('/user_not_in_channel')
def user_not_in_channel():
    raise AccessError("User not in channel")

@app.route('/timeinpast')
def time_is_in_past(): 
    raise ValueError("Time is in path")
    
@app.route('/invalidmessage')
def message_invalid():
    raise ValueError("User not in channel")

@app.route('/invalidmessageid')
def invalid_messageID():
    raise ValueError("Invalid Message ID")

@app.route('/invalidreactid')
def invalid_reactID():
    raise ValueError("react_id is not valid")

@app.route('/alreadyreacted')
def already_reacted(): 
    raise ValueError("Message already reacted")

@app.route('/alreadyunreacted')
def already_unreacted(): 
    raise ValueError("Message already unreacted")

@app.route('/alreadypinned')
def already_pinned(): 
    raise ValueError("Message already pinned")

@app.route('/alreadyunpinned')
def already_unpinned(): 
    raise ValueError("Message already unpinned")

@app.route('/notanadmin')
def not_an_admin(): 
    raise ValueError("User not an admin")


@app.route('/alreadyhadstandup')
def already_have_standup(): 
    raise ValueError("An active standup is currently running in this channel")

@app.route('/nostandup')
def have_no_standup(): 
    raise ValueError("No active standup is currently running in this channel")






@app.route('/invalidchannelid')
def invalid_channelid():
    raise ValueError("Channel ID is not a valid channel")
    
@app.route('/privatechannel')
def private_channel():
    raise AccessError("This channel is private")
    
@app.route('/invalidstart')
def invalid_start():
    raise ValueError("This start is oversized")

@app.route('/invalidhandle')
def invalid_handle():
    raise ValueError("Handle must be between 3 and 50 characters")

@app.route('/imageoutofdimension()')
def user_profile_image_out_of_dimension():
    raise ValueError("image is out of dimension")
    
@app.route('/wrongimagetype')
def user_profile_wrong_imagetype():
    raise ValueError("user profile is wrong_imagetype")
    
@app.route('/existedhandle')
def existed_handle():
    raise ValueError("Handle is used by another user")
if __name__ == '__main__':
    app.run(debug=True)