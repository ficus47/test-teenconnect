import os
import date
import json

os.makedirs('chat_serv/user', exist_ok=True)

lien = "chat_serv/user/"#r"C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/user/".replace("\\", "/")

def get_name(sender, receiver):
	return "-".join([sender, receiver].sort())

def add_user(user):
		if not user in os.listdir(lien):
				os.makedirs(lien + user)
				os.makedirs(lien + user + "/new")
				os.makedirs(lien + user + "/old")

def check_user(user):
		return user in os.listdir("user")

#def talk(sender, reciever, msg):
#		if check_user(sender) and check_user(reciever):                  #old version, deprecated
#				open(f'user/sender/'+sender+date.get_date(), "w").write(msg)

actual_date = date.get_date()

def register(sender, reciever, msg, register_as_new=True):
		name = get_name(sender, reciever)
		os.makedirs(name, exist_ok=True)
		if check_user(sender) and check_user(reciever):
			open(lien + f"{name}/"+actual_date, "w+")
			json.dump({"msg":msg, "reciever":reciever}, open(lien + f"{reciever+'-'+sender}"+actual_date+".json", "w+"))

	#if register_as_new:
	#	if check_user(sender) and check_user(reciever):
	#		open(lien + reciever + "/new/recieve/"+actual_date+".json", "w+")
	#		json.dump({"msg":msg, "receiver":sender}, open(lien + reciever + "/new/recieve/"+actual_date+".json", "w+"))
	#else: 
	#	if check_user(sender) and check_user(reciever):
	#		open(lien + reciever + "/old/recieve/"+actual_date+".json", "w+")
	#		json.dump({"msg":msg, "receiver":sender}, open(lien + reciever + "/old/recieve/"+actual_date+".json", "w+"))

def see_msg(user, other):
	if check_user(user):
		msg_list = os.listdir(lien + get_name(user, other))
		msg_dict = [{msg:json.load(open(lien + get_name(user, other)+msg))} for msg in msg_list]
		return msg_dict
	else:
		return []