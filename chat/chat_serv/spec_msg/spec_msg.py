import os
import json

def _add_user_config(config=None, complet=True , user):
	if config is None:
		config = {"admin":False}

	if complet:
		config_complet = {"admin":False}
		config.update(config_complet)

	json.dump(config, open("user_config"+user, "w"))

def update_user_config(config_to_add=None, complet=True , user):
	if not user in os.listdir("user_config"):
		_add_user_config(config_to_add, complet, user)
	else:
		config = json.load(open(user, "r"))

		if config is None:
			config = {"admin":False}

		if complet:
			config_complet = {"admin":False}
			config.update(config_complet)
		config.update(config_to_add)

	json.dump(config, open("user_config"+user, "w"))
