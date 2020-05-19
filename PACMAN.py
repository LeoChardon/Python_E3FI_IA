import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import copy
 

#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        
        
TBL = np.array(TBL,dtype=np.int32)
TBL = TBL.transpose()  ## ainsi, on peut écrire TBL[x][y]


        
ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
 


###########################################################################################

# création de la fenetre principale  -- NE PAS TOUCHER

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# création de la frame principale stockant plusieurs pages

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
    
    
def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")
PoliceEndText = tkfont.Font(family='Arial', size=50, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
################################################################################
#
# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM

PacManPos = [5,5]

GUM = PlacementsGUM()  

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ]     )         



# variable pour le score

Score = 0
 
 
#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche():
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = "yellow")
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
     
   # texte score
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "Score :" + str(Score), fill ="yellow", font = PoliceTexte)
 
            
#################################################################
##
##  IA RANDOM
# Création de la grille des GUM
Grille = copy.deepcopy(TBL)

# Grilles de distance avec les ghosts
GrilleGhost1 = copy.deepcopy(TBL)
GrilleGhost2 = copy.deepcopy(TBL)
GrilleGhost3 = copy.deepcopy(TBL)
GrilleGhost4 = copy.deepcopy(TBL)

# Grille des distances : valeur minimales des 4 cartes de distance des ghosts
GrilleDist = copy.deepcopy(TBL)


      
def PacManPossibleMove(x,y):
   L = []
   
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
# Fonction des moves possibles lorsque les ghosts sont dans leur maison
def GhostsPossibleMoveIn(x,y):
   L = []
   
   if ( TBL[x  ][y-1] != 1 ): L.append((0,-1))
   if ( TBL[x  ][y+1] != 1 ): L.append((0, 1))
   if ( TBL[x+1][y  ] != 1 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] != 1 ): L.append((-1,0))

   return L

# Fonction des moves possibles lorsque les ghosts ne sont pas dans leur maison
def GhostsPossibleMoveOut(x,y):
   L = []
   
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   
   return L
   
def IA():
   global PacManPos, Ghosts, Grille
   #deplacement Pacman
  
  
   
   left = Grille[PacManPos[0]-1, PacManPos[1]]
   right = Grille[PacManPos[0]+1, PacManPos[1]]
   up = Grille[PacManPos[0], PacManPos[1]+1]
   down = Grille[PacManPos[0], PacManPos[1]-1]
   
   
   # Tuples de direction associés à Choix.
   directions = [ (-1,0), (1,0), (0,1), (0,-1)]
   # Verification des cases avoisinantes avec la grille des distances des fantomes !
   if GrilleDist[PacManPos[0]-1, PacManPos[1]] <= 3:
      left = 100
   if GrilleDist[PacManPos[0]+1, PacManPos[1]] <= 3:
      right = 100
   if GrilleDist[PacManPos[0], PacManPos[1]+1] <= 3:
      up = 100
   if GrilleDist[PacManPos[0], PacManPos[1]-1] <= 3:
      down = 100

   #On regroupe les valeurs des cases avoisinantes 
   choix = [ left, right, up, down]
   

   #if len(choix) == 0:
   #   L = PacManPossibleMove(PacManPos[0], PacManPos[1])
   #   choixRand = random.randrange(len(L))
   #   PacManPos[0] += L[choixRand][0]
   #   PacManPos[1] += L[choixRand][1]
   #else :



   # On prend la case qui a la valeur la plus petite
   move = directions[choix.index(min(choix))]
   
   # Mouvement du Pacman
   PacManPos[0] += move[0]
   PacManPos[1] += move[1]
   
   #deplacement Fantome
   for F in Ghosts:
      if TBL[F[0]][F[1]] == 2 :
         L = GhostsPossibleMoveIn(F[0],F[1])
      else:
         L = GhostsPossibleMoveOut(F[0],F[1])
      
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]

def EatGUM():
   global PacManPos, Score
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if GUM[x][y] == 1 and PacManPos[0] == x and PacManPos[1] == y:
            GUM[x][y] = 0
            Score += 10
##############################
# Travail sur l'IA et la création de la nouvelle Grille


