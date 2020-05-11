import tkinter as tk
import random
import numpy as np
import copy
import time

#################################################################################
#
#   Données de partie

Data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()

LARGEUR = 13
HAUTEUR = 17


# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit, 1, 1)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L

Window = tk.Tk()
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))  # taille de la fenetre
Window.title("TRON")

# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
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

canvas = tk.Canvas(Frame0, width=largeurPix, height=hauteurPix, bg="black")
canvas.place(x=0, y=0)


#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()

    def DrawCase(x, y, coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=coul)

    # dessin des murs

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1: DrawCase(x, y, "gray")
            if Game.Grille[x, y] == 2: DrawCase(x, y, "cyan")

    # dessin de la moto
    DrawCase(Game.PlayerX, Game.PlayerY, "red")


def AfficheScore(Game):
    info = "SCORE : " + str(Game.Score)
    canvas.create_text(80, 13, font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA


def MonteCarlo(Game, nombreParties):
    """Principe de MonteCarlo, pour un nombre donné ont va simuler
    a chaque fois une partie aléatoire et indiquer la somme
    des scores récupérés pour chaque partie avant qu'elle ne termine en erreur. """
    result = 0
    for i in range(nombreParties):
        Game2 = Game.copy()
        result += SimulPart(Game2)
    return result


def MonteCarloOpti(Game, nombreParties):
    return SimulPartOpti(Game, nombreParties)


def ListMoves(Game):
    """Cette fonction renvoie une liste de tuple contenant (x,y)
    indiquant les deplacements possible, haut bas droite gauche """
    x, y = Game.PlayerX, Game.PlayerY
    a = Game.Grille[x, y + 1]
    b = Game.Grille[x + 1, y]
    c = Game.Grille[x, y - 1]
    d = Game.Grille[x - 1, y]

    listRet = []

    if a == 0: listRet.append((0, 1))
    if b == 0: listRet.append((1, 0))
    if c == 0: listRet.append((0, -1))
    if d == 0: listRet.append((-1, 0))

    return listRet


def SimulPart(Game):
    """Ici on simule une partie, des déplacements aléatoires sont faits
    et tant qu'on a pas perdu on continue à jouer, bien sur dès qu'on avance
     on met à jours le nombre de case parcouru, dès qu'on perd on retourne le nombre."""
    cases = 0
    x, y = Game.PlayerX, Game.PlayerY
    while (True):
        Game.Grille[x, y] = 2  # laisse la trace de la moto
        mvt = ListMoves(Game)
        nbMvt = len(mvt)

        if nbMvt == 0:
            # collision détectée car aucune option possible
            return cases  # retourner le nombre ce case

        else:
            pos = random.randrange(nbMvt)
            x += mvt[pos][0]
            y += mvt[pos][1]
            Game.PlayerX = x  # valide le déplacement
            Game.PlayerY = y  # valide le déplacement
            cases += 1


# Optimisation de la simulation par numpy:------------

# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas
dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int8)


def ListMovesNumpy(G, I, X, Y, nb):
    """
    cette fonction retourne toutes les possibilités de déplacement dans une liste de 4,
    pour chaque partie I
    :param G: Grille
    :param I: Liste associée à toutes les partie
    :param X: coordonnée x, toutes les parties
    :param Y: coordonnée y, toutes les parties
    :return: listes possibilités (1,2,3,4 ou 0) et nombre total de possibilité pour chaque (indices)
    chaque element dans la liste des possibilités est en fait l'indice dans la liste des directions
    """
    LPossible = np.zeros((nb, 4), dtype=np.int8)
    indices = np.zeros(nb, dtype=np.int8)

    Vgauche = (G[I, X - 1, Y] == 0) * 1
    LPossible[I, indices[I]] = Vgauche
    indices[I] += Vgauche

    Vdroite = (G[I, X + 1, Y] == 0) * 1
    LPossible[I, indices[I]] = Vdroite * 3
    indices[I] += Vdroite

    Vhaut = (G[I, X, Y + 1] == 0) * 1
    LPossible[I, indices[I]] = Vhaut * 2
    indices[I] += Vhaut

    Vbas = (G[I, X, Y - 1] == 0) * 1
    LPossible[I, indices[I]] = Vbas * 4
    indices[I] += Vbas

    return (LPossible, indices)


