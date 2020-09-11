######################### iteration 1 ###########################

Meeting 1:
    time: 3-5pm Tue 01/10/19
    location: main library
    member: all of us

    Content:
        - splited the tasks for each person
        - user stories and tests are distributed equally amongst four of us 
        - each of us will write a *_test.py file that contains both stub functions and test functions
        - next meeting will be held on Thursday
        
    Work Distribution (Test Functions): 
        1-8: Silvia
        9-16: Minhui
        17-24: Zijing
        25-32: Yiwei

    Goal:
        - complete user stories and tests by Friday
        - expected to finish this iteration before Sunday, so that we can discuss on Sunday to fix other problems


******************************************************************

Meeting 2:
    time: 2-7pm Thus 03/10/19
    location: business school
    member: Yiwei, Zijing, Minhui

    Content:
        - reschedule the test functions
        - decide to split the functions into four files containing their stub functions: auth.py, channel.py, message.py, user.py
        - create other four files containing test functions: auth_test.py, channel_test.py, message_test.py, user_test.py
        - we complete all the auth_* functions tegether and started channel_* funcitnos
        - pair programing was implemented so that each person can take a turn and improve quality of code
        - contact Silvia online about the progress and adjustments
        - Silvia and Minhui will be in charge of all the user stories
        - next meeting will be held on Friday

    Work distribution:
        - auth.py completed and channel.py started by Yiwei, Zijing, Minhui
        - some of user stories completed by Silvia

    Goal:
        - finish most of the test functions on Friday

******************************************************************

Meeting 3:
    time: 2-6pm Fri 04/10/19
    location: main library
    member: Silvia, Zijing, Minhui

    Content: 
        - user stories finished by Silvia and Minhui
        - finished most of channel.py, message.py, user.py and their test files
        - changed the way to write stub functions (was too detailed and overdesigned in auth.py)
        

    Work Distribution: 
        - channel.py, channel_test.py (Zijing)
        - message.py, message_test.py (Silvia)
        - user.py, user_test.py (Minhui)


######################### iteration 2 ###########################

Since the content of iteration 2 is mostly inter-related and there are lots of issues that need to be discussed and clarified,
we strive to meet as often as we can, so that everyone keeps the same understanding and our file is up to date. 

Meetings in total: 5

Process:
    standup (raise problems, discuss how we can solve them)
->  make a task board (list all problems from high priority to low)
->  work pattern (i.e together, in pair, individually, depends on task board)
->  split works 
->  discussion when having problems
->  if we can not finish every task, divide into four parts for each of us to do at home

For individual work:
    When one person gets stuck, another person comes and checks together. If it's still not solved, we discuss about it together.

For pair work:
    When two person get stuck, everyone checks together. If it's still not solved, we leave it on the task board till someone think 
    of an idea or leave it till the end.



Meeting 1:

Content:
    - Figure out the priority of functions: auth -> user/channel -> message -> others
    - Make a task board (ordered by priority)
    - Auth functions need to be complete first since other functions will depend on them
    - Decide to do the auth parts together (get a feeling of flask server and everyone can do the rest with understanding towards 
    things related to auth i.e how token works)
    - Write functions for server first, then start pytest files

Work pattern:
    - Together 

Goal:
    - Complete all auth functions
    - Test on postman

What's left:
    - Test file for auth 
    - Assumptions 



Meeting 2:

Content:
    - Have standup and discuss about new issues 
    - Discuss about assumptions
    - Check each other's code 
    - Start on channel, figure out the priority 
    - Make a task board (ordered by priority)
    - Complete channel create&invite together (according to priority)
    - For other parts, split work and code in pairs
    - Add errors in error_raise.py for auth
    - Also add errors as we go through errors in channel

Work pattern:
    - Together and in pair 

Goal:
    - Complete all channel functions 
    - Add errors for auth and channel

What's left:
    - Channel_messages()
    - Test file for channel
    - Assumptions
    - Test channel functions on postman



Meeting 3:

Content:
    - Have standup and discuss about new issues 
    - Discuss about assumptions
    - Check each other's code 
    - Start on user and message functions, figure out the priority 
    - Make a task board (ordered by priority)
    - Add errors as we go
    - Split work and code independently

Work pattern:
    - Individually

Goal:
    - Complete all user and message functions
    - Add errors for user and message

What's left:
    - message_sendlater() & message_remove()
    - Test file for user and message
    
    

Meeting 4:

Content:
    - Have standup and discuss about new issues 
    - Check each other's code 
    - Make a task board (ordered by priority)
    - Finish the rest of what we left from last meeting
    - Split work and code independently
    - Write message sendlater, standup start&send, search and permission change
    - Test flask server 
    - Implement pytest for all files 
    
Work pattern:
    - Individually 

Goal:
    - Complete message sendlater
    - Complete standup start&send, search and permission change

What's left:
    - Pytest debug



Meeting 5:

Content:
    - Have standup and discuss about new issues 
    - Check each other's code 
    - Make a task board (ordered by priority) 
    - Solve small problems in code 
    - Write assurance file
    - Put our acceptance criterias into gitlab task board 
    - Merge everything on git 
    - Test flask server in the master branch 

