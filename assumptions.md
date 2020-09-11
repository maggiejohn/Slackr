Related function is put into {}

1. Conceptually u_id is fixed but token changes every time when a user login, we use token to encode details of the user. However, in iteration 1 we could not and don't need to write perfect stub functions returning different token (as there might be some functions called generate_token), so we assume the return value of token and u_id is fixed.
    {most functions}

2. The reset code should be dynamic, but we assume the reset code is fixed, and new password is not the same as old password. Also we need to check if email address is valid or not and if it is registered or not. (this is not in exception column of spec)
    {auth_passwordreset_reset}

3. Assume there are 2 function called channel_id_check(channel_id) and message_id_check(message_id) which returns true or false
   {message_sendlater & message_remove}

4. Assume react_id 0 = empty
   {message_react}

5. Assume channel id -1 is invalid
   {message.py, message_test.py}

6. Token decides a user's permission in a channel; permission id decides a user's permission in slackr

7. Assume that in token 0 represents owner og the channel; 1 represents member of channel

8. Assume we have helper function permission_id_check(u_id) returns the integer permission id of a user

9. Assume there is a fucntion changing token in standup_start, then the token conveys a time that is greater than finish time, it will then be a parameter of standup_send, indicating the standup time has stopped
   {standup_send test}

##############
10.Admin can be changed to slakr owner or member; owner can be changed to slakr admin or member; member can be changed to slakr admin or owner. There is at least one onwer of slakr.
11.There can be two same handles when register, but not when reset handle
the length of handle can be less than 3 or greater than 20 when register since it's a concatenation of firstname and lastname. But when a user reset handle, the length of handle can not be less than 3 or greater then 20
12.When register with a valid email format and it is not in the database, this email is actually existing and working, so that when requesting a password reset code, the email will receive the reset code
13.No two distinct user receive the same password reset code at the same time
14.There are no numbers in firstname or lastname
15.When reset password, it can be the same as previous one
16.When a channel is created, it is not automatically added in the database of slakr owner and admin
17.For channel list, the owner and admin can only see a list of channels that they joined
18.A channel can still exist if everyone leaves the channel