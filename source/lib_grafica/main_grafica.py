####################################################
#Software License:                                 #
#--------------------------------------------------#
#main_grafica.py, a pygame library to handle the Graphics of the game. 
#Copyright (C) 2016  Daniel Santoyo Gomez

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

    #You should have received a copy of the GNU Lesser General Public
    #License along with this library; if not, write to the Free Software
    #Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#contact: daniel.santoyo@gmx.com
import threading
from time import sleep
import os, traceback, sys
THREAD_LOCK = threading.Lock()

import pygame
from pygame.locals import*

#constanti
from game_constants import *

class Sprite():
    '''classe usata per la gestione delle immagini per gli eventi'''

    def __init__(self):
        self.indice = -1
        self.image = None
        self.tile = None
        self.rect = None
        self.nome_sprite = ''
        self.verso = 0
        self._width = 36
        self.sx = 0
        self.sy = 0
        self.sz = 0
        self.zlimit = 0

class GraphicHandler(threading.Thread):
    '''classe per la gestione della grafica. Thread'''

    def __init__(self,name):
        threading.Thread.__init__(self)
        pygame.init()
        ################# manage ###############################
        self.name = name
        self.running = True
        self.FPSCLOCK = pygame.time.Clock()
        self.counter = 0#contatore per aggiornare le informazioni dei tile...
        ################## display ###############################
        self.DISPLAYSURF = pygame.display.set_mode((W, H), DOUBLEBUF | HWSURFACE, 32)
        pygame.display.set_caption('SmallBarrel-Flatlandia')
        self.basicFont = pygame.font.SysFont("Ubuntu",DIMCHAR)
        self.display = pygame.Surface((W,H))#per settare lo sfondo
        self.displayRect = self.display.get_rect()
        
        ################## RAM ###########################
        self.offsetx = 0
        self.offsety = 0
        print "[GRAPHICS]: load RAM\t"
        self.matrice_tiles = None #chunk tiles (matrice[z][y][x])
        self.lista = []
        self.background = self.carica_immagine('background')
        self.backgroundRect = self.background.get_rect()
        self.backgroundRect.topleft = (0,0)
        self.mappa = [] #array di immagini da caricare
        self.mappa_up = []#altre immagini da caricare
        self.mappaRect = None#self.mappa[0].get_rect()
        self.sprites = [] #vettore con gli sprite usati dagli eventi
        
    def __repr__(self):
        t = self.name + "-> Active"
        return t

    def __raise__error(self):        
        print "!!!!!!!!!!!!!!!# WARNING: "+self.name+" IS DOWN !!!!!!!!!!!!!!!"
        self.running = False
        print sys.exc_info()

    def carica_mappa(self):
        self.mappa = []
        self.mappa_up = []
        for z in xrange(len(self.matrice_tiles)): #dimz
            sprite = self.carica_immagine(r"results/hill_"+str(z)+"_d",TRANSPARENCY )
            self.mappa.append(sprite)
        for z in xrange(len(self.matrice_tiles)): #dimz
            sprite = self.carica_immagine(r"results/hill_"+str(z)+"_u",TRANSPARENCY )
            self.mappa_up.append(sprite)
        self.zlimit = z

    def carica_immagine(self,nome,trasp = TRANSPARENCY ):#carica un immagine
        '''carica un'immagine con colore di trasparenza 123,123,123'''
        path = r"../graphics/"+nome+'.png'
        imm = pygame.image.load(path).convert()
        imm.set_colorkey(TRANSPARENCY)
        return imm
            
    def push_single_sprite(self, name, indice):
        '''aggiunge uno sprite all'array sprites'''
        single_sprite = Sprite()
        single_sprite.nome_sprite = name
        single_sprite.image = self.carica_immagine(single_sprite.nome_sprite)
        single_sprite.indice = int(indice)
        single_sprite.rect = single_sprite.image.get_rect()
        self.sprites.append(single_sprite)
    #def pop_single_sprite(self, indice):
    
    def coordinate_iso(self,x,y,z):
        '''trasforma le coordinate da cartesiane in isometriche'''
        xo = W/2 + (x-y+1)*DX
        yo = (x+y)*DY - z*DZ + Y_OFFSET
        #print x,y,z," -> ",xo,yo
        return xo,yo

    def update(self):
        '''aggiorna la grafica'''
        #disegna lo sfondo
        self.mappaRect.midbottom = (self.offsetx + W/2, self.offsety + H)
        self.display.blit(self.background,self.backgroundRect)

        #disegna gli eventi mobili
        sprites = []
        for sprite in self.sprites:
            sprite.tile = sprite.image.subsurface(sprite._width*sprite.verso,0,sprite._width,sprite._width)
            sprite.rect.midbottom = self.coordinate_iso(sprite.sx,sprite.sy,sprite.sz)
            sprite.rect.x += self.offsetx
            sprite.rect.y += self.offsety
            sprites.append(sprite)
            #print sprite.sx,sprite.sy,sprite.sz,"->",sprite.rect.midbottom

        ##disegna i tiles
        sprites.sort(key = lambda s: s.rect.y)#EDTI????
        sprites.sort(key = lambda s: s.sz)#EDTI????
        #for sprite in sprites:
            #self.display.blit(sprite.tile,sprite.rect)
            
        for land in xrange(self.zlimit+1):#self.mappa:
            self.display.blit(self.mappa[land],self.mappaRect)
            for sprite in sprites:
                if sprite.sz == land-1:
                    self.display.blit(sprite.tile,sprite.rect)
            self.display.blit(self.mappa_up[land],self.mappaRect)
            for sprite in sprites:
                if sprite.sz == land-1:
                    self.display.blit(sprite.tile.subsurface(0,0,DWARF_WIDTH,DWARF_HEIGHT/2),sprite.rect)
        
        
        self.DISPLAYSURF.blit(self.display,self.displayRect)

    def run(self):
        print "Starting " + self.name +'\t'
        while self.running:
            try:
                self.FPSCLOCK.tick(FPS)
                THREAD_LOCK.acquire()
                self.update()
                pygame.display.update()
                THREAD_LOCK.release()
                self.counter =  (self.counter + 1)%FPS
                #if self.counter == 0:
                    #self.carica_mappa()
            except:
                print '-'*80
                traceback.print_exc(file=sys.stdout)
                print '-'*80
                self.__del__()
        pygame.quit()

    def __del__(self):
        print "Stopping " + self.name
