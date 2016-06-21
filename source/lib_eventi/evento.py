####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
import threading
from time import sleep
from lib_grafica.game_constants import *
from random import randint
#from Queue import Queue
THREAD_LOCK = threading.Lock()

class Event(threading.Thread):

    def __init__(self,indice,x=0,y=0,z=0):
        threading.Thread.__init__(self)
        self.grafica = ""
        self.verso = 0 #dx = 0 sx = 1
        self.x = x
        self.y = y
        self.z = z
        self.velocita = 0.1#randint(1,9)/10.0
        self.path = []
        self.indice = indice
        self.oggetto = []
        self.bloccato = False
        self.running = True
        self.chunk_ostacoli = None #puntatore a chunk ostacoli
        self.sprite = None
    
    def try_move_random(self, x, y, z, verso):
        '''cerca nel chunk ostacoli per verificare le posizioni valide nelle 4 celle vicine e muoversi'''
        THREAD_LOCK.acquire()
        
        su = 'X'
        giu= 'X'
        dx = 'X'
        sx = 'X'
        if y > 0:
            su = self.chunk_ostacoli.matrice[z][y-1][x]
            if su == T_VOID:
                if z > 0:
                    if self.chunk_ostacoli.matrice[z-1][y-1][x] == FREE:
                        su = T_DOWN
            if su != EVENT:
                if z < D_WORLD-1:
                    if self.chunk_ostacoli.matrice[z+1][y][x] == T_VOID:
                        if self.chunk_ostacoli.matrice[z+1][y-1][x] == FREE:
                            su = T_UP

        if y < H_WORLD-1:
            giu = self.chunk_ostacoli.matrice[z][y+1][x]
            if giu == T_VOID:
                if z > 0:
                    if self.chunk_ostacoli.matrice[z-1][y+1][x] == FREE:
                        giu = T_DOWN
            if giu != EVENT:
                if z < D_WORLD-1:
                    if self.chunk_ostacoli.matrice[z+1][y][x] == T_VOID:
                        if self.chunk_ostacoli.matrice[z+1][y+1][x] == FREE:
                            giu = T_UP
        if x > 0:
            sx = self.chunk_ostacoli.matrice[z][y][x-1]
            if sx == T_VOID:
                if z > 0:
                    if self.chunk_ostacoli.matrice[z-1][y][x-1] == FREE:
                        sx = T_DOWN
            if sx != EVENT:
                if z < D_WORLD-1:
                    if self.chunk_ostacoli.matrice[z+1][y][x] == T_VOID:
                        if self.chunk_ostacoli.matrice[z+1][y][x-1] == FREE:
                            sx = T_UP
        if x < W_WORLD-1:
            dx = self.chunk_ostacoli.matrice[z][y][x+1]
            if dx == T_VOID:
                if z > 0:
                    if self.chunk_ostacoli.matrice[z-1][y][x+1] == FREE:
                        dx = T_DOWN
            if dx != EVENT:
                if z < D_WORLD-1:
                    if self.chunk_ostacoli.matrice[z+1][y][x] == T_VOID:
                        if self.chunk_ostacoli.matrice[z+1][y][x+1] == FREE:
                            dx = T_UP
        ostacoli = [su,sx,dx,giu]
        
        if ostacoli[verso] == FREE or ostacoli[verso] == T_DOWN or ostacoli[verso] == T_UP:
            self.chunk_ostacoli.matrice[z][y][x] = FREE
            
            if verso == 0:
                self.verso = 1
                self.y -= 1
            elif verso == 1:
                self.verso = 0
                self.x -= 1
            elif verso == 2:
                self.verso = 1
                self.x += 1
            elif verso == 3:
                self.verso = 0
                self.y += 1
            if ostacoli[verso] == T_UP:
                self.z += 1
            if ostacoli[verso] == T_DOWN:
                self.z -= 1
            self.chunk_ostacoli.matrice[self.z][self.y][self.x] = EVENT
            
        THREAD_LOCK.release()
