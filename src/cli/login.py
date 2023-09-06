from apps.recommend import recommend_dinner_list
from os.path import join as pathjoin
import json


def create_new_user(username: str):
    with open(pathjoin('configs', 'general.json'), 'r') as f:
        users = json.load(f)['users']   
    
    if username not in users:
        new_user = { 'username': username,
            'settings': {
                'dinnerListReciever': None
            } 
        }
        
        with open(pathjoin('configs', 'users', f'{username}.json'), 'x') as f:
            json.dump(new_user, f)        
    else:
        print('User with that name already exists')
    

def user_login() -> str:
    with open(pathjoin('configs', 'general.json'), 'r') as f:
        content: dict = json.load(f)
        users: list = content['users']

    if len(users) != 0:
        if content['lastUserLoggedIn'] == "":
            print('0. [No User]')
            for index, user in enumerate(users):
                print(f'{index + 1}. {user}')
            user_chosen: int  = int(input('Choose a user to log in as (by number): '))

            if user_chosen == 0:
                return ''
            elif user_chosen <= len(users) and (user_chosen >= 0):
                with open(pathjoin('configs', 'general.json'), 'w') as f:
                    content['lastUserLoggedIn'] = users[user_chosen - 1]
                    json.dump(content, f, indent=2)
                return users[user_chosen - 1]
            else:
                print('Invalid User Choice')
        else:
            return content['lastUserLoggedIn']
        
   
    else:
        print('There are no users registered')
        print('You can continue with not logged in, but some functionality will be unavailable')
        inp = input('Would you like to register a new user [yes or no]: ')
        
        while True:                
            if inp.lower() in 'yes':
                inp: str = input('Enter the name of new user: ')
                users.append(inp)
                create_new_user(username=inp)
                with open(pathjoin('configs', 'general.json'), 'w') as f2:
                    content['users'] = users
                    json.dump(content, f2, indent=2)
                print(f'Created new user {inp}')
                return inp
            elif inp.lower() in 'no':
                return ''
            else:
                print('Please try again.')
                continue
    

def on_login(user: dict = None):
    import os

    if user['settings']['dinnerListReciever'] is not None:
        recommend_dinner_list(eval(user['settings']['dinnerListReciever']))        
    
        