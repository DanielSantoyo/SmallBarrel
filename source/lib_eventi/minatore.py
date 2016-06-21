####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
import evento
from time import sleep
from random import choice
from random import randint
from lib_grafica.game_constants import *
import sys, traceback

IDLE = 0

class Miner(evento.Event):

    def __init__(self, nome='', indice=0):
        evento.Event.__init__(self,indice)
        self.nome = nome
        self.sesso = choice(['M','F'])
        self.eta = 0
        self.vitalita = 0
        self.salute = 0
        self.forza = 0
        self.intelligenza = 0
        self.saggezza = 0
        self.carisma = 0
        #bisogni
        self.sonno = 0
        self.fame = 0
        ##self.sete = 0
        self.noia = 0
        self.solitudine = 0
        self.vizio = 0
        self.ferito = 0
        self.STATO = IDLE
        #psicologia
        self.umilta = 0
        self.compassione = 0
        self.carattere = 0
        #societa'
        self.ricchezza = 0
        self.rispetto = 0
        self.professione = ''
        self.cognome = ''
        self.generazione = 1
        self.abilita = []#livelli di professione
        #esterno -- OVERRIDE --???
        self.indice = indice
        self.grafica = "miner"
        self.sprite_width = MINER_WIDTH
        #abilita'
        
    def __repr__(self):
        t = ''
        t += self.nome+' '+self.cognome+'\n'
        t += self.sesso+'\n'
        t += 'eta:'+str(self.eta)+'\n'
        t += 'vit:'+str(self.vitalita)+'\n'
        t += 'for:'+str(self.forza)+'\n'
        t += 'int:'+str(self.intelligenza)+'\n'
        t += 'sag:'+str(self.saggezza)+'\n'
        t += 'car:'+str(self.carisma)+'\n'
        t += 'p-umi:'+str(self.umilta)+'\n'
        t += 'p-com:'+str(self.compassione)+'\n'
        t += 'p-crt:'+str(self.carattere)+'\n'
        return t
   
    def run(self):
        while self.running:
            #gestione movimento evento
            #movimento random...
            try:
                if len(self.path) == 0:
                    verso = randint(0,3)
                    self.try_move_random(self.x, self.y, self.z, verso)
                sleep(self.velocita)
                
            except:
                traceback.print_exc(file=sys.stdout)
                self.running = False
            self.sprite[self.indice].sx = self.x
            self.sprite[self.indice].sy = self.y
            self.sprite[self.indice].sz = self.z
            self.sprite[self.indice].verso = self.verso
    
