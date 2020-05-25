import tkinter as tk
from tkinter import messagebox
import random
import time
import numpy as np

###############################################################################
# création de la fenetre principale  - ne pas toucher

winner = 0
player = 1
score_ia = 0
score_humain = 0

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
  

###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 
def ResetGame(winner) :
    global player
    global score_humain
    global score_ia
    player = 1
    if winner == 1 :
        score_humain += 1
    elif winner == 2 : 
        score_ia += 1
	#else match nul donc pas de score en plus
    for i in range(0,3):
        for j in range(0,3):
            Grille[i][j] = 0

def Play(x,y,z):             
    if Grille[x][y] == 0:
        Grille[x][y] = z
        return True
    return False
  
def MatchNul():
    for i in range(0,3):
        for j in range(0,3):
            if (Grille[i][j] == 0):
                return False
    return True

def Victoire(): #On regarde si le joueur a gagné
    for i in range (0,3):
		#Lignes
        if (Grille[i][0] != 0 and Grille[i][0] == Grille[i][1] and Grille[i][1] == Grille[i][2]):
            return Grille[i][0]

		#Colonnes 
        if (Grille[0][i] != 0 and Grille[0][i] == Grille[1][i] and Grille[1][i] == Grille[2][i]):
            return Grille[0][i]

	#Diagonales
    if (Grille[0][0] != 0 and Grille[0][0] == Grille[1][1] and Grille[1][1] == Grille[2][2]):
        return Grille[0][0]

    if (Grille[2][0] != 0 and Grille[0][2] == Grille[1][1] and Grille[1][1] == Grille[2][0]):
        return Grille[0][2]
	
    return 0
          
    
################################################################################
#    
# Dessine la grille de jeu

def Dessine(winner):
    ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")
    color = "blue"
    if (winner == 1) :
        color = "red"
    if (winner == 2) :
        color = "yellow"

    for i in range(4):
        canvas.create_line(i*100,0,i*100,300,fill=color, width="4" )
        canvas.create_line(0,i*100,300,i*100,fill=color, width="4" )
        
    for x in range(3):
        for y in range(3):
            xc = x * 100 
            yc = y * 100 
            if ( Grille[x][y] == 1):
                canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
            if ( Grille[x][y] == 2):
                canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )

    canvas.create_text(LARG-30, 20, text="IA : "+str(score_ia), fill="white", font="Arial")
    canvas.create_text(30, 20, text="You : "+str(score_humain), fill="white", font="Arial")
        
       
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def newPlayer():
    """cette fonction change le joueur"""
    global player
    if player == 1:
        player = 2
    else:
        player = 1

def getCaseDisp():
    """retourne toutes les cases disponibles"""
    liste = []
    for i in range(3):
        for j in range(3):
            if Grille[i][j] == 0:
                liste.append([i,j])
    return liste

def thisIsIA():
    """cette fonction fait jouer l'IA"""
    global player
    cases_disp = getCaseDisp()
    ia_choice = random.randint(0,len(cases_disp)-1)
    # choice = cases_disp[ia_choice] # pour aleatoire
    choice = simulaIA()[0] #min max implementation
    #print(choice)
    Play(choice[0],choice[1],player)
    newPlayer()
    winner = Victoire() # on stock le resultat actuel 
    if (winner or MatchNul()):
        Dessine(winner) #on dessine
        Window.update() # maj de la fenetre avant la fin du tour de tkinter
        Window.after(3000) # pause de 3secondes
        ResetGame(winner) #on met les cases a 0
        Dessine(winner) # on dessine la couleur du gagnant
        return
    Dessine(winner) # on dessine le jeu

def simulaIA():
    """simulation pour l'ia en cherchant toujours la meilleur solution"""
    winner = Victoire()
    if winner == 2:
        return 1
    elif winner == 1:
        return -1
    if MatchNul():
        return 0
    cases_disp = getCaseDisp()
    result = []
    for couple in cases_disp:
        Play(couple[0],couple[1],2)
        value = simulaPLY()
        if type(value) is not int:
            value = value[1]
        result.append([couple,value])
        Grille[couple[0]][couple[1]] = 0
    return maxi(result)
    
    
def simulaPLY():
    """simulation pour le joueur en cherchant la pire solution"""
    winner = Victoire()
    if winner == 2:
        return 1
    elif winner == 1:
        return -1
    if MatchNul():
        return 0
    cases_disp = getCaseDisp()
    result = []
    for couple in cases_disp:
        Play(couple[0],couple[1],1)
        value = simulaIA()
        if type(value) is not int:
            value = value[1]
        result.append([couple,value])
        Grille[couple[0]][couple[1]] = 0
    return mini(result)

def maxi(liste):
    """fonction maximum pour une coordonée et une valeur"""
    max = -2
    coord = [0,0]
    for elt in liste:
        if elt[1] >= max:
            max = elt[1]
            coord = elt[0]
    return [coord,max] 

def mini(liste):
    """fonction minimum pour une coordonée et une valeur"""
    min = 2
    coord = [0,0]
    for elt in liste:
        if elt[1] < min:
            min = elt[1]
            coord = elt[0]
    return [coord,min] 
    
def MouseClick(event):
    """fonction lance quand on clic"""
    global player
    global winner
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    print("clicked at", x,y)
    hasPlay = Play(x,y,player)  # on regarde si le joueur a jouer correctement
    if hasPlay:
        newPlayer() # dans ce cas là on change de joueur 
    winner = Victoire()
    if (winner or MatchNul()):
        Dessine(winner)
        Window.update()
        Window.after(3000)
        ResetGame(winner)
        Dessine(winner)
        return
    Dessine(winner)
    if hasPlay: # si le joueur a bien joué, alors c'est au tour de l'ia
        Window.update()
        Window.after(3000)
        thisIsIA()

canvas.bind('<ButtonPress-1>',  MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine(winner)
Window.mainloop()


  


    
        

      
 

