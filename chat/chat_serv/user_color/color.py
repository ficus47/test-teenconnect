import os
import json

lien = "color_user/"

delfaut_color = "#0B04BA"

def add_user(user, color): #color in hexa
    json.dump([color], open(lien+user, "w"))

def get_user_color(user):
    if os.path.isfile(lien+user) and open(lien+user).read():
        return json.load(open(lien+user))[0]
    else:
        add_user(user, delfaut_color)
        return delfaut_color
    