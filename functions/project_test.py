import re
import sys
import pytest
from auth import *
from user import *
from channel import *
from message import *
###set up####
registerResponse1 = auth_register('123@gmail.com','password','andrew','John')
token1 = registerResponse1['token']
registerResponse2 = auth_register('maggie@gmail.com','password','maggie','John')
token2 = registerResponse2['token']
registerResponse3 = auth_register('matt@gmail.com','password','matt','John')
token3 = registerResponse3['token']
registerResponse4 = auth_register('emma@gmail.com','password','emma','John')
token4 = registerResponse4['token']
channels_create(token2, "maggie", False)
channels_create(token3, "matt", False)
message_id1 = message_send(token2, 100000, 'hello')
message_id2 = message_send(token2, 100000, ' ')

#everytime we auth_registered,we append, so dont need to register again
def test_auth_register_existed_email():
    with pytest.raises(ValueError,match=r'Email has been registered'):
        auth_register('123@gmail.com','password','andrew','John')

def test_auth_register_invalid_email_format():
    with pytest.raises(ValueError,match=r'email is not valid'):
        auth_register('123.com','password','andrew','John')

def test_auth_register_short_password():
    with pytest.raises(ValueError,match=r'invalid password'):
        auth_register('123@gmail.com','123','andrew','John')

def test_auth_register_long_firstname():
    with pytest.raises(ValueError,match=r'invalid first name'):
        auth_register('123@gmail.com','1234567','a'*100,'John')

def test_auth_register_long_lastname():
    with pytest.raises(ValueError,match=r'invalid last name'):
        auth_register('123@gmail.com','1234567','andrew','a'*100)

def test_auth_register_sucessful():
    assert(auth_register('silvia@gmail.com','password','maggie','John')) == {'u_id': 5, 'token': jwt.encode({'email': 'silvia@gmail.com'}, 'comp1531', algorithm='HS256').decode('utf-8')}

  
#############################################

def test_auth_login_invalid_email_format():
    with pytest.raises(ValueError,match = r'email is not valid'):
        auth_login('123.com','12345')

def test_auth_login_invalid_email():
    with pytest.raises(ValueError,match = r'Email is not registered'):
        auth_login('aabbc@gmail.com','1234')

def test_auth_login_wrong_password():
    with pytest.raises(ValueError,match = r'Invalid password'):
        auth_login('123@gmail.com','1234567')

def test_auth_login_sucessful():
    assert(auth_login('123@gmail.com','password')) == {'u_id': 1, 'token': jwt.encode({'email': '123@gmail.com'}, 'comp1531', algorithm='HS256').decode('utf-8')}
    assert(auth_login('matt@gmail.com','password')) == {'u_id': 3, 'token': jwt.encode({'email': 'matt@gmail.com'}, 'comp1531', algorithm='HS256').decode('utf-8')}
    assert(auth_login('emma@gmail.com','password')) == {'u_id': 4, 'token': jwt.encode({'email': 'emma@gmail.com'}, 'comp1531', algorithm='HS256').decode('utf-8')}

#############################################

def test_logout_sucess():
    assert(auth_logout(token1))
    assert(auth_logout(token2))


#test permission:
def test_permission_invalid_uid():
    with pytest.raises(ValueError,match = r'invalid u_id'):
        permission_change(token1,8,3)

def test_permission_invalid_permissionid():
    with pytest.raises(ValueError,match = r'invalid permission'):
        permission_change(token1,1,4)

def test_permission_not_auth():
    with pytest.raises(AccessError,match = r'not autho'):
        permission_change(token2,3,3)
        
#####################################pytest-for-channel##################################
#test channel create
def test_create_invalid_name(): 
 with pytest.raises(ValueError,match=r'Invalid channel name'):
  channels_create('token1','g'*21,False)

#test channel invite
def test_channel_invite_invalid_channel():
 with pytest.raises(AccessError,match=r'Already member'):
  channels_invite(token2,100000,2)
   
def test_channel_invite_invalid_u_id():
 with pytest.raises(ValueError,match=r'Not exist user'):
  channels_invite(token2,100000,1000)    #1000 is not in the dictionary 
  
#test channel_leave
def test_channel_leave_nonexistent_channel():
 with pytest.raises(ValueError,match=r'Channel does not exist'):
  channels_leave(token2,5) 

