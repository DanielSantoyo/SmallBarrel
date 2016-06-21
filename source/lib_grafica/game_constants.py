####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
from math import sqrt
W = 640
H = 480
DIMCHAR = 20
FPS = 30

BLOCCOX = 36
BLOCCOY = 43
DZ = 21#DZ = BLOCCOY/2.0
DX = 18#DX = BLOCCOX/2.0
DY = 10.75#DY = DZ/2.0
T_ERBA  = '0'
T_ACQUA = '1'
T_SABBIA = '2'
T_TERRA = '3'
T_NEVE = '4'
T_LAVA = '5'

EVENT = 'E'
T_UP = '^'
T_DOWN = 'v'
T_VOID = '@'
T_HIDE = 'X'
Z_SEA = 2
Z_SNOW = 13

NUM_MINERS = 3
MINER_WIDTH  = 36
MINER_HEIGHT = 36
W_WORLD,H_WORLD,D_WORLD = 20, 20, 10
Y_OFFSET = H-DY*(2*H_WORLD + 2) + DZ - DY#;print "YOFFSET", Y_OFFSET
TRANSPARENCY = (123,123,123)
DIAGONAL = sqrt(DX*DX+DY*DY)
SQRT3 = sqrt(3)
MOUSE_TH = 20
FREE = ' '
def walkable(x):
    if x == T_ERBA:
        return True
    if x == T_SABBIA:
        return True
    if x == T_NEVE:
        return True
    return False
    
