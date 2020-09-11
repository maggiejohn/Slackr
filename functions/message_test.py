import pytest
#update
from message import *
from auth import *

uid_token1 = auth_register("silvia@gmail.com", "silvia123", "silvia", "awesome")
uid_token2 = auth_register("matt@gmail.com", "matt123", "matt", "johnson")
channel_id = channels_create(uid_token1['token'], "channel1", "True")
uid_token3 = auth_register("maggir@gmail.com", "matt123", "matt", "johnson")
message_id1 = message_send(uid_token1['token'], "100000", "This is my message")
message_id2 = message_send(uid_token1['token'],'100000', " ")


##############SETUP#############
############Tests for message_send##############
################################################
def test_message_send_1_validmessage(): 
    assert message_id1 == 101018

def test_message_send_2_longmessage():
    with pytest.raises(ValueError,match=r'.*'):
        message_send(uid_token1['token'],'100000', "1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxc\vbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm")

def test_message_send_1_emptymessage():
    assert message_id2 == 101001

def test_message_send_usernotinchannel():
    with pytest.raises(AccessError,match=r'*'):
        message_send(uid_token2['token'],'100000'," ")



########################################
'''
#Tests for send_messagelater: 
def test_send_messagelater_1_doesnotexist(): 
    with pytest.raises(AccessError,match=r'*'):
        message_sendlater('Token1', '-1', "Message is cool", '10:00:00')

def test_send_messagelater_2_longmessage():
    with pytest.raises(ValueError,match=r'*'):
            message_sendlater('Token1','1', "1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm1234567890qdfsghfdswertyuiopasdfghjklzxcvbnm1234567890qwertyuioasdfghjklzxcvbnm1234567890asdfghjklzxcvbnm", "10:00:00")

     
'''

###########test for message remove##############
################################################
'''
def test_message_remove_1_doesNotExist(): 
    registerResponse1=auth_register("validemail@gmail.com", "12331214356", "name", "lastname")
    token1 = registerResponse1['token']
    with pytest.raises(ValueError, match=r'*'):
        message_remove(token1, 'doesNotExist')

def test_message_remove_1_notintoken(): 
    registerResponse1=auth_register("validemail@gmail.com", "12331214356", "name", "lastname")
    registerResponse2=auth_register("validemail1@gmail.com", "12331214356", "name", "lastname")
    token1 = registerResponse1['token']
    token2 = registerResponse2['token']
    channel1 = channels_create(token1, "channel1", "True")
    message_id = message_send(token1, channel1 , "This is my message")
    with pytest.raises(AccessError, match=r'*'):
        message_remove(token2, message_id)

'''
###########test for message edit################
################################################

def test_message_edit_1_notauthorised():
    with pytest.raises(AccessError, match=r'.*'):
        message_edit(uid_token2['token'], message_id1, "new message")

def test_message_edit_2_notauthorised():
    with pytest.raises(AccessError, match=r'*'):
        message_edit(uid_token3['token'], message_id1, "new message added")

def test_message_invalidMessageID():
    with pytest.raises(ValueError, match=r'*'):
        message_edit(uid_token3['token'], '123', "new message added")

###########test for react ######################
################################################

#test for react to message
def test_message_react_1_invalidmessage(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(uid_token2['token'], 'not valid', '1')

def test_message_react_1_invalidreact(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(uid_token2['token'], 'message_id', 'not exist')

def test_message_react_successfulreact(): 
        assert message_react(uid_token1['token'], message_id1 , 1) == None

def test_message_react_usernotinchannel(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(uid_token3['token'], message_id1 , 1)

def test_message_react_1_reacted(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(uid_token1['token'], message_id1  , 1)

#############test for unreact ##################
################################################

#test for react to message
def test_message_unreact_1_invalidmessage(): 
    with pytest.raises(ValueError, match=r'*'):
        message_unreact(uid_token2['token'], 'not valid', '0')

def test_message_unreact_1_invalidreact(): 
    with pytest.raises(ValueError, match=r'*'):
        message_unreact(uid_token2['token'], 'message_id', 'not exist')

def test_message_unreact_successfulreact(): 
        assert message_unreact(uid_token1['token'], message_id1 , 0) == None

def test_message_unreact_usernotinchannel(): 
    with pytest.raises(ValueError, match=r'*'):
        message_react(uid_token3['token'], message_id1 , 0)

def test_message_unreact_1_unreacted(): 
    with pytest.raises(ValueError, match=r'*'):
        message_unreact(uid_token1['token'], message_id1, 0)

###############test for ##pin ##################
################################################

def test_message_pin_1_notadmin():
    with pytest.raises(AccessError, match=r".*"):
        message_pin(uid_token2['token'], message_id2)

def test_message_pin_2_invalidmessage(): 
    with pytest.raises(ValueError, match=r".*"):
        message_pin(uid_token1['token'], 'not valid')

def test_message_pin_success(): 
    assert message_pin(uid_token1['token'], message_id1) == None

def test_message_pin_alreadypinned(): 
    with pytest.raises(ValueError, match=r".*"):
        message_pin(uid_token1['token'], message_id1)

def test_message_pin_4_notmember():
    with pytest.raises(ValueError, match=r".*"):
        message_pin(uid_token2['token'],message_id1)

###############test for unpin ##################
################################################

def test_message_unpin_2_invalidmessage(): 
    with pytest.raises(ValueError, match=r".*"):
        message_unpin(uid_token1['token'], 'not valid')

def test_message_unpin_success(): 
    assert message_unpin(uid_token1['token'], message_id1) == None

def test_message_unpin_1_notadmin():
    with pytest.raises(ValueError, match=r".*"):
        message_unpin(uid_token2['token'], message_id2)

def test_message_unpin_alreadypinned(): 
    with pytest.raises(ValueError, match=r".*"):
        message_unpin(uid_token1['token'], message_id1)

def test_standup_send_4_time_stopped():
    finish = standup_start('token', 'channel_id')
    # assume there is a fucntion changing token in standup_start
    # then the token conveys a time that is greater than finish time
    # it will then be a parameter of send, indicating the standup time has stopped
    with pytest.raises(AccessError, match=r".*"):
        standup_send('token', 'channel_id', 'hi')

#########################################
#test for search

def test_search_1_simple():
    assert search('token', 'project')

def test_search_2_empty():
    assert search('token', '')

def test_search_3_space():
    assert search('token', '  ')

def test_search_4_number():
    assert search('token', '123')

def test_search_5_punct():
    assert search('token', '?')

