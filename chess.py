#TODO
# Yalnızca vezire terfi yapılabiliyor.
# Oyun bitmiyor.
#Pat olmuyor

import pygame
from pygame.locals import *
import requests
import itertools

pygame.init()
background_color=(52, 110, 235)
warning_color=(255, 0, 0)
stockfish_color=(0, 255, 0)
highlight_color=(0,50,0)
white_square_color=(255,255,255)
black_square_color=(3, 23, 245)
notation_text_color=(255,0,0)
notation_text_font = pygame.font.SysFont('Comic Sans MS', 20)
notation_number_font = pygame.font.SysFont('Comic Sans MS', 20)
font_reset = pygame.font.SysFont('Comic Sans MS', 20)
warning_font = pygame.font.SysFont('Comic Sans MS', 30)



castle_white=[False,False,False,0]
castle_black=[False,False,False,0]
notations='abcdefgh'
castled=0
fenn=''
stockfish_on=False
stockfish_moves=[]
sirra=0
s=""
winner=0
logs=[]
ean=0
warning=''
tahta=[
["w","b","w","b","w","b","w","b"],
["b","w","b","w","b","w","b","w"],
["w","b","w","b","w","b","w","b"],
["b","w","b","w","b","w","b","w"],
["w","b","w","b","w","b","w","b"],
["b","w","b","w","b","w","b","w"],
["w","b","w","b","w","b","w","b"],
["b","w","b","w","b","w","b","w"],
]
taslar=[
    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]
tahta2=[
    ["a8","b8","c8","d8","e8","f8","g8","h8"],
    ["a7","b7","c7","d7","e7","f7","g7","h7"],
    ["a6","b6","c6","d6","e6","f6","g6","h6"],
    ["a5","b5","c5","d5","e5","f5","g5","h5"],
    ["a4","b4","c4","d4","e4","f4","g4","h4"],
    ["a3","b3","c3","d3","e3","f3","g3","h3"],
    ["a2","b2","c2","d2","e2","f2","g2","h2"],
    ["a1","b1","c1","d1","e1","f1","g1","h1"]
]

