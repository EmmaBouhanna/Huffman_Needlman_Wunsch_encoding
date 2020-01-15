from ruler import Ruler
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("fichier", help= "le nom du fichier")
args = parser.parse_args()


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