from scipy.spatial.distance import euclidean

# ----------------- Funcoes internas ----------------- #
def calculo_distancias_inicial(dados, tam):
    distancias = {}
    for i in range(tam):
        dist_list = []
        for j in range(i + 1):
            dist_list.append( round(euclidean([dados.loc[i][1], dados.loc[i][2]], [dados.loc[j][1], dados.loc[j][2]]), 2))
        distancias[dados.loc[i][0]] = dist_list
    return distancias

def single_link(dados, distancias, tam):
    return
# ------------------------------------------------------ #

def hierarquico_aglomerativo(dados, kmin, kmax):
    tam = len(dados)
    distancias = {}
    distancias = calculo_distancias_inicial(dados, tam)
    single_link(dados, distancias, tam)