Work pattern:
    - Individually, in pair and together

Goal:
    - Finish everything we can for the project
 
 
Reflection: 

What went well: 
    - Pair and group programming: caught onto bugs and issues early on
        E.g. messageDatabase structure: previously it was [{[{}]}], it was changed as it was too complex and took too much 
        function power to implement and iterate. 
    - Discussion: made sure that we were all on the same page. 
        E.g. When we discussed about assumptions, more issues were brought up therefore they can be considered making our project 
        more complete. 
    - Planning: all members met deadlines and we did not cause any delays in our set milestones. 
    

Issues: 
    - Starting our assignment too late: we could be more organised and start earlier to ensure that our work is 100%
    - Git Merge/Push/Pull: we did not know how to properly utilize git merge/push/pull therefore it overwritten our local repo 
    making our work disappear.


######################### iteration 3 ###########################

For this iteration, since we gained a deeper understanding about the project from iteration 2, we can separate some of the work for 
everyone to do independently at the beginning. Then we can have meetings to update progress and solve difficulties together.


Plan of iteration 3:
    - analyse new tasks
    - make a taskboard based on priority
    - split the high priority tasks equally
    - have meetings to solve problems (for meetings, we follow the process in iteration 2)
    - try our best :)


Task borad:
1. Adapt to changes in spec
    1.1 added functions: users/all, user/profiles/uploadphoto
	1.2 changes of functions: standup/start, message/edit
    1.3 incomplete functions from last iteration: message/remove, message/search, message/sendlater, standups 

2. Testing
    2.1 fix problems from last iteration
    2.2 add tests for new functions 

3. Analyse the system
    3.1 an er diagram modles the data layer

4. Demonstrate software engineering design understanding
    4.1 refactor our code 
        4.1.1 change database to pickle
        4.1.2 reduce overlapping code
        4.1.3 adding comments
        4.1.4 improve pytest
        4.1.5 further improvement of code quality 
    4.2 in the mean time reflect in seprinciples.md
    
5. Reflect on your use of agile practices and how you worked as a team
    5.1 as we develop the project, one person will write teamwork.md 

6. Integrate with front end
    6.1 test if backend works
    6.2 connect backend with front end 

Task based on priority:

    high:
        Task 1: Adapt to changes in spec 
        We need to finish this task for refactor, tests and frontend. And also because the workload is quite big, it is 
        important to start first, this task is splited among us.

    middle:
        Task 2: Testing 
        We can write tests while doing task 1 which also helps to debug.

        Task 4.1: Demonstrate software engineering design understanding 
        The focus is to simplify and optimize our code with the use of software engineering principles.
        We can do this task once a file is complete, helper functions is put in a new file called helper.py.

        Task 6: Integrate with front end
        In iteration 2, we did auth functions together, so we also connect this part to front end together.
        Then we integrate other parts wiht the front end based on what functions we write.

    low: 
        Task 3: Analyse the system (er diagram)
        Task 4.2: Write on seprinciples.md 
        Task 5: Reflect on your use of agile practices and how you worked as a team (teamwork.md)
        These tasks are related to documentation, we can develop them along the way.


How multiple people work on the same code:

    Difficulty 1: code dependency 
        Most of our funcions is inter-related, one will not running if another is not working.
    Solution:
        We make a new task board only containing incomplete functions, then write them in the order auth & user-channel-message-standup. 
        After finishing one part, people who wrote this part's code will fix the bugs.

    Difiiculty 2: progression update 
        Meeting is held less than last iteration, online messages can be ignored, new changes made may not be noticed.
    Solution: 
        When a change is made, it is put on the top of task board in red colour to notify everyone.
        When a task is complete, it is ticked in our task board so that others know what is working.
        Therefore we can solve this by checking task board.

    Difficulty 3: merging
        Merging on git can be hard since the code is changed consistently.
    Solution:
        Each one of us makes a new branch, when a piece of code is complete, we put it in the branch calld "iteration 3", others who
        need this code can use from here.


Reflection:

    What went well:
        - Teamwork:
            From last two iteration, our collaboration is continuously getting better along the way. 
            After helping each other out and lots of discussions, trust and harmony in our team is getting stronger.

        - Pair and group programming and discussion: 
            In this iteration, it helped a lot when we improve our code. 
            Better ideas and methods can be generate from this.

        - Refactor:
            Thought our code can still be optimized a lot, our improvement of software engineering design is quite big 
            compare to iteration 2.

        - Planning:
            Our plan was clear for everyone, therefore we all have a sense of what to do and what should be done first 
            and our efficiency is increased.

        - Learning and practice:
            The constant work of this project has significantly enriched our knowledge and practical skill towards software engineering.
        
    Issues:
        - Time management:
            We started too slow which results in a rush when it comes to deadline.
            
        - Incompletion:
            Some parts are not working(i.e. meesage/search, standup/start&send, http error and so on)
            
        - Difficuties related to how multiple people work on the same code.
        