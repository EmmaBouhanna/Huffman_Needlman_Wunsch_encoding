from ruler import Ruler
import csv
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("fichier", help= "le nom du fichier")
args = parser.parse_args()
import numpy as np

'''1ère méthode : en utilisant l'itérateur'''

with open(args.fichier, 'r') as f:
    sentinelle = True
    n = 0
   
    while sentinelle == True:
        try : 
            b = next(f)
            n += 1
            c = next(f)
        except StopIteration:
            sentinelle = False
            break
        
        try :
            next(f) # la ligne vide qu'il faut passer entre deux comparaisons
        except StopIteration:
            sentinelle = False # cela signifie que la dernière ligne était vide
            break

        fragment = Ruler(b, c)
        fragment.compute()
        (top, bottom) = fragment.report()
        print(f"====== fragment #{n} - distance = {fragment.distance} \n{top}\n{bottom}")
 


print("fin de la comparaison")



'''  Deuxième façon : avec pandas '''
import pandas as pd

with open(args.fichier, 'r') as fichier2:
    dataset = pd.read_csv(fichier2, header=None) # peut lire un fichier .txt
    n = len(dataset[0])
    print(n)
    print(dataset)
    # Les lignes vides sont automatiquement supprimées par le pd.read_csv
    # Mais au cas où, on remplace les lignes vides par des NaN et on les enlève

    dataset.replace('', np.nan, inplace=True)
    dataset.dropna(inplace=True)


    for k in range(0, n//2):  # on ne prend pas en compte la dernière ligne
        fragment = Ruler(dataset[0][2*k], dataset[0][2*k+1])
        fragment.compute()
        (top, bottom) = fragment.report()

        print(
            f"====== fragment #{k+1} - distance = {fragment.distance} \n{top}\n{bottom}")