#test channel_join
def test_channel_join_not_exist():
 with pytest.raises(ValueError,match=r'Channel does not exist'):
  channels_join(token1,500)
  
def test_channel_join_unauth():
 with pytest.raises(AccessError,match=r'This channel is private'):
  channels_join(token3,100000)
   

#test channel_addowner
def test_channel_addowner_nonexistent_channel():
 with pytest.raises(ValueError,match=r'Invalid channel_id'):
  channels_addowner(token2,500,1)
  
def test_channel_addowner_already_owner():
 with pytest.raises(AccessError, match=r"Already owner"):
  channels_addowner(token2, 100000, 2) 

def test_channel_addowner_unauthorized():
 with pytest.raises(AccessError, match=r"Unauthorize to add"):
  channels_addowner(token3, 100000, 4)

#test remove owner
def test_channel_removeowner_not_exist():
 with pytest.raises(ValueError,match=r'Channel does not exist'):
  channels_removeowner(token2,500,2)

def test_channel_removeowner_not_userofchannel():
 with pytest.raises(AccessError, match=r"Not Owner"):
  channels_removeowner(token2, 100000, 4) 
                                              
def test_channel_removeowner_unauthorized():
 with pytest.raises(AccessError, match=r"Not authorized"):
  channels_removeowner(token4, 100000, 2) 

#test list
def channel_list_sucess():
  assert(channel_list(token2) ==  
  {
   'channel_id': 100000,
   'name':'maggie'
   }
   )
#test channel_detail
def test_invalid_channel():
 with pytest.raises(ValueError,match=r'Channel does not exist'):
  channels_detail(token2,5)
 
def test_user_notin_channel():
 with pytest.raises(AccessError,match=r'User not in channel'):  
  channels_detail(token2,100001)
'''
#test channel_message
def test_channel_message_nonexistent_channel():
 with pytest.raises(ValueError,match=r'Channel does not exist'):
  channels_message(token1,5000,2)

def test_channel_message_excessive():
 with pytest.raises(ValueError,match=r'Excessive start'):
  channels_message(token2,100000,51)

def test_channel_message_unauth():
 with pytest.raises(AccessError,match=r'User not in channel'):
  channels_message(token4,100000,1)


############Tests for message_send#######################################
#########################################################################
    
def test_message_send_1_validmessage(): 
    assert message_id1 == 100001

def test_message_send_2_longmessage():
    with pytest.raises(ValueError,match=r'.*'):
        message_send(token2,'100000', "1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxc\vbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm")

def test_message_send_1_emptymessage():
    assert message_id2 == 100002

def test_message_send_usernotinchannel():
    with pytest.raises(AccessError,match=r'*'):
        message_send(token2,'100000'," ")
        

###########test for react ##############################################
########################################################################

#test for react to message
def test_message_react_1_invalidmessage(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(token2, 'not valid', '1')

def test_message_react_1_invalidreact(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(token2, 'message_id', 'not exist')

def test_message_react_successfulreact(): 
        assert message_react(token1, message_id1 , 1) == None

def test_message_react_usernotinchannel(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(token1, message_id1 , 1)

def test_message_react_1_reacted(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(token2, message_id1 , 1)


'''



###########################################################################
############################# user_profile ################################

# test when user id is not valid
def test_user_profile_nonexist1():
    with pytest.raises(ValueError, match = r"User doess not exist"):
        user_profile(token1, 10000)

def test_user_profile_nonexist2():
    with pytest.raises(ValueError, match = r"User doess not exist"):
        user_profile(token2, 10000)

def test_user_profile_nonexist3():
    with pytest.raises(ValueError, match = r"User doess not exist"):
        user_profile(token3, 10000)

# test successful cases
def test_user_profile():
    u_id1 = registerResponse1['u_id']
    u_id2 = registerResponse2['u_id']
    assert user_profile(token1, u_id1) == { 
        'email': '123@gmail.com', 
        'name_first': 'andrew',
        'name_last': 'John', 
        'handle_str': 'andrewJohn'
    }
    assert user_profile(token2, u_id2) == { 
        'email': 'maggie@gmail.com', 
        'name_first': 'maggie',
        'name_last': 'John', 
        'handle_str': 'maggieJohn'
    } 

