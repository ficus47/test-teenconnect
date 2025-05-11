import json
import os

lien = "C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/grp/"

def add_user_to_grp(user, grp):
	if grp in os.listdir(lien):
		dict_grp = json.load(open(lien+grp))
		if dict_grp["list_type"] == "white":
			return True
		else:
			try:
				dict_grp["user"].append(user)
				return True
			except exception:
				dist_grp["user"] = [user]
				return True
			else:
				return False
		json.dumps(dict_grp, open(lien+grp))

def block_user_from_grp(user, grp):
	if grp in os.listdir(lien):
		dict_grp = json.load(open(lien+grp))
		try:
			if not user in dict_grp["ban_users"]:
				dict_grp["ban_users"].append(user)
			else:
				return False
		except exception:
			dict_grp["ban_users"] = [user]

		json.dumps(dict_grp, open(lien+grp))

def check_block_user_from_grp(user, grp):
	if grp in os.listdir(lien):
		dict_grp = json.load(open(lien+grp))
		try:
			return user in dict_grp["ban_users"]
		except exception:
			pass

def unblock_user_from_grp(user, grp):
	if grp in os.listdir(lien):
		dict_grp = json.load(open(lien+grp))
		try:
			if user in dict_grp["ban_users"]:
				del dict_grp["ban_users"][user]
			else:
				return False
		except exception:
			dict_grp["ban_users"] = []
		json.dumps(dict_grp, open(lien+grp))


def create_grp(grp):
	os.makedirs(grp, exist_ok=True)

def check_grp(grp):
	return grp in os.listdir(lien)