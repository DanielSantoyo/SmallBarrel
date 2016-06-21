#!/usr/bin/python
####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
header = '''\
#######################################
#                                     #
#     SMALLBARREL MINERS              #
#                                     #
#######################################'''
import time
import sys
import main_input
import master
from lib_grafica.game_constants import *
DEBUG = 0

def main():
    print header
    print "Starting [MAIN]"
    tasti = main_input.InputHandler('[INPUT]')
    Master = master.Master('[MASTER]',DEBUG)
    Master.start()# Thread
    tasti.zlimit = Master.grafica.zlimit
    tasti.zlimitMax = tasti.zlimit
    
    while tasti.running: # main game loop
        tasti.run()
        Master.grafica.offsetx = tasti.screen_x
        Master.grafica.offsety = tasti.screen_y
        Master.grafica.zlimit = tasti.zlimit
        
    print "END [MAIN]"
    Master.running = False
    sys.exit()
if __name__ == '__main__':
    main()