def legal(kaynak, hedef,i,j,i_hedef,j_hedef):
    global ean
    if taslar[i][j][1]=='K':## sahin hamleleri
        legal_hamleler_sah=["No"]
        if i!=0:
            if taslar[i-1][j][0]!=taslar[i][j][0]:
                legal_hamleler_sah.append(tahta2[i-1][j])
            if taslar[i-1][j-1][0]!=taslar[i][j][0]:
                if j!=0:
                    legal_hamleler_sah.append(tahta2[i-1][j-1])
            if taslar[i-1][j+1][0]!=taslar[i][j][0]:
                if j!=7:
                    legal_hamleler_sah.append(tahta2[i-1][j+1])
        if i!=7:
            if taslar[i+1][j][0]!=taslar[i][j][0]:
                legal_hamleler_sah.append(tahta2[i+1][j])
            if taslar[i+1][j-1][0]!=taslar[i][j][0]:
                if j!=0:
                    legal_hamleler_sah.append(tahta2[i+1][j-1])
            if taslar[i+1][j+1][0]!=taslar[i][j][0]:
                if j!=7:
                    legal_hamleler_sah.append(tahta2[i+1][j+1])
        if j!=0:
            if taslar[i][j-1][0]!=taslar[i][j][0]:
                legal_hamleler_sah.append(tahta2[i][j-1])
        if j!=7:
            if taslar[i][j+1][0]!=taslar[i][j][0]:
                legal_hamleler_sah.append(tahta2[i][j+1])
        




        if taslar[i][j][0]=='w':#castle
            if not castle_white[0]:
                if not castle_white[1]:
                    if taslar[7][5]=='--' and taslar[7][6]=='--':
                            legal_hamleler_sah.append(tahta2[7][6])
                if not castle_white[2]:
                    if taslar[7][1]=='--' and taslar[7][2]=='--' and taslar[7][3]=='--':
                        legal_hamleler_sah.append(tahta2[7][2])
        if taslar[i][j][0]=='b':
            if not castle_black[0]:
                if not castle_black[1]:
                    if taslar[0][5]=='--' and taslar[0][6]=='--':
                        legal_hamleler_sah.append(tahta2[0][6])
                if not castle_black[2]:
                    if taslar[0][1]=='--' and taslar[0][2]=='--' and taslar[0][3]=='--':
                        legal_hamleler_sah.append(tahta2[0][2])
        return legal_hamleler_sah
            
            
    if taslar[i][j]=='wp':
        beyaz_piyon_hamleleri=["No"]
        ##en passant
        if len(logs)!=0:
            if j==0:#en passant
                if logs[-1][0]==tahta2[i-2][j+1]:
                    if logs[-1][1]==tahta2[i][j+1]:
                        beyaz_piyon_hamleleri.append(tahta2[i-1][j+1])
                        ean=1
            if j==7:
                if logs[-1][0]==tahta2[i-2][j-1]: 
                    if logs[-1][1]==tahta2[i][j-1]:
                        beyaz_piyon_hamleleri.append(tahta2[i-1][j-1])
                        ean=1
            else:
                if logs[-1][0]==tahta2[i-2][j+1]:
                    if logs[-1][1]==tahta2[i][j+1]:
                        beyaz_piyon_hamleleri.append(tahta2[i-1][j+1])
                        ean=1          
                if logs[-1][0]==tahta2[i-2][j-1]:
                    if logs[-1][1]==tahta2[i][j-1]:
                        beyaz_piyon_hamleleri.append(tahta2[i-1][j-1])
                        ean=1 
        if i==6 and taslar[5][j]=='--' and taslar[4][j]=='--':
                beyaz_piyon_hamleleri.append(tahta2[i-2][j])
        if j!=7 and i!=0:
            if taslar[i-1][j+1][0]=='b':
                beyaz_piyon_hamleleri.append(tahta2[i-1][j+1])
        if i!=0 and j!=0:
            if taslar[i-1][j-1][0]=='b':
                beyaz_piyon_hamleleri.append(tahta2[i-1][j-1])
        if i!=0:
            if taslar[i-1][j]=='--':
                beyaz_piyon_hamleleri.append(tahta2[i-1][j])
        return beyaz_piyon_hamleleri
    if taslar[i][j]=='bp':
        siyah_piyon_hamleleri=["No"]
        if len(logs)!=0:
            if j==0:##enpassant
                if logs[-1][0]==tahta2[i+2][j+1]:
                    if logs[-1][1]==tahta2[i][j+1]:
                        siyah_piyon_hamleleri.append(tahta2[i+1][j+1])
                        ean=1
            if j==7:
                if logs[-1][0]==tahta2[i+2][j-1]: ##burda
                    if logs[-1][1]==tahta2[i][j-1]:
                        siyah_piyon_hamleleri.append(tahta2[i+1][j-1])
                        ean=1
            else:
                if logs[-1][0]==tahta2[i+2][j+1]:
                    if logs[-1][1]==tahta2[i][j+1]:
                        siyah_piyon_hamleleri.append(tahta2[i+1][j+1])
                        ean=1          
                if logs[-1][0]==tahta2[i+2][j-1]:
                    if logs[-1][1]==tahta2[i][j-1]:
                        siyah_piyon_hamleleri.append(tahta2[i+1][j-1])
                        ean=1

        if i==1 and taslar[2][j]=='--' and taslar[3][j]=='--':
            siyah_piyon_hamleleri.append(tahta2[i+2][j])
        if j!=0 and i!=7:
            if taslar[i+1][j-1][0]=='w':
                siyah_piyon_hamleleri.append(tahta2[i+1][j-1])
        if i!=7 and j!=7:
            if taslar[i+1][j+1][0]=='w':
                siyah_piyon_hamleleri.append(tahta2[i+1][j+1])
        if i!=7:
            if taslar[i+1][j]=='--':
                siyah_piyon_hamleleri.append(tahta2[i+1][j])
        return siyah_piyon_hamleleri
    
    if taslar[i][j][1]=='N':##atin hamleleri
        legal_hamleler_at1=["No"]
        legal_hamleler_at=list(itertools.permutations(['1','2','-1','-2'], 2))
        legal_hamleler_at.pop(10)
        legal_hamleler_at.pop(6)
        legal_hamleler_at.pop(5)
        legal_hamleler_at.pop(1)
        for a in range(0,len(legal_hamleler_at)):
            bir=i+int(legal_hamleler_at[a][0])
            iki=j+int(legal_hamleler_at[a][1])
            if bir<=7:
                if bir>=0:
                    if iki <=7:
                        if iki>=0:
                            if tahta2[bir][iki]!='--':
                                if taslar[bir][iki][0]!=taslar[i][j][0]:
                                    legal_hamleler_at1.append(tahta2[bir][iki])
                            else:
                                if taslar[bir][iki][0]!=taslar[i][j][0]:
                                    legal_hamleler_at1.append(tahta2[bir][iki])
        return legal_hamleler_at1
    
    
    if taslar[i][j][1]=='B':##filin hamleleri
        legal_hamleler_fil=["No"]
        x=i
        y=j
        while x>0 and y >0:
            x=x-1
            y=y-1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])
        x=i
        y=j
        while x <=6 and y<=6:
            x=x+1
            y=y+1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])

        x=i
        y=j        
        while x <=6 and y>0:
            x=x+1
            y=y-1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])

        x=i
        y=j
        while x >0 and y<=6:
            x=x-1
            y=y+1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])
        return legal_hamleler_fil



    if taslar[i][j][1]=='R':##kale
        legal_hamleler_kale=["No"]
        for a in range(i+1,8):
            if taslar[a][j]!='--':
                if taslar[a][j][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[a][j])
                break
            legal_hamleler_kale.append(tahta2[a][j])
        for a in range(i-1,-1,-1):
            if taslar[a][j]!='--':
                if taslar[a][j][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[a][j])
                break
            legal_hamleler_kale.append(tahta2[a][j])
        for a in range(j-1,-1,-1):
            if taslar[i][a]!='--':
                if taslar[i][a][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[i][a])
                break
            legal_hamleler_kale.append(tahta2[i][a])
        for a in range(j+1,8):
            if taslar[i][a]!='--':
                if taslar[i][a][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[i][a])
                break
            legal_hamleler_kale.append(tahta2[i][a])
        return legal_hamleler_kale
    
    
    
    
    
    
    
    
    
    
    if taslar[i][j][1]=='Q':#vezirin hamleler
        legal_hamleler_vezir=["No"]
        legal_hamleler_fil=[]
        legal_hamleler_kale=[]
        for a in range(i+1,8):
            if taslar[a][j]!='--':
                if taslar[a][j][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[a][j])
                break
            legal_hamleler_kale.append(tahta2[a][j])
        for a in range(i-1,-1,-1):
            if taslar[a][j]!='--':
                if taslar[a][j][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[a][j])
                break
            legal_hamleler_kale.append(tahta2[a][j])
        for a in range(j-1,-1,-1):
            if taslar[i][a]!='--':
                if taslar[i][a][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[i][a])
                break
            legal_hamleler_kale.append(tahta2[i][a])
        for a in range(j+1,8):
            if taslar[i][a]!='--':
                if taslar[i][a][0]!=taslar[i][j][0]:
                    legal_hamleler_kale.append(tahta2[i][a])
                break
            legal_hamleler_kale.append(tahta2[i][a])
        #fil
        legal_hamleler_fil=["No"]
        x=i
        y=j
        while x>0 and y >0:
            x=x-1
            y=y-1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])
        x=i
        y=j
        while x <=6 and y<=6:
            x=x+1
            y=y+1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])

        x=i
        y=j        
        while x <=6 and y>0:
            x=x+1
            y=y-1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])

        x=i
        y=j
        while x >0 and y<=6:
            x=x-1
            y=y+1
            if taslar[x][y]!='--':
                if taslar[x][y][0]!=taslar[i][j][0]:
                    legal_hamleler_fil.append(tahta2[x][y])
                break
            legal_hamleler_fil.append(tahta2[x][y])
        legal_hamleler_vezir=legal_hamleler_vezir +legal_hamleler_fil+ legal_hamleler_kale
        return legal_hamleler_vezir







