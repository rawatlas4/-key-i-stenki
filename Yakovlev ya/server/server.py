import pygame
from socket import*
import threading

server = socket(AF_INET,SOCK_STREAM)
server.bind(("localhost",2010))
server.listen(5)
server.setblocking(False)
players = {}
id = 0
def obmen():
    while 1:
        # pygame.time.delay(10)
        try:
            for conect in list(players):
            
                danni = conect.recv(1024).decode()
                danni = danni.split(",")
                danni2 = list(map(int,danni))
                if len(danni2) == 4:
                    players[conect]["x"] = danni2[1]
                    players[conect]["y"] = danni2[2]
                    players[conect]["radius"] = danni2[3]
                    
            
                pocket = ""
                for key,znachenie in players.items():
                    if key != conect:
                        line = f"{znachenie['id']},{znachenie['x']},{znachenie['y']},{znachenie['radius']},{znachenie['name']}"
                        pocket += line +"|"

                conect.send(pocket.encode())
            
        except:
                pass
            
            
            
threading.Thread(target=obmen).start()


while 1:
    try:
        conect,ip = server.accept()
        conect.setblocking(False)
        print("i pahay",ip)
        id+=1
        players[conect] = {
            "id":id,
            "x":0,
            "y":0,
            "radius":20,
            "name":None
        }
        conect.send(f"{id},0,0,20".encode())
    except:
        pass