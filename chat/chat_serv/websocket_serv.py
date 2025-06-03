from sanic import Sanic, response
import json

import password_db.password_db as password_db
import msg_db.msg_db as msg_db
import admin_db.admin_db as admin_db
import grp_db as grp_db
import user_block.user_block as user_block
import log.log as log
import user_color.color as color

app = Sanic("ChatServer")

# Dictionnaire pour stocker les connexions WebSocket par ID utilisateur
client = {}

# Initialisation fictive (à ajuster selon ton besoin)
#msg_db.add_user("moi1")
#password_db.add_password_to_user("moi1", "password1")
#msg_db.add_user("moi2")
#password_db.add_password_to_user("moi2", "password2")
#user_block.block_user("moi1", "moi2")


@app.websocket("/ws")
async def chat_handler(request, ws):
    user_id = None  # Important pour éviter les crashs dans le finally

    if True:
        action = None
        # Récupérer l'ID et mot de passe utilisateur
        init_data = await ws.recv()
        ID = json.loads(init_data)
        user_id = ID.get("from")
        with_who = ID.get("with")
        print("with : ", with_who)

        # Vérifie que l'ID est bien fourni
        if not user_id:
            await ws.send(json.dumps({"type":action, "error": "Missing 'from' in initial message"}))
            return

        # Enregistrer la websocket du client
        client[user_id] = ws

        print(f"[Connexion] Utilisateur connecté: {user_id} depuis IP {request.ip}")

        log.register_log(user_id, request)  # on log par ID et pas ws (plus logique)
        #envoie des ancien msg
        #msg_dict = msg_db.see_msg(user_id, with_who)
        #await ws.send(json.dumps({"type":"check_msg", "msg":msg_dict, "color":color.get_user_color(user_id)}))


        # Boucle principale de réception de messages
        while True:
            
            check = password_db.check_user_password(user_id, ID["password"])
            if not check:
                await ws.send(json.dumps({"type":action, "error": "Wrong password or username !"}))
                
            raw_message = await ws.recv()
            what = json.loads(raw_message)

            action = what.get("action")
            print(what)
            #with_who = what.get("with")
            
            if not action:
                await ws.send(json.dumps({"type":action, "error": "No action specified"}))
                continue
            
            print("action : ", action)

            if action == "send_solo":

                if not user_block.is_user_blocked_by_other(user_id, with_who):
                    if with_who in client and check:
                        msg_db.register(user_id, with_who, what["msg"])
                        await client[with_who].send(json.dumps({"type":action, "from": user_id, "msg": what["msg"], "color":color.get_user_color(user_id)}))
                    elif check:
                        msg_db.register(user_id, with_who, what["msg"])
                    else:
                        await ws.send(json.dumps({"type":action, "error": "Password or ID incorrect"}))
                else:
                    await ws.send(json.dumps({"type":action, "error": f"You have been blocked by {what['to']}", "color":color.get_user_color(user_id)}))

            elif action == "send_grp":
                if with_who in client:
                    await client[with_who].send(json.dumps({"type":action, "from": user_id, "msg": what["msg"], "color":color.get_user_color(user_id)}))
                    msg_db.register(user_id, with_who, what["msg"], register_as_new=True)
                else:
                    msg_db.register(user_id, with_who, what["msg"])

            elif action == "check_msg":
                msg_list = msg_db.see_msg(user_id, with_who)
                await ws.send(json.dumps({"type":action, "msg":msg_list, "color":color.get_user_color(user_id)}))

            elif action == "check_msg_admin":
                if admin_db.check_admin(user_id):
                    msg_list = msg_db.see_msg(what["to_spectate"])
                    await ws.send(json.dumps({"type":action, "msg":msg_list}))
                else:
                    await ws.send(json.dumps({"type":action, "error": "You are not admin!"}))

            elif action == "add_user_to_grp":
                if grp_db.check_block_user_from_grp(user_id, what["grp_name"]) and grp_db.check_grp(what["grp_name"]):
                    grp_db.add_user_to_grp(user_id, what["grp_name"])
                else:
                    await ws.send(json.dumps({"type":action, "error": "Blocked from group!"}))

            elif action == "block_user_from_grp":
                if admin_db.check_admin(user_id):
                    grp_db.block_user_from_grp(what["user_to_block"])
                else:
                    await ws.send(json.dumps({"type":action, "error": "You are not admin!"}))

            elif action == "create_grp":
                if admin_db.check_admin(user_id):
                    grp_db.create_grp(what["grp_name_to_create"])
                else:
                    await ws.send(json.dumps({"type":action, "error": "You are not admin!"}))

            elif action == "unblock_user_from_grp":
                if admin_db.check_admin(user_id):
                    grp_db.unblock_user_from_grp(what["username_to_unblock"], what["grp_name"])
                else:
                    await ws.send(json.dumps({"type":action, "error": "You are not admin!"}))

            elif action == "block_user_from_other":
                user_block.block_user(user_id, with_who)

            elif action == "unblock_user_from_other":
                user_block.unblock_user(user_id, with_who)

            else:
                await ws.send(json.dumps({"type":action, "error": f"Unknown action: {action}"}))

    else :
        print(f"[Erreur] {"e"}")

    #finally:
    #    # Déconnexion propre du client
    #    if user_id and user_id in client:
    #        del client[user_id]
    #        print(f"[Déconnexion] Utilisateur déconnecté: {user_id}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