def highlight():
    for a in range(0,len(tahta2)):
        for b in range(0,len(tahta2[a])):
            if tahta2[a][b] in legal(0,0,i,j,0,0):
                tahta[a][b]=tahta[a][b]+'G'
def unhighlight():
    for a in range(0,len(tahta)):
        for b in range(0,len(tahta[a])):
            if 'G' in tahta[a][b]:
                ind=tahta[a][b].index('G')
                tahta[a][b]=tahta[a][b][:ind]+ tahta[a][b][ind+1:]



def hamle(kaynak, hedef):
    global winner
    global ean
    global warning
    i=abs(int(kaynak[1])-8)
    i_hedef=abs(int(hedef[1])-8)
    j=0
    j_hedef=0
    for a in range(len(tahta2)):
        for b in range(len(tahta2[a])):
            if tahta2[a][b]==hedef:
                j_hedef=b
            if tahta2[a][b]==kaynak:
                j=b
    if taslar[i][j][0]==taslar[i_hedef][j_hedef][0]:
        warning='Illegal Move'
        return 1
    ##kaynak bos mu
    
    if(taslar[i][j])!='--':
        legal_hamleler_toplam=legal(kaynak,hedef,i,j,i_hedef,j_hedef)
        if len(legal_hamleler_toplam)!=0:
            if tahta2[i_hedef][j_hedef] not in legal_hamleler_toplam:
                warning='Illegal'
                return 'illegal'  
            if tahta2[i_hedef][j_hedef] in legal_hamleler_toplam:
                if ean:
                    if taslar[i][j][1]=='p':
                        if j+1==j_hedef:
                            taslar[i][j+1]='--'
                        if j-1==j_hedef:
                            taslar[i][j-1]='--'                   
                if taslar[i_hedef][j_hedef]!='--':
                    logs.append([tahta2[i][j],tahta2[i_hedef][j_hedef],i,j,i_hedef,j_hedef,'x',taslar[i_hedef][j_hedef]])
                else:
                    if ean:
                        logs.append([tahta2[i][j],tahta2[i_hedef][j_hedef],i,j,i_hedef,j_hedef,'e',taslar[i_hedef][j_hedef]])
                    else:
                        logs.append([tahta2[i][j],tahta2[i_hedef][j_hedef],i,j,i_hedef,j_hedef])
                taslar[i_hedef][j_hedef]=taslar[i][j][0]+taslar[i][j][1]
                taslar[i_hedef][j_hedef]=taslar[i][j]
                taslar[i][j]='--'
                if ean:
                    if taslar[i][j][0]=='w':
                        if j+1==j_hedef:
                            taslar[i][j]=='--'
                            ean=0
                for k in range(0,8):
                    for l in range(0,8):
                        if taslar[k][l]=='wK':
                            if tahta2[k][l] in legal_hamleler_toplam:
                                winner=2
                        if taslar[k][l]=='bK':
                            if tahta2[k][l] in legal_hamleler_toplam:
                                winner=1