###########################################################################
########################## user_profile_setname ###########################

# test when first name is more than 50 characters
def test_user_profile_setname_longfirst1():
    with pytest.raises(ValueError, match = r"Invalid first name"):
        user_profile_setname(token1, 'a'*100, 'a')

def test_user_profile_setname_longfirst2():
    with pytest.raises(ValueError, match = r"Invalid first name"):
        user_profile_setname(token2, 'a'*100, 'b')

def test_user_profile_setname_longfirst3():
    with pytest.raises(ValueError, match = r"Invalid first name"):
        user_profile_setname(token3, 'a'*100, 'c')

# test when last name is more than 50 characters
def test_user_profile_setname_longlast1():
    with pytest.raises(ValueError, match = r"Invalid last name"):
        user_profile_setname(token1, 'a', 'a'*100)

def test_user_profile_setname_longlast2():
    with pytest.raises(ValueError, match = r"Invalid last name"):
        user_profile_setname(token2, 'b', 'a'*100)

def test_user_profile_setname_longlast3():
    with pytest.raises(ValueError, match = r"Invalid last name"):
        user_profile_setname(token3, 'c', 'a'*100)

# test successful cases
def test_user_profile_setname():
    # change both 
    assert user_profile_setname(token1, 'ella', 'brown') == {}
    # no change 
    assert user_profile_setname(token2, 'maggie', 'floyd') == {}
    # change firstname
    assert user_profile_setname(token3, 'silvia', 'lastname') == {}

###########################################################################
########################## user_profile_setemail ##########################

# test when email is not valid
def test_user_profile_setemail_invalid1():
    with pytest.raises(ValueError, match = r"Email is not valid"):
        user_profile_setemail(token1, 'email')

def test_user_profile_setemail_invalid2():
    with pytest.raises(ValueError, match = r"Email is not valid"):
        user_profile_setemail(token2, 'email')

def test_user_profile_setemail_invalid3():
    with pytest.raises(ValueError, match = r"Email is not valid"):
        user_profile_setemail(token3, 'email')

# test when email is already being used by another user
def test_user_profile_setemail_used1():
    with pytest.raises(ValueError, match = r"Email has been registered"):
        user_profile_setemail(token1, 'emma@gmail.com')

def test_user_profile_setemail_used2():
    with pytest.raises(ValueError, match = r"Email has been registered"):
        user_profile_setemail(token2, 'emma@gmail.com')

def test_user_profile_setemail_used3():
    with pytest.raises(ValueError, match = r"Email has been registered"):
        user_profile_setemail(token3, 'emma@gmail.com')

# test successful cases
def test_user_profile_setemail():
    assert user_profile_setemail(token1, '321@gmail.com') == {}
    


###########################################################################
########################## user_profile_sethandle #########################

# test when handle is more than 20 characters
def test_user_profile_sethandle_long1():
    with pytest.raises(ValueError, match = r"Handle must be between 3 and 50 characters"):
        user_profile_sethandle(token1, 'i'*100)

def test_user_profile_sethandle_long2():
    with pytest.raises(ValueError, match = r"Handle must be between 3 and 50 characters"):
        user_profile_sethandle(token2, 'u'*100)

def test_user_profile_sethandle_long3():
    with pytest.raises(ValueError, match = r"Handle must be between 3 and 50 characters"):
        user_profile_sethandle(token3, 'm'*100)

# test when handle is used by others
def test_user_prifile_sethandle_used1():
    with pytest.raises(ValueError, match = r"Handle is used by another user"):
        user_profile_sethandle(token1, 'emmaJohn')
    
def test_user_prifile_sethandle_used2():
    with pytest.raises(ValueError, match = r"Handle is used by another user"):
        user_profile_sethandle(token2, 'emmaJohn')
    
def test_user_prifile_sethandle_used3():
    with pytest.raises(ValueError, match = r"Handle is used by another user"):
        user_profile_sethandle(token3, 'emmaJohn')
    
# test successful cases
def test_user_profile_sethandle():
    assert user_profile_sethandle(token1, 'hahahaha') == {}
    assert user_profile_sethandle(token2, 'uuuuuu') == {}
    assert user_profile_sethandle(token3, 'boring') == {}
