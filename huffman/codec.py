'''modules utiles'''
from itertools import product


class Node:
    ''' Cette classe construit le noeud correspondant à l'ancêtre des deux occurences avec le plus petit poids'''

    def __init__(self, occurence: dict):
        self.parent = ['', 0]
        # chaine de caractère correspondant au parent et poids correspondant
        self.enfants = {}
        self.dictionnaire = occurence

    def construction_du_noeud(self):
        a = min(self.dictionnaire.values())
        for key in self.dictionnaire:
            if self.dictionnaire[key] == a:
                self.enfants['0'] = key
                self.parent[0] += key
                self.parent[1] += a
                # on enlève le caractère du dictionnaire des occurences
                del(self.dictionnaire[key])
                break
        b = min(self.dictionnaire.values())
        for key2 in self.dictionnaire:
            if self.dictionnaire[key2] == b:
                self.enfants['1'] = key2
                self.parent[0] += key2
                self.parent[1] += b
                del self.dictionnaire[key2]
                break
        # apparition du nouveau caractère issu de la fusion des deux précédents.
        self.dictionnaire[self.parent[0]] = self.parent[1]


class TreeBuilder:
    '''classe capable de construire un arbre binaire à partir d'une chaine de caractère'''

    def __init__(self, text: str):
        self.texte = text
        self.occur = {}  # dictionnaire des poids de chaque caractère
        for x in self.texte:
            if x in self.occur:
                self.occur[x] += 1
            else:
                self.occur[x] = 1
        # self.occur comporte initialement le nombre d'occurences de chaque caractère

    def tree(self):
        '''construit l'arbre binaire à partir du texte'''
        liste = []
        # on construit une liste de tuples contenant à chaque fois : le parent et le dictionnaire contenant des clés binaires avec comme valeur les chaines de caractères correspondant
        while len(self.occur) >= 2:
            noeud = Node(self.occur)
            noeud.construction_du_noeud()
            liste += [(noeud.parent[0], noeud.enfants)]
        for i in range(1, len(liste)):
            # on regarde les values de chaque dictionnaire des enfants
            for x in liste[i][1].values():
                for (y, z) in product(liste, liste[i][1]):
                    # liste[i][1][z] est une valeur du dictionnaire des enfants
                    if y[0] == x and liste[i][1][z] == x:
                        # on remplace la chaine de caractère par le dictionnaire des enfants avec les clés binaires qui lui correspond
                        liste[i][1][z] = y[1]
        return(liste[-1][1])
        # le dernier élément de la liste sera mis à jour avec tous les dictionnaires au lieu des chaines de caractères.


class Codec:

    def __init__(self, tree):
        self.binarytree = tree

    def traduction(self, memoire=''):
        '''renvoie un dictionnaire qui contient les codes binaires de chaque lettre'''
        code = {}

        def intermediaire(arbre: dict, codebis, memoire=''):
            for noeud in arbre.keys():
                if len(arbre[noeud]) == 1:
                    codebis[memoire+noeud] = arbre[noeud]
                else:
                    intermediaire(arbre[noeud], codebis, memoire+noeud)

        intermediaire(self.binarytree, code)
        return(code)

    def encode(self, text):
        '''renvoie le texte codé sous forme binaire'''
        code = self.traduction()
        binarytext = ''
        # on construit le dictionnaire inverse pour pouvoir accéder plus facilement aux caractères grâce aux clés
        # toutes les valeurs sont différentes telles que l'on a construit code
        codeinv = dict((texte, binary) for (binary, texte) in code.items())
        for x in text:
            binarytext += codeinv[x]
        return(binarytext)

    def decode(self, binary):
        '''renvoie une chaine de caractère issue du décodage d'une chaine binaire'''
        code = self.traduction()
        realtext = ''
        parcours = ''
        for b in binary:
            parcours += b
            if parcours in code:
                realtext += code[parcours]
                parcours = ''
        return(realtext)


'''test'''
text = "a dead dad ceded a bad babe a beaded abaca bed"

# on analyse les fréquences d'occurrence dans text
# pour fabriquer un arbre binaire
builder = TreeBuilder(text)
binary_tree = builder.tree()

print(binary_tree)

# on passe l'arbre binaire à un encodeur/décodeur
codec = Codec(binary_tree)
# qui permet d'encoder
encoded = codec.encode(text)
# et de décoder
decoded = codec.decode(encoded)
# si cette assertion est fausse il y a un gros problème avec le code
assert text == decoded

# on affiche le résultat
print(f"{text}\n{encoded}")
if decoded != text:
    print("OOPS")
else:
    print("Gagné!")