#pygame.init()
window = pygame.display.set_mode((1200,1000),pygame.RESIZABLE)
button = pygame.image.load(r"./images/stockfish_button.png")
button1 = pygame.transform. scale(button, (50,50))
button2=pygame.image.load(r"./images/undo.png")
button3=pygame.transform. scale(button2, (50,50))
#font_reset = pygame.font.SysFont('Comic Sans MS', 20)
reset_text = font_reset.render('reset', False, (235, 70, 52))
window.blit(button1, (1100,300))
window.blit(button3, (1100,400))




def tahta_yukle():
    for x in range(0,8):##tahta arkplani
        for y in range(0,8):
            s=notations[y]
            if tahta[x][y] == "b":
                pygame.draw.rect(window,black_square_color,((y*100)+100,(x*100)+100,100,100))
            if tahta[x][y] == "w":
                pygame.draw.rect(window,white_square_color,((y*100)+100,(x*100)+100,100,100))
            if 'G' in tahta[x][y]:
                pygame.draw.rect(window,highlight_color,((y*100)+100,(x*100)+100,100,100))

            if y==7:
                for z in range(0,8):
                    #notation_number_font = pygame.font.SysFont('Comic Sans MS', 20)
                    text_surface2 = notation_number_font.render(notations[z], False, notation_text_color)
                    window.blit(text_surface2, ((z*100)+180,875))
        #notation_text_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = notation_text_font.render(str(8-(x)), False, notation_text_color)
        window.blit(text_surface, ((100),(x*100)+150))



