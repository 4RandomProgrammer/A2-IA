import random 
from kmedia import kmedia
# from aglomerativo import hierarquico_aglomerativo
import aglomerativo as x
import pandas as pd
from sklearn.metrics.cluster import adjusted_rand_score

def main():
    # Lendo os arquivos de dados
    c2ds1 = pd.read_csv("datasets/dummy.txt", sep="\t")
    hipotese = kmedia(c2ds1, 2, 5)
    c2ds1_real = pd.read_csv("datasets/c2ds1-2spReal.clu", header=None, sep="\t")

    # esperado = []
    # for i in range(len(c2ds1_real)):
    #     esperado.append(c2ds1_real.loc[i][1])

    # ari = adjusted_rand_score(hipotese, esperado)
    # print(ari)

    # hierarquico_aglomerativo(c2ds1, 0, 0)
    x.calculo_distancias_inicial(c2ds1, len(c2ds1))

if __name__ == '__main__':
    main()