def SimulPartOpti(Game, nb):
    """La fonction qui simule un nombre nb de partie, en retournant un score qui correspondant à chaque déplacement
    de chaque partie, avant la défaite. Cette simulation est très optimisés grâce à numpy"""
    # on copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    while (boucle):

        # marque le passage de la moto
        G[I, X, Y] = 2

        # on créé les deux listes pour se déplacer
        LPossible, indices = ListMovesNumpy(G, I, X, Y, nb)
        # on remplace tous les 0 par des 1, utile plus tard pour le modulo
        indices[indices == 0] = 1

        # Direction : 2 = vers le haut
        # Choix = np.ones(nb,dtype=np.uint8) * 2

        Choix = np.random.randint(12, size=nb)  # nombre entre 0 et 12 pour toutes les parties
        Choix = Choix % indices  # le nombre entre 0 et 12 est modulo indices, ainsi on ne peut obtenir que 0,1,2 ou 3
        # Le nouveau nombre choix est la direction possible, pioché aléatoirement dans la liste
        # grace au precedent nombre choix ( 0,1,2,3)
        Choix = LPossible[I, Choix]

        if np.array_equal(Choix, np.zeros(nb, dtype=np.int8)):  # si toutes les direction possible sont 0
            return S.sum()  # alors on retourne la somme de tous les scores

        # on ajoute un au score pour toutes les parties où la direction n'est pas 0
        S += (Choix != 0) * 1

        # DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]

        X += DX
        Y += DY


# --

def Play(Game):
    """La fonction qui fait tourner le jeu, soit c'est aléatoire soit c'est Monte Carlo."""
    ia = True
    opti = True
    if ia:
        return PlayMonteCarlo(Game, opti)
    else:
        return PlayRandom(Game)


def PlayRandom(Game):
    """La fonction qui joue de maniere aleatoire."""

    x, y = Game.PlayerX, Game.PlayerY

    Game.Grille[x, y] = 2  # laisse la trace de la moto

    mvt = ListMoves(Game)  # On recupere la liste des positions
    nbMvt = len(mvt)  # sa longueur

    if nbMvt == 0:
        # collision détectée car aucune option possible
        return True  # partie terminée

    else:
        pos = random.randrange(nbMvt)  # on recupere un nombre aleatoire, un index pour la liste
        x += mvt[pos][0]  # on ajoute a x la valeur x du tuple dans la liste mvt à l'index  recuperee au dessus
        y += mvt[pos][1]  # on ajoute a y la valeur y du tuple dans la liste mvt à l'index  recuperee au dessus

        Game.PlayerX = x  # valide le déplacement
        Game.PlayerY = y  # valide le déplacement
        Game.Score += 1
        return False  # la partie continue


def PlayMonteCarlo(Game, opti):
    """La fonction qui joue de maniere MonteCarlo."""

    x, y = Game.PlayerX, Game.PlayerY
    Game.Grille[x, y] = 2  # laisse la trace de la moto
    mvt = ListMoves(Game)  # On recupere la liste des positions
    nbMvt = len(mvt)  # sa longueur
    if nbMvt == 0:
        # collision détectée car aucune option possible
        return True  # partie terminée

    else:
        good_move = (0, 0)  # on admet un tuple de coordonnee par defaut
        actuMax = 0  # on admet un maximum
        for elt in mvt:  # pour chaque tuple dans la liste
            Game.PlayerX += elt[0]  # on augmente les coordonnées temporairement pour monteCarlo
            Game.PlayerY += elt[1]
            if opti:
                thisMax = MonteCarloOpti(Game, 10000)
                print(thisMax)
            else:
                thisMax = MonteCarlo(Game, 3000)  # on calcul un nombre avec monteCarlo et le jeu
                # qui viens de recevoir le deplacement du tuple
            Game.PlayerX -= elt[0]  # une fois le nombre calcule, on enleve les deplacement
            Game.PlayerY -= elt[1]  # On pourrait cloner Game mais cela est plus couteux alors on enleve simplement
            if thisMax >= actuMax:  # si le max est plus grand que celui actuel
                actuMax = thisMax  # alors on a un nouveau max
                good_move = elt  # et on sait que le meilleur tuple est celui qui nous a donné ce nouveau max
        x += good_move[0]
        y += good_move[1]
        Game.PlayerX = x  # valide le déplacement
        Game.PlayerY = y  # valide le déplacement
        Game.Score += 1
        return False


################################################################################

CurrentGame = GameInit.copy()


def Partie():
    tstart = time.time()
    PartieTermine = Play(CurrentGame)
    print(time.time() - tstart)
    if not PartieTermine:
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(500, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100, Partie)
Window.mainloop()
