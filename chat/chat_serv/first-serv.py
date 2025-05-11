import asyncio
import websockets
import json
import password_db.password_db as password_db
import msg_db.msg_db as msg_db
import admin_db.admin_db as admin_db
import grp_db.grp_db as grp_db
import user_block.user_block as user_block
import log.log as log

client = {}

msg_db.add_user("moi1")
msg_db.add_user("moi2")

async def serv_connection(websocket, path):
	ID = json.loads(await websocket.recv())
	client[ID["from"]] = websocket

	print(ID)

	what = await websocket.recv()
	log.register_log(websocket)

	if what["action"] == "send_solo":
		check = password_db.check_user_password(ID["from"], ID["password"])
		tronq(ID["from"])
		if not user_block.is_user_blocked_by_other(ID["from"], what["to"]):
	
			if what["to"] in client and check:
				client[what["to"]].send({"from":ID["from"], "msg":what["msg"]})
				msg_db.register(ID["from"], what["to"], what["msg"], register_as_new=True)
			elif check:
				msg_db.register(ID["from"], what["to"], what["msg"])
			else:
				await websocket.send(json.dumps("error : password or ID not right"))
		else:
			websocket.send(json.dumps("you have been blocked by " + what["to"] + '!'))

	elif what["action"] == "send_grp":

		if what["to"] in client:
			client[ID["to"]].send({"from":ID["from"], "msg":what["msg"]})
			msg_db.register(ID["from"], ID["to"], what["msg"], register_as_new=True)
		elif check:
			msg_db.register(ID["from"], ID["to"], what["msg"])
		else:
			await websocket.send(json.dumps("error : password or ID not right"))

	elif what["action"] == "check_msg":
		msg_list = msg_db.see_msg(ID["from"])
		msg_db.tronq(user)
		await websocket.send(json.dumps(msg_list))

	elif what["action"] == "check_msg_admin":
		if admin_db.check_admin(ID["from"]):
			msg_list = msg_db.see_msg(ID["to_spectate"])
			msg_db.tronq(user)
			await websocket.send(json.dumps(msg_list))
		else:
			await websocket.send(json.dumps("error : you are not admin !"))

	elif what["action"] == "add_user_to_grp":
		if grp_db.check_block_user_from_grp(ID["from"], what["grp_name"]) and grp_db.check_grp(what["grp_username"]):
			grp_db.add_user_to_grp(ID["from"], what["grp_name"])

		else:
			websocket.send("error ! you are blocked from this grp !")
			
	elif what["action"] == "block_user_from_grp":
		if admin_db.check_admin(ID["from"]):
			grp_db.block_user_from_grp(what["user_to_block"])
		else:
			await websocket.send(json.dumps("error : you are not admin !"))

	elif what["action"] == "create_grp":
		if admin_db.check_admin(ID["from"]):
			grp_db.create_grp(what["grp_name_to_create"])
		else:
			await websocket.send(json.dumps("error : you are not admin !"))

	elif what["acton"] == "unblock_user_from_grp":
		if admin_db.check_admin(ID["from"]):
			grp_db.unblock_user_from_grp(ID["username_to_unblock"], what["grp_name"])
		else:
			await websocket.send(json.dumps("error : you are not admin !"))

	elif what["acton"] == "block_user_from_other":
		user_block.block_user(ID["from"], what["to"])

	elif what["acton"] == "unblock_user_from_other":
		user_block.unblock_user(ID["from"], what["to"])


async def main():
    # Créer le serveur WebSocket
    start_server = websockets.serve(serv_connection, "0.0.0.0", 9999)
    
    # Démarrer le serveur
    server = await start_server
    
    # Garder le serveur en cours d'exécution
    print("Serveur WebSocket démarré sur ws://0.0.0.0:9999")
    await server.wait_closed()

asyncio.run(main())