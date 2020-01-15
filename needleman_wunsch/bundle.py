from ruler import Ruler
import pandas as pd
import numpy as np

dataset = pd.read_csv("DATASET.csv", header = None)
n = len(dataset[0])
print(n)
print(dataset)
# Les lignes vides sont automatiquement supprimées par le pd.read_csv
# Mais au cas où, on remplace les lignes vides par des NaN et on les enlève

dataset.replace('', np.nan, inplace = True)
dataset.dropna(inplace = True)


for k in range(0, n//2): # on ne prend pas en compte la dernière ligne
        fragment = Ruler(dataset[0][2*k], dataset[0][2*k+1])
        fragment.compute()
        (top, bottom) = fragment.report()
        
        print(
            f"====== fragment #{k} - distance = {fragment.distance} \n{top}\n{bottom}")
