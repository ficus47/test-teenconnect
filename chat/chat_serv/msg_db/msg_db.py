import os
import date
import json 

os.makedirs('chat_serv/user', exist_ok=True)

lien = "chat_serv/user/"#r"C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/user/".replace("\\", "/")

def get_name(sender, receiver):
	return "-".join(sorted([sender, receiver]))

def add_user(user):
	pass

def check_user(user):
	return user in os.listdir("chat_serv/user_password")

#def talk(sender, reciever, msg):
#		if check_user(sender) and check_user(reciever):                  #old version, deprecated
#				open(f'user/sender/'+sender+date.get_date(), "w").write(msg)

def register(sender, reciever, msg, register_as_new=True):
		actual_date = date.get_date()
		name = get_name(sender, reciever)
		os.makedirs(lien+name, exist_ok=True)
		if check_user(sender) and check_user(reciever):
			open(lien + f"{name}/"+actual_date+".json", "w")
			json.dump({"msg":msg, "sender":sender}, open(lien + f"{name}/"+actual_date+".json", "w+"))

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
		try:
			msg_list = os.listdir(lien + get_name(user, other))
			msg_list.reverse()
			msg_dict = []
			for msg in msg_list:
				sender = json.load(open(lien + get_name(user, other)+"/"+msg))["sender"]
				block = not sender != user 
				msg_dict.append({"msg":json.load(open(lien + get_name(user, other)+"/"+msg))["msg"], "date":msg.split(".")[0], "sender":sender, "block":block})

			return msg_dict
		except Exception as e:
			os.makedirs(get_name(user, other), exist_ok=True)
			return []
	else:
		print(user)
		return []