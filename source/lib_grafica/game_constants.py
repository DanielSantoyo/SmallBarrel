####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
#constants values
W = 640
H = 480
DIMCHAR = 20
FPS = 30

BLOCCOX = 36
BLOCCOY = 43
DZ = 21
DX = 18
DY = 10.75
T_ERBA  = '0'
T_ACQUA = '1'
T_VOID = '@'
T_HIDE = 'X'
T_SABBIA = '2'
T_TERRA = '3'
T_NEVE = '4'
T_LAVA = '5'
Z_SEA = 2
Z_SNOW = 13

NUM_DWARFS = 1
DWARF_WIDTH  = 36
DWARF_HEIGHT = 36
W_WORLD,H_WORLD,D_WORLD = 20, 20, 8
Y_OFFSET = H-DY*(2*H_WORLD + 2) + DZ - DY
TRANSPARENCY = (123,123,123)
print "YOFFSET", Y_OFFSET
#W_WORLD,H_WORLD,D_WORLD = 20, 20, 8 
#DZ = BLOCCOY/2.0
#DX = BLOCCOX/2.0
#DY = DZ/2.0

#print DX, DY, DZ
