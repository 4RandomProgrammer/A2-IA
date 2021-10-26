import random 
from kmedia import kmedia
# from aglomerativo import hierarquico_aglomerativo
from aglomerativo import hierarquico_aglomerativo
import pandas as pd
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    # Lendo os arquivos de dados
    # c2ds1 = pd.read_csv("datasets/c2ds1-2sp.txt", sep="\t")
    c2ds1 = pd.read_csv("dummy.txt", sep="\t")
    # hipotese = kmedia(c2ds1, 2, 5)
    # c2ds1_real = pd.read_csv("datasets/c2ds1-2spReal.clu", header=None, sep="\t")

    # esperado = []
    # for i in range(len(c2ds1_real)):
    #     esperado.append(c2ds1_real.loc[i][1])

    # ari = adjusted_rand_score(hipotese, esperado)
    # print(ari)

    hierarquico_aglomerativo(c2ds1, 0, 10)

if __name__ == '__main__':
    main()