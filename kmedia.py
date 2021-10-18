from scipy.spatial.distance import euclidean
import pandas as pd

# ----------------- Funcoes internas ----------------- #
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
            resultado[clusters[clu_id][obj_i][0]] = clu_id

    # Escreve o resultado em um arquivo
    f = open('c2ds1-2spHipotese.txt', 'w')
    for i in range(tam):
        f.write(f"{dados.loc[i][0]} {resultado[dados.loc[i][0]]}\n")
    f.close()

    hipotese = []
    for i in range(tam):
        hipotese.append(resultado[dados.loc[i][0]])
    return hipotese