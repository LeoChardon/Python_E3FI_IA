import tkinter as tk
import random
import time
import numpy as np

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


class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)


GameInit = Game(GInit, 1, 1)


#############################################################
#
#  affichage en mode texte


def AffGrilles(G, X, Y):
    nbG, larg, haut = G.shape
    for y in range(haut - 1, -1, -1):
        for i in range(nbG):
            for x in range(larg):
                g = G[i]
                c = ' '
                if G[i, x, y] == 1: c = 'M'  # mur
                if G[i, x, y] == 2: c = 'O'  # trace
                if (X[i], Y[i]) == (x, y): c = 'X'  # joueur
                print(c, sep='', end='')
            print(" ", sep='', end='')  # espace entre les grilles
        print("")  # retour à la ligne


###########################################################
#
# simulation en parallèle des parties


# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas
dx = np.array([0, -1, 0, 1, 0], dtype=np.int8)
dy = np.array([0, 0, 1, 0, -1], dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0, 1, 1, 1, 1], dtype=np.int8)

Debug = True
nb = 10  # nb de parties


def ListMoves(G, I, X, Y):
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


def Simulate(Game):
    # on copie les datas de départ pour créer plusieurs parties en //
    G = np.tile(Game.Grille, (nb, 1, 1))
    X = np.tile(Game.PlayerX, nb)
    Y = np.tile(Game.PlayerY, nb)
    S = np.tile(Game.Score, nb)
    I = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    if Debug: AffGrilles(G, X, Y)

    # VOTRE CODE ICI

    while (boucle):
        if Debug: print("X : ", X)
        if Debug: print("Y : ", Y)
        if Debug: print("S : ", S)

        # marque le passage de la moto
        G[I, X, Y] = 2

        # on créé les deux listes pour se déplacer
        LPossible, indices = ListMoves(G, I, X, Y)
        # on remplace tous les 0 par des 1, utile plus tard pour le modulo
        indices[indices == 0] = 1

        # Direction : 2 = vers le haut
        # Choix = np.ones(nb,dtype=np.uint8) * 2

        Choix = np.random.randint(12, size=nb)  # nombre entre 0 et 12 pour toutes les parties
        Choix = Choix % indices  # le nombre entre 0 et 12 est modulo indices, ainsi on ne peut obtenir que 0,1,2 ou 3
        # Le nouveau nombre choix est la direction possible, pioché aléatoirement dans la liste
        # grace au precedent nombre choix ( 0,1,2,3)
        Choix = LPossible[I, Choix]

        if np.array_equal(Choix, np.zeros(nb, dtype=np.int8)): # si toutes les direction possible sont 0
            print(S.sum())
            return S.sum() # alors on retourne la somme de tous les scores

        # on ajoute un au score pour toutes les parties où la direction n'est pas 0
        S += (Choix != 0) * 1

        # DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]

        if Debug: print("DX : ", DX)
        if Debug: print("DY : ", DY)
        X += DX
        Y += DY

        # debug
        if Debug: AffGrilles(G, X, Y)
        if Debug: time.sleep(2)

        print("Scores : ", np.mean(S))


Simulate(GameInit)
