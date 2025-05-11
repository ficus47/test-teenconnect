import os 
import json

lien = ''

os.makedirs("blocked_user", exist_ok=True)

def block_user(user, user_to_block):
	try:
		set_user = json.load(open("blocked_user/"+user+'.json'))
		set_user += [user_to_block]
		set_user = list(set(set_user))
		json.dump(set_user, open("blocked_user/"+user+'.json', "w"))
	except Exception:
		set_user = [""]
		set_user.append(user_to_block)
		json.dump(set_user, open("blocked_user/"+user+'.json', "w"))

def is_user_blocked_by_other(user, other):
	try:
		return other in json.load(open("blocked_user/"+user+'.json'))
	except Exception:
		open("blocked_user/"+user+'.json', "w").write("['']")
		return False

def unblock_user(user, other):
	if is_user_blocked_by_other(user, other):
		set_user = json.load(open("blocked_user/"+user+'.json'))
		del set_user[set_user.index(other)]
		json.dump(open("blocked_user/"+user+'.json'), set_user)
		