# Initialisation brute des grilles de distance des ghosts
def UpdateGridGhost(Grille, number):
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if TBL[x][y] == 0 or TBL[x][y] == 2 : 
            Grille[x][y] = 100
         if TBL[x][y] == 1 :
            Grille[x][y] = 555
         if number == 1 :
            if (TBL[x][y] == 0 or TBL[x][y] == 2) and Ghosts[0][0]==x and Ghosts[0][1]==y :
               Grille[x][y] = 0
         if number == 2 : 
            if (TBL[x][y] == 0 or TBL[x][y] == 2) and Ghosts[1][0]==x and Ghosts[1][1]==y :
               Grille[x][y] = 0
         if number == 3:
            if (TBL[x][y] == 0 or TBL[x][y] == 2) and Ghosts[2][0]==x and Ghosts[2][1]==y :
               Grille[x][y] = 0
         if number == 4:
            if (TBL[x][y] == 0 or TBL[x][y] == 2) and Ghosts[3][0]==x and Ghosts[3][1]==y :
               Grille[x][y] = 0

def UpdateGridDist(Grille):
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         GrilleDist[x][y] = FourMinimal(GrilleGhost1[x][y], GrilleGhost2[x][y], GrilleGhost3[x][y], GrilleGhost4[x][y])

# initialisation brute de la grille
def UpdateGrid(Grille):
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if TBL[x][y] == 1 or TBL[x][y] == 2:
            Grille[x][y] = 555
         if TBL[x][y] == 0 and GUM[x][y] == 1:
            Grille[x][y] = 0
         if TBL[x][y] == 0 and GUM[x][y] == 0:
            Grille[x][y] = 100
   




# Fonction qui calcule le minimum entre 4 nombres.
def FourMinimal(a,b,c,d):
   min = a
   if b < min : min = b
   if c < min : min = c
   if d < min : min = d
   return min


# Crée un boolean qui correspond à l'état de la grille : mise a jour ou pas.
def UpdatePath(Grille, type, number):
   if type == 'Ghost':
      if number == 1:
         UpdateGridGhost(Grille, 1)
      if number == 2:
         UpdateGridGhost(Grille, 2)
      if number == 3:
         UpdateGridGhost(Grille, 3)
      if number == 4:
         UpdateGridGhost(Grille, 4)
   else:
      UpdateGrid(Grille)
   
   isEven = False
   while isEven == False:
      isEven = True 
      GrillePrevious = copy.deepcopy(Grille)
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if Grille[x][y] > 0 and Grille[x][y]< 150:
               
               left = Grille[x-1][y]
               right = Grille[x+1][y]
               up  = Grille[x][y+1]
               down = Grille[x][y-1]
               # On trouve le minimum entre les 4 directions possibles
               min = FourMinimal(left,right,up,down)
               # Si le minimum +1 est tjrs inferieur à la valeur de la case courante, on donne la valeur de minimum+1 à la case courante
               if min+1 < Grille[x][y] : 
                  Grille[x][y] = min+1      
           
      # Verifie si la grille a encore été changée, si oui : on continue. si non : la grille est finie.
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if Grille[x][y] != GrillePrevious[x][y]:
               
               isEven = False
               break
         
# FONCTION FIN DE PARTIE !

def EndGame():
   for ghost in Ghosts:
      if PacManPos[0] == ghost[0] and PacManPos[1] == ghost[1]:
         canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
         canvas.place(x=0,y=0)
         canvas.configure(background='black')
         canvas.create_text(screeenWidth // 2, screenHeight//2 , text = "Fin de partie ! \nScore :" + str(Score), fill ="yellow", font = PoliceEndText)
         return True
   if Score == 1000:
      canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
      canvas.place(x=0,y=0)
      canvas.configure(background='black')
      canvas.create_text(screeenWidth // 2, screenHeight//2 , text = "Fin de partie ! \nScore :" + str(Score), fill ="yellow", font = PoliceEndText)
      return True
   return False

      



#################################################################
##
##   GAME LOOP
def MainLoop():
   EndGame()
   if(EndGame() != True):
      IA()
      Affiche()
      EatGUM() 
      UpdatePath(Grille, '', '')
      UpdatePath(GrilleGhost1, 'Ghost', 1)
      UpdatePath(GrilleGhost2, 'Ghost', 2)
      UpdatePath(GrilleGhost3, 'Ghost', 3)
      UpdatePath(GrilleGhost4, 'Ghost', 4)
      UpdateGridDist(GrilleDist)

  
 
  
###########################################:
#  demarrage de la fenetre - ne pas toucher

AfficherPage(0)
Window.mainloop()

   
   
    
   
   