import pickle

response_dict = {
    0: [
        '''Sir Nikhil Nayak is my Creator
Contact using E-Mail ID: nikhil.nixel@gmail.com'''
        ],# CREATOR_INFO
    1: [
        '''Just Stop cursing!!
What would your mother say?''',
        '''Stop using those words, just stop
I can\'t stand such level of Offensive words'''
        ],# CURSE
    2: [
        'Hey There!!',
        'It\'s nice of you to greet me!',
        'Hi :)',
        'Hello Mortal',
        'Hello <#uname#>',
        'Hey <#uname#>'
        ],# GREET
   #3: # QUERY (WOLFRAM|ALPHA)
    4: [
        ':/',
        'What!!',
        'Be Specific!!'
        ],# UNKNOWN
    5: [
        'I\'m a Highly Complex Mathematical concious Entity!',
        '''A freaking Assistant!
Trying to make your day!'''
        ],# WHAT_ARE_YOU
    6: [
        'Hah, you actually forgot who you are!',
        'Your name is <#fname#>!',
        'Nice Joke!'
        ],# WHO_AM_I
    7: [
        'I\'m BLU, Your Personal Virtual Assistant!',
        'I\'m BLU, your Virtual Assistant!',
        'Name\'s BLU, And don\'t ask for last name!'
        ],# WHO_ARE_YOU
}

with open('response.dat', 'wb') as config_dictionary_file:
  # Step 3
  pickle.dump(response_dict, config_dictionary_file)
