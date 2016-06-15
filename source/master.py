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
import sys, traceback
from random import randint
from time import sleep

THREAD_LOCK = threading.Lock()
DEBUG = 0
INITIALIZE = 1

from lib_scribi import nomi_lingue
from lib_eventi import nano

from lib_grafica.game_constants import *
from lib_grows import chunk
from lib_grows import genesi
from lib_grafica import main_grafica

class Master (threading.Thread):
    '''classe per la gestione della comunicazione tra le librerie. Thread'''

    def __init__(self, name, mode=1):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.timer = 0.5
        self.mode = mode
        self.LOG_DEBUG = False#True
        self.dwarfs = []
        #-----------------------------------------------------------------------------#
        # world creation
        World = genesi.World_maker('[WORLD MAKER]')
        World.crea_montagne_perlin(20)
        World.conservatore(20)
        self.matrice_tiles = World.start()
        #-----------------------------------------------------------------------------#
        
        THREAD_LOCK.acquire()
        self.grafica = main_grafica.GraphicHandler('[GRAPHICS]')
        self.grafica.matrice_tiles = self.matrice_tiles
        print self.name, "MATRICE_TILES added to [GRAPHICS]"
        self.grafica.carica_mappa()
        self.grafica.mappaRect = self.grafica.mappa[0].get_rect()
        
        if self.mode == DEBUG:
            
            sleep(1)
            ##############INITIALIZE DEBUG MODE###################
            self.ck_ostacoli = chunk.Chunk(0) #ostacoli
            self.ck_ostacoli.carica_matrice(self.grafica.matrice_tiles)

            #CENTRO CITTA'
            x = randint(0,W_WORLD-1)
            y = randint(0,H_WORLD-1)
            z = 0
            while(True):
                try:
                    if self.ck_ostacoli.matrice[z][y][x] == ' ':
                        break
                except:
                    pass
                z += 1
                if z == D_WORLD:
                    x = randint(0,W_WORLD-1)
                    y = randint(0,H_WORLD-1)
                    z = 0
            print x,y,z, "centro"
            self.centerx = x
            self.centery = y
            self.centerz = z
            
            for i in range(NUM_DWARFS):
                n = nano.Nano('',i)
                n = genesi.nano_random(n)
                self.dwarfs.append(n)
                self.grafica.push_single_sprite(n.grafica, n.indice)
                
                n.x = x
                n.y = y
                n.z = z 
            print self.name + ": created %d dwarfs"%NUM_DWARFS
            
            for d in self.dwarfs:
                d.chunk_ostacoli = self.ck_ostacoli #puntatore al chunk ostacoli
                d.sprite = self.grafica.sprites #puntatore agli sprites della grafica
                d.start()
            ###############INITIALIZE DEBUG MODE###################
       
        self.grafica.start()# Thread
        THREAD_LOCK.release()
        
    def __repr__(self):
        t = self.name + "-> Active"
        return t

    def __raise__error(self):        
        print "!!!!!!!!!!!!!!!# WARNING: "+self.name+" IS DOWN !!!!!!!!!!!!!!!"
        self.running = False
        print sys.exc_info()

    def run(self):
        print "Starting " + self.name + " in DEBUG mode\t"*(self.mode == DEBUG)
        while self.running:
            try:
                sleep(self.timer)

            except:
                print '-'*80
                traceback.print_exc(file=sys.stdout)
                print '-'*80
                self.running = False
                self.__del__()

    def __del__(self):
        self.grafica.running = False
        print self.name + ": stopping dwarfs Threads"
        for d in self.dwarfs:
            d.running = False
        THREAD_LOCK.acquire()
        THREAD_LOCK.release()
        print "Stopping " + self.name
        
