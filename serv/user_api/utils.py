import newfile as User

import os
import json

def load_user(path):
    user = User()
    user.load(path)
    return user

def save(user, path):
    os.makedirs(user.pseudo, exist_ok=True)
    user.save(user.pseudo+"/"+path)

def save_user_post(post, name, user, format, desc):
    path = user.pseudo + "/"
    os.makedirs(path+"post", exist_ok=True)
    try:
        name = list(os.listdir(path))
        last = int(name[:-1][:name.index(".")])
    except Exception:
        last = 0
    
    os.makedirs(str(last))

    with open(path+str(last)+"/img."+format, "w") as f:
        f.write(post)
        f.close()
    
    json.dumps(open(path+str(last)+"json.json", "w"), {"desc":desc, "name":name, "user":user})
    