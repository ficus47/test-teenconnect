import websockets
import asyncio
import json

async def client():
    # Se connecter au serveur WebSocket
    async with websockets.connect("ws://172.28.80.1:9999") as websocket:
        # envoyer la demande d'authentification au serveur
        await websocket.send(json.dumps({"from":"moi2", "password":"48562"}))
        #envoie d'un message
        await websocket.send(json.dumps({"msg":"bj tout le monde", "action":"send_grp"}))
        # Recevoir la réponse du serveur
        response = json.loads(await websocket.recv())        
        print(f"Réponse du serveur : {response}")

# Lancer le client
asyncio.run(client())