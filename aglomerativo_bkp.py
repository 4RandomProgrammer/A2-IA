from scipy.spatial.distance import euclidean
import numpy as np
import pandas as pd
import copy

# --------------------- Classes --------------------- #
class Objeto:
    def __init__(self, i, d1, d2):
        self.cluster = None
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

    def getCluster(self):
        return self.cluster

    def setCluster(self, i):
        self.cluster = i

class Cluster:
    def __init__(self, i, o):
        self.id = i
        self.obj = []
        self.obj.append(o)   #cada cluster começa com apenas 1 objeto

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
    # for x in range(len(pares)):
    #     print(pares[x].getDist())
    clu_id = 0
    for k in range(len(objetos)):
        obj1 = pares[k].getObjeto(0)
        obj2 = pares[k].getObjeto(1)
        if obj1.getCluster() is None and obj2.getCluster() is None:
            obj1.setCluster(clu_id)
            obj2.setCluster(clu_id)
            clu_id += 1
        elif not (obj1.getCluster() is None) and not (obj2.getCluster() is None):
            substituto = obj1.getCluster()
            substituido = obj2.getCluster()
            for j in range(len(objetos)):
                if objetos[j].getCluster() == substituido:
                    objetos[j].setCluster(substituto)
        else:
            if obj1.getCluster() is None:
                obj1.setCluster(obj2.getCluster())
            else:
                obj2.setCluster(obj1.getCluster())
                
        particoes[k].append(objetos)
        for m in range(len(objetos)):
            print(f"{objetos[m].getId()} {objetos[m].getCluster()}")
        print("----")
    return particoes
# ------------------------------------------------------ #

def hierarquico_aglomerativo(dados, kmin, kmax):
    tam = len(dados)
    objetos = []
    clusters = []
    for i in range(tam):
        objetos.append(Objeto(dados.loc[i][0], dados.loc[i][1], dados.loc[i][2]))
        clusters.append(Cluster(i, objetos[i]))
    
    pares = calculo_distancias_iniciais(tam, objetos)
    single_link(pares, objetos)

def main():
    c2ds1 = pd.read_csv("dados.txt", sep="\t")
    hierarquico_aglomerativo(c2ds1, 0, 0)

if __name__ == '__main__':
    main()