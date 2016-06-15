####################################################
#Software License:                                 #
#--------------------------------------------------#
#The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
#contact: daniel.santoyo@gmx.com                   #
####################################################
import random

def nome_random(s):
    if s == 'M':
        mono = '''grum,klum,fil,bil,bum,rik,kru,ka,ra,re,po,yo,gro,glum'''.split(',')
        voc = '''o,i,ur'''.split(',')
    else:
        mono = '''gam,klim,fal,vil,blum,rig,me,ga,na,ne,bo,yen,hi,gun'''.split(',')
        voc = '''a,e,as'''.split(',')
    if random.randint(0,1):
        t = random.choice(mono)+random.choice(voc)+random.choice(mono)*random.randint(0,1)
    else:
        t = random.choice(voc)*random.randint(0,1)+random.choice(mono)+random.choice(voc)
    t = (t[:1]).upper() + t[1:]
    return t

def cognome_random():
    mono = '''tuk,duk,con,mon,lum,gan,mel'''.split(',')
    voc = '''a,e,i,o,u'''.split(',')
    if random.randint(0,1):
        t = random.choice(mono)+random.choice(voc)+random.choice(mono)*random.randint(0,1)
    else:
        t = random.choice(voc)*random.randint(0,1)+random.choice(mono)+random.choice(voc)
    t = (t[:1]).upper() + t[1:]
    return t