count=1
sirra=0
i=0
j=0
def on_click(x,y):##mouse input
    global count
    global sirra
    global i
    global j
    global winner
    global warning
    global castle_white, castle_black
    i_hedef=0
    j_hedef=0
    if count%2!=0:
        j=lokasyon(x)
        i=lokasyon(y)
        count+=1
        highlight()
        warning=''
        return
    if count %2==0 and count>1:#second click
        unhighlight()
        if sirra%2==0 and taslar[i][j][0]!='w':
            warning="White's turn!"
            i=0
            j=0
            count=1
            return 
        if sirra%2!=0 and taslar[i][j][0]!='b':
            warning="Black's turn!"
            i=0
            j=0
            count=1
            return
        count+=1
        i_hedef=lokasyon(y)#
        j_hedef=lokasyon(x)#
        if taslar[i][j]=='wp' and taslar[i_hedef][j_hedef][0]=='b':
            if i_hedef==0:
                taslar[i_hedef][j_hedef]='wQ'
                taslar[i][j]='--'
                return
        if taslar[i][j]=='bp' and taslar[i_hedef][j_hedef]=='b':
            if i_hedef==7:
                taslar[i_hedef][j_hedef]='bQ'
                taslar[i][j]='--'
                return
        
        if hamle(tahta2[i][j],tahta2[i_hedef][j_hedef])=='illegal':
            warning="Illegal Move!"
            i=0
            j=0
            return
        if taslar[i][j][0]==taslar[i_hedef][j_hedef][0]:
            warning='Illegal Move! Cant eat own piece!'#
            return 1

        hamle(tahta2[i][j],tahta2[i_hedef][j_hedef])##castle problem
        if taslar[7][4]!='wK':
            castle_white[0]=True
        if taslar[7][0]!='wR':
            castle_white[2]==True
        if taslar[7][7]!='wK': 
            castle_white[1]==True 
        if taslar[0][4]!='bK':
            castle_black[0]=True
        if taslar[0][0]!='bR':
            castle_black[2]==True
        if taslar[0][7]!='bK': 
            castle_black[1]==True  
        if i==7 and j==4:   
            if i_hedef==7:
                if j_hedef==6:
                    taslar[7][5]='wR'
                    taslar[7][7]='--' 
                    castle_white[3]=1 
                if j_hedef==2:
                    taslar[7][3]='wR'
                    taslar[7][0]='--'
                    castle_white[3]=1 
        if i==0 and j==4:   
            if i_hedef==0:
                if j_hedef==6:
                    taslar[0][5]='bR'
                    taslar[0][7]='--'  
                    castle_black[3]=1 
                if j_hedef==2:
                    taslar[0][3]='bR'
                    taslar[0][0]='--'
                    castle_black[3]=1 
        
        
        #hamle(tahta2[i][j],tahta2[i_hedef][j_hedef])     

        i_hedef=0
        j_hedef=0
        i=0
        j=0
        sirra+=1 
        warning=''
        if stockfish_on:
            stockfish()

        return
def lokasyon(a):

    if a<200:
        return 0
    if a<300:
        return 1
    if a<400:
        return 2
    if a<500:
        return 3    
    if a<600:
        return 4
    if a<700:
        return 5
    if a<800:
        return 6
    if a<900:
        return 7
def reset():
    global sirra, winner, logs, ean, warning, taslar, castle_black,castle_white
    castle_white=[False,False,False]
    castle_black=[False,False,False]
    sirra=0
    winner=0
    logs=[]
    ean=0
    warning=''
    taslar=[
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bp","bp","bp","bp","bp","bp","bp","bp"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["wp","wp","wp","wp","wp","wp","wp","wp"],
        ["wR","wN","wB","wQ","wK","wB","wN","wR"]
    ]
def undo():
    global sirra, warning,ean
    if len(logs)<=0:
        warning='It is the first move'
        return 
    i,j,i_hedef,j_hedef=logs[-1][2],logs[-1][3],logs[-1][4],logs[-1][5]
    taslar[i][j]=taslar[i_hedef][j_hedef]
    if castle_white[3]==1:
        taslar[7][4]='wK'
        if logs[-1][5]==6:
            taslar[7][6]='--'
            taslar[7][5]='--'
            taslar[7][7]='wR'
        if logs[-1][5]==3:
            taslar[7][0]='wR'
            taslar[7][1]='--'
            taslar[7][2]='--'
            taslar[7][3]='--'
    if castle_black[3]==1:
        taslar[7][4]='bK'
        if logs[-1][5]==6:
            taslar[0][7]='bR'
            taslar[0][6]='--'
            taslar[0][5]='--'
        if logs[-1][5]==3:
            taslar[0][0]='bR'
            taslar[0][1]='--'
            taslar[0][2]='--'
            taslar[0][3]='--'

    if ean:
        if logs[-1][2]>logs[-1][4]:#white's enpassant
            if logs[-1][3]>logs[-1][5]:
                taslar[logs[-1][2]][logs[-1][3]-1]='bp'
            if logs[-1][3]<logs[-1][5]:
                taslar[logs[-1][2]][logs[-1][3]+1]='bp'
        if logs[-1][2]<logs[-1][4]:#black's enpassant
            if logs[-1][3]>logs[-1][5]:
                taslar[logs[-1][2]][logs[-1][3]-1]='wp'
            if logs[-1][3]<logs[-1][5]:
                taslar[logs[-1][2]][logs[-1][3]+1]='wp'
    if 'x' in logs[-1]:
        taslar[i_hedef][j_hedef]=logs[-1][-1]
    else:
        taslar[i_hedef][j_hedef]='--'
    sirra+=1

    logs.pop()
