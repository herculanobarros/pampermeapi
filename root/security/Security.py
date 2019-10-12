from werkzeug.security import safe_str_cmp
from user import User


users = [
    User(1,'Herculano Barros','abc@gmail.com')
]

user_mapping = {user.username: user for user in users}

userid_mapping = {user.id: user for user in users}



#function to authenticate users
def authenticate(username,password):
    user = user_mapping.get(username, None)
    if user and safe_str_cmp(user.password == password):
        return user


#function to identify users
def identify(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)