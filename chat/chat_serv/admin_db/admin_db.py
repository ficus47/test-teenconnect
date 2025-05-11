import os 

lien = "chat_serv"#r"C:/Users/Coqen/OneDrive/Bureau/tout_python/chat_serv/"

def check_admin(admin):
	return admin in os.listdir("admin_db")

def add_admin(user):
	open(lien+"admin_db"+user+"txt", "w")
	return True
