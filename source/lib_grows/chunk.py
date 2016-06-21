####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
from lib_grafica.game_constants import *

class Chunk():

    def __init__(self, id):
        self.id = id
        self.matrice = None#{}
        self.keys_actives = [] #chiavi delle matrici attive????
        self.DEPTH  = 0
        self.HEIGHT = 0
        self.WIDTH  = 0

    def __repr__(self):
        t = "CHUNK\n"
        t += "\t"+str(self.id)+'\n'
        t += "\tpiani_matrice: "+str(len(self.matrice))+'\n'
        t += "\ttipo: "+ str(self.tipo)
        
        for y in xrange(H_WORLD):
            for x in xrange(W_WORLD):
                t += self.matrice[0][y][x]
            t += '\n'
        return t
        
    def carica_matrice(self,matrice_pkl):
        self.matrice = matrice_pkl
        dimz = len(matrice_pkl)
        dimy = len(matrice_pkl[0])
        dimx = len(matrice_pkl[0][0])
        for z in xrange(dimz):
            for y in xrange(dimy):
                for x in xrange(dimx):
                    if walkable(self.matrice[z][y][x][0]):
                        self.matrice[z][y][x] = FREE
