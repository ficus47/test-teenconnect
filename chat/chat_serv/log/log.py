import os
import json

lien = "chat_serv/" #r"C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/"


def register_log(ws, request):
	dict_log = {
	"url":request.ip,
	"ws":str(ws),
	}
	
	current = json.load(open(lien + "log.json", 'r'))
	if current:
		current += dict_log
	else:
		current = [dict_log]
	json.dump(current, open(lien + "log.json", 'w'))