'''Projet info'''
import numpy as np
from itertools import product


from colorama import Fore, Style


def red_text(text):
    ''' Pour afficher du texte en rouge'''

    return f"{Fore.RED}{text}{Style.RESET_ALL}"


'''Algorithme de Needleman-Wunsch'''


class Ruler:
    
    def __init__(self, chaine1: str, chaine2: str, dist=1, sub=1):
        # on peut modifier le cout des insertions et des délétions (d) et des substitutions (s)
        # par défaut on place ce coût à 1
        self.chaine1 = chaine1
        self.chaine2 = chaine2
        # on initialise notre matrice de calcul de distance minimale
        self.M = np.zeros(
            (len(self.chaine2)+1, len(self.chaine1)+1), dtype=int)
        self.d = dist
        self.s = sub
        self.distance = 0

    # contrairement à wikipedia, la similitude n'est pas codée sous forme matricielle
    def similitude(self, i: int, j: int):
        '''établit la correspondance entre chaine1[j] et chaine2[i]'''

        if self.chaine1[j-1] == self.chaine2[i-1]:  # les caractères sont similaires
            return (0)
        else:
            # les caractères sont différents et une substitution coute 1
            return(self.s)

    def compute(self):  # ne renvoie rien mais crée la matrice qui sert à déterminer la distance minimale
        '''lance le calcul pour construire M'''

        self.M[0] = self.d*np.arange(1, len(self.chaine1) + 2)
        self.M[:, 0] = self.d*np.arange(1, len(self.chaine2) + 2)
        self.M[0, 0] = 0
        for (i, j) in product(range(1, len(self.chaine2) + 1), range(1, len(self.chaine1) + 1)):
            '''on regarde à chaque étape lorsqu'on parcourt la chaine2 si il vaut mieux ajouter un trou
            sur la chaine1 ou sur la chaine2 ou si il faut les aligner pour avoir la plus grande ressemblance
            entre les deux chaines à la fin'''
            self.M[i, j] = min(self.M[i-1, j] + self.d, self.M[i, j-1] +
                               self.d, self.M[i-1, j-1] + self.similitude(i, j))
        self.distance = self.M[len(self.chaine2), len(self.chaine1)]
   
        # distance min que l'on peut obtenir en alignant toute la chaine1 avec la chaine2
      

    # on va parcourir M en partant de M[m,n] et on va remonter pour savoir quel alignement donne une distance minimale
    def report(self):
        top = ''
        bottom = ''

        i = len(self.chaine2)
        j = len(self.chaine1)
        while (i, j) != (0, 0):
            b = min(self.M[i-1, j-1], self.M[i, j-1], self.M[i-1, j])
            # on regarde les voisins de M[i,j] pour trouver celui qui a le plus petit coeff
            # ce sera donc l'ancêtre de M[i,j]
            if self.M[i-1, j-1] == b:
                top += self.chaine1[j-1]
                bottom += self.chaine2[i-1]
                j = j-1
                i = i-1

            elif self.M[i, j-1] == b:
                top += self.chaine1[j-1]
                bottom += '='
                j = j-1
            else:
                top += '='
                bottom += self.chaine2[i-1]
                i = i-1
        top2 = ''
        bottom2 = ''
        # on remet top et bottom dans le bon sens car on avait décodé en partant de la fin
        for (x, y) in zip(top[::-1], bottom[::-1]):
            if x != y:  # il faut donc les mettre en rouge
                top2 += red_text(x)
                bottom2 += red_text(y)
            else:
                top2 += x
                bottom2 += y

        return(top2, bottom2)
'''
ruler = Ruler("ACTG", "CG")

# on impose à l'utilisateur de la classe
# de lancer explicitement le calcul
ruler.compute()

# on obtient la distance
print(ruler.distance)

# et pour afficher les différences
top, bottom = ruler.report()
print(top)
print(bottom)
'''