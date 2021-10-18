import random 
import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.metrics.cluster import adjusted_rand_score

# ----------------- Funcoes auxiliares ----------------- #
def recalculo_centr(cluster):
    """
    Descricao: recalcula o centroide do cluster passado por parametro
    Parametro:
        cluster: um cluster
    Retorno: 
        novo_centr: um vetor com as coordenadas do novo centroide desse cluster
    """
    tam = len(cluster)
    # Primeiro atributo
    soma_d1 = 0
    for i in range(tam):
        soma_d1 += cluster[i][1]

    # Segundo atributo
    soma_d2 = 0
    for i in range(tam):
        soma_d2 += cluster[i][2]

    novo_centr = [soma_d1 / tam, soma_d2 / tam]
    return novo_centr

def divide_cluster(dados, distancias, tam, k):
    """
    Descricao: separa os objetos em cada cluster usando a menor distancia do centroide como criterio
    Parametros:
        dados: datagrama dos dados
        distancias: matriz de distancias euclidianas
        tam: numero de objetos
        k: numero de clusters
    Retorno: 
        clusters: vetor de clusters resultantes da divisao
    """
    clusters = [[] for _ in range(k)]   #inicializacao do vetor de clusters
    # Para cada objeto...
    for obj_i in range(tam):
        minimo = distancias[0][obj_i]  #pega a primeira distancia como valor inicial
        indice = 0
        # ...entre cada cluster(centroide)...
        for clu_id in range(k):
            # ...verifica qual a menor distancia.
            if minimo > distancias[clu_id][obj_i]:
                minimo = distancias[clu_id][obj_i]
                indice = clu_id #armazena em qual dos clusters deve ser inserido o objeto atual
        # Insere o objeto no cluster correto
        clusters[indice].append([dados.loc[obj_i][0], dados.loc[obj_i][1], dados.loc[obj_i][2]])
    return clusters

def calculo_distancias_inicial(dados, tam):
    distancias = {}
    for i in range(tam):
        dist_list = []
        for j in range(tam):
            dist_list.append( round(euclidean([dados.loc[i][1], dados.loc[i][2]], [dados.loc[j][1], dados.loc[j][2]]), 2))
        # dist_list.append([euclidean([dados.loc[i][1], dados.loc[i][2]], [dados.loc[j][1], dados.loc[j][2]]) for j in range(tam)])
        distancias[dados.loc[i][0]] = dist_list
        
    return distancias

def single_link(dados, distancias, tam):
    particoes = [[] for _ in range(tam)]
    for k in range(tam):
        nome_minimo_i = ''
        nome_minimo_j = ''

        # Passa por toda a matriz em busca da menor distancia
        for i in range(tam - k):
            if k == 0:
                nome = dados.loc[i][0]
            else:
                nome = '' + nome_minimo_i + ' ' + nome_minimo_j
            
            minimo = distancias[nome][1] #pega a primeira distancia diferente de 0
            for j in range(tam - k):
                print(str(nome) + ': ' + str(distancias[nome][j]))
                if minimo > distancias[nome][j] and distancias[nome][j] != 0:
                    minimo = distancias[nome][j]
                    nome_minimo_i = nome
                    nome_minimo_j = dados.loc[j][0]

        # e readiciona uma dimensao que representa o novo cluster agrupado
        nova_dist_list = []
        for m in range(tam):
            if distancias[nome_minimo_i][m] > distancias[nome_minimo_j][m]:
                nova_dist_list.append(distancias[nome_minimo_j][m])
            else:
                nova_dist_list.append(distancias[nome_minimo_i][m])

        novo_nome = '' + nome_minimo_i + ' ' + nome_minimo_j
        distancias[novo_nome] = nova_dist_list

        # Remove duas dimensoes da matriz
        distancias.pop(nome_minimo_i, None)
        distancias.pop(nome_minimo_j, None)

        # Armazenado o estado da particao em cada iteracao
        particoes[k] = [distancias.keys()]
    print(particoes)
# ------------------------------------------------------ #

def kmedia(dados, k, n):
    """
    Descricao: algoritmo k-medias
    Parametros:
        dados: datagrama dos dados
        k: numero de clusters
        n: numero maximo de iteracoes
    """
    # Declaracoes
    centroides= []
    distancias = []
    tam = len(dados)
    for iteracoes in range(n):
        distancias = [] # reset do vetor de distancias euclidianas
        # Calculo das distancias euclidianas
        for i in range(k):
            # Apenas na primeira iteracao, pegamos centroides aleatorios
            if iteracoes == 0:
                # random_n = random.randint(0, 999)
                random_n = i
                centroides.append([dados.loc[random_n][1], dados.loc[random_n][2]])
            # Calculo e armazenamento da distancia
            # dados.loc[j][1] é o valor do atributo 1
            # dados.loc[j][2] é o valor do atributo 2
            distancias.append([euclidean(centroides[i], [dados.loc[j][1], dados.loc[j][2]]) for j in range(tam)])
                
        clusters = divide_cluster(dados, distancias, tam, k) # separacao dos objetos entre os clusters

        # Novos centroides
        for i in range(k):
            centroides[i] = recalculo_centr(clusters[i])
    
    # Organizacao dos clusters gerados em um dicionario (resultado)
    resultado = {}
    for clu_id in range(k):
        for obj_i in range(len(clusters[clu_id])):
            # clusters[clu_id][obj_i][0] é o "nome" do objeto
            resultado[clusters[clu_id][obj_i][0]] = clu_id #:D

    # Escreve o resultado em um arquivo
    f = open('c2ds1-2spHipotese.txt', 'w')
    for i in range(tam):
        f.write(f"{dados.loc[i][0]} {resultado[dados.loc[i][0]]}\n")
    f.close()

    hipotese = []
    for i in range(tam):
        hipotese.append(resultado[dados.loc[i][0]])
    return hipotese

def hierarquico_aglomerativo(dados, kmin, kmax):
    tam = len(dados)
    distancias = {}
    distancias = calculo_distancias_inicial(dados, tam)
    single_link(dados, distancias, tam)

    
def main():
    # Lendo os arquivos de dados
    c2ds1 = pd.read_csv("datasets/dummy.txt", sep="\t")
    # hipotese = kmedia(c2ds1, 2, 5)
    # c2ds1_real = pd.read_csv("datasets/c2ds1-2spReal.clu", header=None, sep="\t")

    # esperado = []
    # for i in range(len(c2ds1_real)):
    #     esperado.append(c2ds1_real.loc[i][1])

    # ari = adjusted_rand_score(hipotese, esperado)
    # print(ari)

    hierarquico_aglomerativo(c2ds1, 0, 0)

if __name__ == '__main__':
    main()