from scipy.spatial.distance import euclidean
import numpy as np
import pandas as pd
import copy

clu_id = 0 #variavel global, pq antes tava resetando com a função.

# --------------------- Classes --------------------- #
class Objeto:
    def __init__(self, i, d1, d2):
        self.clu_id = None
        self.id = i
        self.atributos = []
        self.atributos.append(d1)
        self.atributos.append(d2)

    def __eq__(self, other):
        if not isinstance(other, Objeto):
            return False
        return np.array_equal(self.atributos, other.getAtributos())

    def getAtributos(self):
        return self.atributos

    def getId(self):
        return self.id

    def getClusterID(self):
        return self.clu_id

    def setClusterID(self, i):
        self.clu_id = i

class Cluster:
    def __init__(self, i):
        self.id = i
        self.obj = []

    def __eq__(self, other):
        return self.obj[0].__eq__(other.getObjeto(0))

    def getObjetos(self):
        return self.obj

    def addObjeto(self, o):
        self.obj.append(o)

    def getId(self):
        return self.id

class ParObjetos:
    def __init__(self, obj1, obj2):
        self.obj = []
        self.obj.append(obj1)
        self.obj.append(obj2)
        self.dist = euclidean([obj1.getAtributos()], [obj2.getAtributos()])
        
    def getObjeto(self, i):
        return self.obj[i]

    def getDist(self):
        return self.dist
        
# ----------------- Funcoes internas ----------------- #

def calculo_distancias_iniciais(qtd_obj, objetos):
    # Instanciamento dos pares de objetos, evitando repeticoes...
    pares = []  #pares de clusters (inicialmente cada cluster so tem um objeto)
    for i in range(qtd_obj):
        for j in range(i + 1):
            # ...e evitando pares de objetos com eles mesmos.
            if not objetos[i].__eq__(objetos[j]):
                pares.append(ParObjetos(objetos[i], objetos[j]))
    
    pares.sort(key=lambda x: x.dist)

    # for i in range(len(pares)):
    #     print(f"par({pares[i].getObjeto(0).getId()}, {pares[i].getObjeto(1).getId()}): dist = {pares[i].dist}")
    return pares


def single_link(pares, objetos):

    particoes = [[] for _ in range(len(pares))]
    temp = 0
    clu_id = 0 #variavel global, pq antes tava resetando com a função.
    n_clusters = len(objetos)

    for k in range(len(pares)):

        obj1 = pares[k].getObjeto(0)
        obj2 = pares[k].getObjeto(1)

        print(f"obj1: {obj1.getId()}, {obj1.getClusterID()}, obj 2 : {obj2.getId()}, {obj2.getClusterID()}")


        #Condição de parada para fazer os grupos finais
        if n_clusters == 2:
            break
        
        #Essa condição precisa existir para ele n contar valores que já ocorreram.
        if obj1.getClusterID() == obj2.getClusterID() and (obj1.getClusterID() is not None and obj2.getClusterID() is not None):
            continue

        if obj1.getClusterID() is None and obj2.getClusterID() is None:
            n_clusters -= 1
            obj1.setClusterID(clu_id)
            obj2.setClusterID(clu_id)
            clu_id += 1

        elif not (obj1.getClusterID() is None) and not (obj2.getClusterID() is None):

            n_clusters -= 1
            substituto = obj1.getClusterID()
            substituido = obj2.getClusterID()
            for j in range(len(objetos)):
                if objetos[j].getClusterID() == substituido:
                    objetos[j].setClusterID(substituto)
            

        else:
            if obj1.getClusterID() is None:
                n_clusters -= 1
                obj1.setClusterID(obj2.getClusterID())
            elif obj2.getClusterID() is None:
                n_clusters -= 1
                obj2.setClusterID(obj1.getClusterID())

        
    for m in range(len(objetos)):
        print(f"{objetos[m].getId()} {objetos[m].getClusterID()}")
    print(f"----")
    

    #return particoes
# ------------------------------------------------------ #

def hierarquico_aglomerativo(dados, kmin, kmax):
    tam = len(dados)
    objetos = []
    for i in range(tam):
        objetos.append(Objeto(dados.loc[i][0], dados.loc[i][1], dados.loc[i][2]))
    
    pares = calculo_distancias_iniciais(tam, objetos)
    particoes = single_link(pares, objetos)
    # for k in range(kmin, kmax):
    #     print(f"k={k + 1}:")
    #     temp_id = len(objetos) - 1
    #     for i in range(len(particoes[k])):
    #         if particoes[k][i].getClusterID() is None:
    #             print(f"{particoes[k][i].getId()}: {temp_id}")
    #             temp_id -= 1
    #         else:
    #             print(f"{particoes[k][i].getId()}: {particoes[k][i].getClusterID()}")
    #     # print('\n')

def main():
    c2ds1 = pd.read_csv("dados.txt", sep="\t")
    hierarquico_aglomerativo(c2ds1, 0, 6)

if __name__ == '__main__':
    main()