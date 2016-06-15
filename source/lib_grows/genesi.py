####################################################
#Software License:                                 #
#--------------------------------------------------#
#genesi.py, a pygame library to create the images of the game. 
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
from random import randint
import os.path
import threading
from perlin_noise import PerlinNoise
import cPickle as pickle
from pygame import image as Image
from pygame import Surface
from lib_scribi import nomi_lingue
from lib_grafica.game_constants import *

def nano_random(n): #EDIT: da sistemare
    n.nome = nomi_lingue.nome_random(n.sesso)
    n.cognome = nomi_lingue.cognome_random()
    n.eta = randint(1,50)
    vitalita = [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 17, 17, 17, 16, 16, 16, 16, 15, 15, 15, 14, 14, 14, 13, 13, 13, 13, 12, 12, 12, 11, 11, 11, 11, 10, 10, 10, 9, 9, 9, 9, 9, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6, 6, 6, 6]
    n.vitalita = vitalita[n.eta]+randint(1,3)
    n.salute = n.vitalita
    forza = [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 20, 20, 20, 19, 19, 18, 18, 17, 17, 16, 16, 15, 15, 14, 14, 13, 13, 12, 12, 11, 11, 10, 10, 9, 9, 9, 8, 8, 7, 7, 7, 6, 6, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
    n.forza = forza[n.eta]+randint(1,3)
    t = 0
    arr = []
    for i in range(n.eta):
        if(i%2)==0:
            t += randint(0,2)        
    n.intelligenza = t
    t = 0
    for i in range(n.eta):
        if(i%3)==0:
            t += randint(0,2)
        if t > 20:
            t = 20
    n.saggezza = t
    t = 0
    for i in range(3):
        t += randint(1,7)
    n.carisma = t
    #psico
    t = 0
    for i in range(3):
        t += randint(1,7)
    n.umilta = t
    t = 0
    for i in range(3):
        t += randint(1,7)
    n.compassione = t
    t = 0
    for i in range(3):
        t += randint(1,7)
    n.carattere = t
    #modifica velocita'
    return n
#----------------------------------------------------------------------#

class World_maker(threading.Thread):

    def __init__(self,name):
        threading.Thread.__init__(self)
        self.tiles = []
        self.matrice = {}
        self.name = name
        self.pkl_name = ""

    def apri_matrice_testuale(self, filename):
        if os.path.isfile(filename+'.pkl'):
            print "[WORLD MAKER]: load", filename, "\t"
            self.matrice = pickle.load( open( filename+".pkl", "rb" ) )
            load = True
            self.pkl_name = filename+'.pkl'
        else:
            '''apre un file di testo casuale con interi separati da spazio, toglie il \n alla fine di ogni riga
            e trasforma tutti i valori in interi. restituisce un array'''
            filename = filename.strip('.txt')
            with open(filename+'.txt', "r") as file:
                matr = map(lambda v: v[:-1].split(), file.readlines() )
                matr = reduce(lambda x,y: x+y, matr)
                matr = map(lambda x: int(x),matr)
            self.pkl_name = filename+'.pkl'
            for id in range(max(matr)):
                self.matrice[id] = [ [] for _ in range(H_WORLD)]
                for y in range(H_WORLD):
                    t = []
                    for x in range(W_WORLD):
                        value = T_VOID
                        if matr[x+y*W_WORLD] >= id:
                            value = T_ERBA
                        t.append(value)
                    self.matrice[id][y] = t
            self.dimz = len(self.matrice)
            self.dimy = len(self.matrice[0])
            self.dimx = len(self.matrice[0][0])
            load = False
        self.maximun = len(self.matrice)
        return load

    def get_dims(self):
        self.dimz = len(self.matrice)
        self.dimy = len(self.matrice[0])
        self.dimx = len(self.matrice[0][0])

    def genera_montagna(self, W_WORLD,H_WORLD, nome = ""):
        '''carica una collina casuale dalla memoria ROM e prepara la matrice'''
        if nome == "":
            #verifica l'esistenza di una montagna gia' creata in graphics/results
            nome = r"lib_grows/perlin_maps/collina"+str(randint(0,19))
            for i in xrange(20):
                filename = r"../graphics/results/collina"+str(i)
                if os.path.isfile(filename+".pkl"):
                    nome = filename
                    print "[WORLD MAKER]: found "+filename+".pkl in memory... load\t"
                    break

        if self.apri_matrice_testuale(nome) == False:
            #modifica il chunk, gestisci i tile erba e la sabbia
            for z in xrange(self.dimz):
                for y in xrange(self.dimy):
                    for x in xrange(self.dimx):
                        if self.matrice[z][y][x] == T_VOID:
                            if z <= Z_SEA:
                                self.matrice[z][y][x] = T_ACQUA
                            
                        if self.matrice[z][y][x] == T_ERBA:
                            if z < self.dimz-1:
                                if y < self.dimy-1 and x < self.dimx -1:
                                    if self.matrice[z+1][y][x] == T_ERBA:
                                        if self.matrice[z][y+1][x] == T_ERBA and self.matrice[z][y][x+1] == T_ERBA:
                                            self.matrice[z][y][x] = T_HIDE
                                            continue
                                if z == Z_SEA:
                                    if y < self.dimy-1:
                                        if self.matrice[z][y+1][x] == T_VOID:
                                            self.matrice[z][y][x] = T_SABBIA
                                            continue
                                    if x < self.dimx-1:
                                        if self.matrice[z][y][x+1] == T_VOID:
                                            self.matrice[z][y][x] = T_SABBIA
                                            continue
                                    if x > 0:
                                        if self.matrice[z][y][x-1] == T_VOID:
                                            self.matrice[z][y][x] = T_SABBIA
                                            continue
                                    if y > 0:
                                        if self.matrice[z][y-1][x] == T_VOID:
                                            self.matrice[z][y][x] = T_SABBIA
                                            continue
                                if z < Z_SEA and self.matrice[z+1][y][x] == T_VOID:
                                    self.matrice[z][y][x] = T_SABBIA
                                    continue
                                if self.matrice[z+1][y][x] != T_VOID:
                                    self.matrice[z][y][x] = T_TERRA
                            if z >= Z_SNOW:# gestisci la neve
                                if self.matrice[z][y][x] == T_ERBA:
                                    self.matrice[z][y][x] = T_NEVE
                            border_type = 0
                            if self.matrice[z][y][x-1] == T_VOID:
                                border_type = border_type | 1
                            if self.matrice[z][y-1][x] == T_VOID:
                                border_type = border_type | 2
                            self.matrice[z][y][x] += '_'+str(border_type)
                            
        else:
            self.get_dims()

    def conservatore(self, num): #picklellatore per le matrici testuali
        print "scrittura pickle in corso"
        for i in range(num):
            print "%3.2f %%" % (float(i*100.0/num)),"\r",
            nome = r"lib_grows/perlin_maps/collina"+str(i)+".txt"
            self.matrice = {}
            self.genera_montagna(W_WORLD,H_WORLD, nome)
            pickle.dump( self.matrice, open( nome.split('.')[0]+'.pkl', "wb" ) )

    def load_tile(self,element,z, side = 1): # side = 1: bottom, side = 0: top
        if element == T_VOID:
            return False
        else:
            tile = Image.load(r"../graphics/tile"+element+".png")
            if element == T_ACQUA:
                if side == 0:
                    return tile
                else:
                    return False
            tile = tile.subsurface(0,side*(BLOCCOY/2),BLOCCOX,BLOCCOY/2)#left top width height
        return tile
    
    def genera_immagini_chunk(self):
        filename = r"../graphics/results/"+ self.pkl_name.split('/')[-1]
        if os.path.isfile(filename):
            print "[WORLD MAKER]: nothing to save..."
            return
        z_max = self.maximun
        dz_height = int((z_max)*(BLOCCOY-2*DY))
        height  = int(2*DY*(self.dimy-1)+BLOCCOY  + dz_height)
        width   = int(BLOCCOX*(self.dimx))
        print "[WORLD MAKER]: generation of chunk images\t"
        background_final = Surface((width, height))
        background_final.set_colorkey(TRANSPARENCY)
        background_final.fill(TRANSPARENCY)
        
        for z in range(self.dimz):
            background = Surface((width, height)) #immagine con i tiles bassi
            foreground = Surface((width, height)) #immagine con i tiles alti
            background.fill(TRANSPARENCY)
            foreground.fill(TRANSPARENCY)
            background.set_colorkey(TRANSPARENCY)
            foreground.set_colorkey(TRANSPARENCY)
            for y in range(self.dimy):
                for x in range(self.dimx):
                    tile    = self.load_tile(self.matrice[z][y][x],z,1)
                    tile_up = self.load_tile(self.matrice[z][y][x],z,0)
                    if tile:
                        xo = width/2 + (x-y-1)*DX
                        yo = (x+y)*DY - z*DZ + dz_height
                        tileRect = tile.get_rect()
                        tileRect.topleft = (int(xo),int(yo)+BLOCCOY/2)
                        background.blit(tile,tileRect)
                    if tile_up:
                        xo = width/2 + (x-y-1)*DX
                        yo = (x+y)*DY - z*DZ + dz_height
                        tileRect = tile_up.get_rect()
                        tileRect.topleft = (int(xo),int(yo))
                        foreground.blit(tile_up,tileRect)
                        
                        
            background_final.blit(background,background.get_rect())
            background_final.blit(foreground,background.get_rect())
            data = Image.tostring(background, "RGBA")
            surf = Image.fromstring(data, (width, height), 'RGBA', False)
            Image.save(surf,r"../graphics/results/hill_"+str(z)+"_d.png")
            data = Image.tostring(foreground, "RGBA")
            surf = Image.fromstring(data, (width, height), 'RGBA', False)
            Image.save(surf,r"../graphics/results/hill_"+str(z)+"_u.png")

        Image.save(background_final,r"../graphics/results/all_hill.png")
        pickle.dump( self.matrice, open( r"../graphics/results/"+self.pkl_name.split('/')[-1], "wb" ) )
        
    def crea_montagne_perlin(self,num): #processo (lento) di creazione mappe con PerlinNoise
        print "[WORLD MAKER]: generation of perlin_maps\t"
        for k in xrange(num):
            print "%3.2f %%" % (float(k*100.0/num)),"\r",
            matr = []
            P = PerlinNoise()
            matr = P.run(W_WORLD, H_WORLD, 0.25,[0.065,0.125,0.25,0.5,0.7,1,1.6,1.8,2],D_WORLD+randint(-2,2))
            t = ''
            for i in range(W_WORLD):
                for j in range(H_WORLD):
                    t += str(matr[i+j*W_WORLD]).ljust(2,' ')+ ' '
                t += '\n'
                
            with open(r"lib_grows/perlin_maps/collina"+str(k)+".txt","w") as out:
                out.write(t)

    def start(self):# start Thread
        print self.name + ": start"
        self.genera_montagna(W_WORLD,H_WORLD)
        self.genera_immagini_chunk()
        return self.matrice
        
    def __del__(self):
        print self.name + ": complete creation\t"
        
