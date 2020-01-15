'''modules utiles'''
from itertools import product


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

    def trouvelespluspetits(self): # au lieu de créer une classe Node, on crée un dictionnaire
        '''cherche les deux caractères avec les plus petits coefficients et construit leur parent (fusion des deux et ajout de leur poids)'''
        petit = {}
        # petit sera un dictionnaire de forme {'0' : 'str de plus petit coeff 1' , '1' : 'str de plus petit coeff 2'}
        poidsparent = 0
        a = min(self.occur.values())
        for key in self.occur:
            if self.occur[key] == a:
                petit['0'] = key
                poidsparent += a
                del self.occur[key]
                break

        b = min(self.occur.values())
        for key2 in self.occur:
            if self.occur[key2] == b:
                petit['1'] = key2
                poidsparent += b
                del self.occur[key2]
                break
        parent = petit['0']+petit['1']
        # apparition d'un nouveau caractère dans self.occur résultant de la fusion des deux précédents.
        self.occur[parent] = poidsparent
        # un tupple pour garder en mémoire le parents des deux plus petits
        return ((parent, petit))

    def tree(self):
        '''construit l'arbre binaire à partir du texte'''
        liste = []
        # on construit une liste de tuples contenant à chaque fois : le parent et le dictionnaire contenant des clés binaires avec comme valeur les chaines de caractères correspondant
        while len(self.occur) >= 2:
            liste += [self.trouvelespluspetits()]
        for i in range(1, len(liste)):
            # on regarde les values de chaque dictionnaire petit
            for x in liste[i][1].values():
                for (y, z) in product(liste, liste[i][1]):
                    if y[0] == x and liste[i][1][z] == x:  # liste[i][1][z] est une valeur de petit
                        # on remplace la chaine de caractère par le dictionnaire avec les clés binaires qui lui correspond
                        liste[i][1][z] = y[1]
        return(liste[-1][1])
        # le dernier élément de la liste sera mis à jour avec tous les dictionnaires au lieu des chaines de caractère


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
