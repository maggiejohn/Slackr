1.Verification:
Verification is the process of checking that a software achieves its goal without any bugs. 
It is the process to ensure whether the product that is developed is right or not. It verifies whether the developed product fulfills the requirements that we have.
Testing of ‘not the absence of bugs’. 
Focus: Compare if input and output matches

2.Validation:
Validation is the process of checking whether the software product is up to the mark or in other words product has high level requirements. 
So, when validating, we need to consider a wider range of inputs compared to verification, this is usually done by the customer.This process is much related to acceptance criteria.
Raise exceptions: Test: ‘customer expectation and requirements has been met’

3.Examples: 
This is how  we make sure verification and validation works in auth_register():
                @APP.route('/auth/register', methods=['POST'])
                def register():
                    email = request.form.get('email')
                    password = request.form.get('password')
                    name_first = request.form.get('name_first')
                    name_last = request.form.get('name_last')
                    dic = auth_register(email, password, name_first, name_last)
                    return dumps(dic)
                    
1.According to the definition of varification and validation, based on our understanding, we should check verifictaion first to make sure it is developed right.
　  1.1 Verification:
    　  -Ask ourselves:"The dictionary returned after we registerd is supposed to have ‘u_id’and ‘token’ (no errors)"
        -What we do to check:
            put right input of email,password,name_first,name_last and check API if it is the expected output without bugs
        -what we got:
        -{'email': matt@qq.com; 'password':123aaa; 'name_first':matt; 'name_last':john}
        -{"u_id": 1, "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1hdHRAcXEuY29tIn0.v5FZipbFYkT_oyUl65d-eqWqYFGgBTbVMI86i-w_5EI"}
        "verification is checked"
        -we focus more on whether input match output
        return { 
           'u_id': user_id, 
           'token':encoded_jwt.decode('utf-8')
        }

  1.2 Validation: 
    -Ask ourselves:"If I use an email that has already been registerd, does it disable the register?"
    -What we do to check:
    Consider wider range of input than verification, this is usually done by the customer
    Validation comes from acceptance criteria of au_register:
    -User story:As a user, I would like to register for an account, so that I can access the required workspace and channels:
        -Acceptance criteria :
            -Information that must be provided: First and Last Name, Email, Password
            -Password must be greater than 5 characters
            -Email must be valid(not registered)
            -Can check if email has been registered
            -Once registered, user will automatically be logged in
    
    choose registered email:
    -What we got:
        {email:matt@qq.com;password:weeeee;name_first:matt;name_last:john}
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
            <title>400 Bad Request</title>
            <h1>Bad Request</h1>
            <p>Email has been registered</p>
     
    "validation is checked"
    we focus more on:
    for i in range(len(userDatabase)): 
        if userDatabase[i]['email'] == email:
            error_raise.existed_email()