def stockfish():
    global stockfish_on, stockfish_moves,s
    url="https://www.chessdb.cn/cdb.php?action=querypv&board="+ to_fen() +"&json=1"  
    eval=requests.get(url)
    data=eval.json()
    if stockfish_on:
        stockfish_moves=data['pvSAN']
        s=','.join(stockfish_moves[:6])
    return data['pvSAN']##bilgisayarın en iyi hamlesi

def draw(drw):##useless function
    frm=''
    dest=''
    for i in range(0,8):
        for j in range(0,8):
            if tahta2[i][j]==drw[:2]:
                frm+=str(i+2)
                frm+=str(j+2)
            if tahta2[i][j]==drw[2:]:
                dest+=str(i+2)
                dest+=str(j+2)
    pygame.draw.polygon(window, (0, 0, 0), ((0, 100), (0, 100), (200, 200), (200, 220), (200, 250), (200,200), (200, 150)))
    return frm,dest

def to_fen():
    turned_to_fen=''
    count=0
    for a in range(0,8):
        for b in range(0,8):
            if taslar[a][b]=="--":
                count+=1
                if b==7:
                    turned_to_fen+=str(count)
                    count=0
                    break
                else:
                    if b<7:
                        if taslar[a][b+1]!='--':
                            turned_to_fen+=str(count)
                            count=0
            
            if taslar[a][b][0]=='b':
                turned_to_fen+=(taslar[a][b][1].lower())
            if taslar[a][b][0]=='w':
                turned_to_fen+=(taslar[a][b][1].upper())
        turned_to_fen+='/'
    if sirra%2==0:
        turned_to_fen+=' w '
    if sirra%2!=0:
        turned_to_fen+=' b '
    if not castle_white[0] and not castle_white[1]:
        turned_to_fen+='K'
    if not castle_white[0] and not castle_white[2]:
        turned_to_fen+='Q'
    if not castle_black[0] and not castle_black[1]:
        turned_to_fen+='k'
    if not castle_black[0] and not castle_black[2]:
        turned_to_fen+='q'
    if len(logs)!=0 :
        turned_to_fen+=' '+logs[-1][1] 
    turned_to_fen+=' 0 0' 
    return turned_to_fen      
def loc():
    pygame.draw.rect(window,(47,79,79),((1097,505,55,20)))
    window.blit(button1, (1100,300))
    window.blit(button3, (1100,400))
    window.blit(reset_text, (1100,500))
    for i in range(0,len(taslar)):
        for j in range(0,len(taslar)):
            if taslar[i][j]!="--":
                image = pygame.image.load(r"./images/"+ taslar[i][j]+ ".png")## load every image in taslar[]
                image = pygame.transform. scale(image, (100,100))
                window.blit(image, (((j)*100)+100,((i)*100)+100))

while True:
    window.fill(background_color)
    tahta_yukle()
    loc()
    #warning_font = pygame.font.SysFont('Comic Sans MS', 30)
    stock_text = warning_font.render(s, False, stockfish_color)
    warning_text = warning_font.render(warning, False, warning_color)
    window.blit(warning_text, (900,150))
    if stockfish_on:
        window.blit(stock_text, (100,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type== MOUSEBUTTONDOWN:
            mouse=pygame.mouse.get_pos()
            if mouse[0]<=900 and mouse[1]<=900:
                sx,sy= pygame.mouse.get_pos()#get the click positions
                sx-= sx % 100
                sy-=sy%100
                on_click(sx,sy)
            if mouse[0]<=1150:
                if mouse[0]>=1100:
                    if mouse[1]<=350:
                        if mouse[1]>=300:
                            stockfish_on= not stockfish_on
                            if stockfish_on:
                                warning='Stockfish on'
                            else:
                                warning='Stockfish off'
                            stockfish()
            if mouse[0]<=1150:
                if mouse[0]>=1100:
                    if mouse[1]<=450:
                        if mouse[1]>=400:
                            undo()
                            warning='Undone'
            if mouse[0]<=1097+55:
                if mouse[0]>=1097:
                    if mouse[1]<=505+20:
                        if mouse[1]>=505:
                            reset()
                            warning='Reset'
            
            
        
        

    pygame.display.flip()