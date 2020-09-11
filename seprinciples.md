1.First of all, we should find the Determining Design Smells: 
 - Needless Complexity: Functions in channel.py and message.py contained needless complexities using multiple nested loops to determine a value from a different database.To make it easier, we create helper functions 
 - Needless Repetition: Within iteration 2, in many of the functions there are a repetition of code doing the same functions therefore making the code quite long and difficult to edit if there is a change needed. 
 - Opacity: Due to the continuous use of indexing and multiple for loops within one function; it was quite difficult to understand the code without spending a significant amount of time. So we add comments. 
 - Fragility: Due to the previous design smells, it has made the code quite fragile and easily broken if an item was changed. Furthermore, it was difficult to debug due to the complexity of the code. 

   According to the smells, methods used and thing to be done to refactor code:
   - 1.1. Change all wildcard import like from xxx import * into import xxx: Although certain modules are designed to export only names that follow certain patterns when you use import *, it is still considered bad practice in production code.
   - 1.2. add helper functions to eliminate repeated work and make the functions simple and clean
   - 1.3. add comments: it is not always easy for not only us but also readers to understand and debug the code
   - 1.4. (to be done)Change all database(list of dictionary) into class.


2.Design Principles Used: 
- 2.1 The first principle we thought about is DRY (Do not repeat yourself)
  - Definition: Reducing duplicate code. 
  - How to achieve: By divide our system into pieces. Divide your code and logic into smaller reusable units and use that code by calling it where you want.
     We went through auth.py, channel.py and message.py, finding out there are lots of additional, repeated unnecessary code which increased the amount of work of building backends and maintain software. For the repeated code, we developed helper functions in helper.py to eliminate.
  - Example: when dealing with auth functions like auth_register and auth_login, in iteration2 to get the token of the user, we repeated the following code each time when we need token:
    Before:
     secret = 'comp1531'
     encoded_jwt = jwt.encode({'email': email}, secret, algorithm='HS256')
     'token': encoded_jwt.decode('utf-8')
   By applying DRY, we create a helper function called create_token(email) and calls helper.create_token to get the token.
    After:
     def create_token(email):
      encoded_jwt = jwt.encode({'email': email}, 'comp1531', algorithm='HS256')
      return encoded_jwt.decode('utf-8')
- 2.2 The second principle we thought about is KISS (Keep It Simple, Stupid)
  - Definition: To keep the code simple and clear, making it easy to understand. Compared with DRY, KISS focus more on methods of solving problems.
  - How to achieve: When dealing with each function, keep our methods small and each should be less than 50 lines. Each method should only solve one small problem, not many use cases. 
  - Advantages: Easier to read, maintain and debug.
  - Example 1.
    Before: In auth_register when raising errors, we use many if and elif clause which is messy:
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",str(email)):
      raise ValueError('Invalid email format')
    elif len(password) < 5:
      raise ValueError('Invalid password')
    elif len(name_first) > 50:
      raise ValueError('Invalid first name')
    elif len(name_last) > 50:
      raise ValueError('Invalid last name')
    After: By applying KISS, the easiest way to modify is to put if instead of elif.Cause the logic is if we have the erro raised, we jumped out of the function and there is no need to confused ourselves with so much else if. Conbinding DRY with KISS, considering that we need to check email format several times, we put it in helper functions and have the following:
        helper.check_email_format(email)
        helper.check_password(password)
        helper.check_firstname(name_first) 
        helper.check_lastname(name_last) 
  - Example 2.
   Before: when we add an owner of a channel, we want to check if the user we add_owner is already an owner and raise error, we use may if clauses under for loops even still under another for loops like this:
    for k in range(len(userDatabase)): 
        if userDatabase[k]['token'] == token: 
          if userDatabase[k]['permission'] != 1:   
              for i in range(len(channelDatabase)):
                if channelDatabase[i]['channelId'] == int(channel_id):
                  if userDatabase[k]['u_id'] not in channelDatabase[i]['owner_members']:
   After:By applying KISS, we simplify for loops by using’if any d[] for d in database’, which is much more easy and clear for both run and debug:
      for i in range(len(channelDatabase)):
        if channelDatabase[i]['channelId'] == channel_id:
         if not any(d['u_id'] == int(u_id) for d in channelDatabase[i]['owner_members']):
  - Example 3. 
    Before: When we wanted to find a dictionary which contained a message_id or message, we would use multiple for loops to find that dictionary. 
    After: We applied KISS to simplify the loop to determine the index within a list by using a helper function: 
        message_index = helper.get_index (messageDatabase,int(message_id), 'message_id')
- 2.3 Simple Responsibility Principle: 
    - Each helper function is responsible to do one thing; this is aligned with all the tasks in the auth.py, channel.py and message.py. The Single Responsibility Principle relies on DRY.
