import numpy as np
import math,random,datetime
from numpy.core.numeric import cross
from numpy.random import rand
import graphic
GENE_SET = list(range(1000))
OBJECT_NUM = 4
GENE_NUM = 4
BEST_NUM = 2
class Chromosome():
    def __init__(self,gene,fitness) -> None:
        self.gene = gene
        self.fitness = fitness
    def __repr__(self):
        return str(self.__dict__)
    def copy(self):
        return Chromosome(self.gene.copy(),int(self.fitness))
def makeParents(size) : return [Chromosome(random.sample(GENE_SET, GENE_NUM),0) for i in range(size)]
def selection(parents) :return [parents.pop([i.fitness for i in parents].index(j)) for j in sorted([i.fitness for i in parents],reverse=True)][:BEST_NUM] 
def crossover(parents,slice = (2,5)):
    result = []
    for i in range(math.floor(OBJECT_NUM/2)):
        popped = random.sample(parents[:],2)
        popped[0].gene[slice[0]:slice[1]], popped[1].gene[slice[0]:slice[1]] = popped[1].gene[slice[0]:slice[1]].copy(), popped[0].gene[slice[0]:slice[1]].copy()
        result += popped
    result.append(random.choice(parents[:])) if OBJECT_NUM % 2 != 0 else None
    return result
def getVariance(x) : return sum([(i-sum(x)/len(x))**2 for i in x])
def getStandardDeviation(x) : return math.sqrt(sum([(i-sum(x)/len(x))**2 for i in x])/(len(x)-1))
def mutation(objects, best, percent = 20):return best+[Chromosome([random.choice(GENE_SET) if random.randint(0,100)<=percent else objects[i].gene[j] for j in range(GENE_NUM)],objects[i].fitness) for i in range(OBJECT_NUM)][BEST_NUM:]
def simulation(objects):
    return [graphic.get_fitness(objects[i].gene,mod = print(f"{i+1}번째 객체 시뮬레이션 완료")) for i in range(len(objects))]
def printGene(objects):print('\n'.join([str(i.gene) for i in objects]))
def oneCycle(objects,generation,printer = 0,IsFile = None,writer = ""):
    print(f'/////GENERATION {generation}/////')
    if IsFile is not None: writer += f'/////GENERATION {generation}/////\n'
    if printer == 0 :
        print("==Objects==")
        printGene(objects)
        if IsFile is not None:
            writer += f'==Objects==\n'
            writer += '\n'.join([str(i.gene) for i in objects])+"\n"
    simulationResult = simulation(objects)
    for i in range(OBJECT_NUM):objects[i].fitness = simulationResult[i]
    if printer == 1 :
        print("fitness :",[objects[i].fitness for i in range(OBJECT_NUM)])
        print("sum of fitness :",sum([objects[i].fitness for i in range(OBJECT_NUM)]))
        print("mean of fitness :",sum([objects[i].fitness for i in range(OBJECT_NUM)])/OBJECT_NUM)
        print("best fitness :",max([objects[i].fitness for i in range(OBJECT_NUM)]))
        print("best gene :",objects[[objects[i].fitness for i in range(OBJECT_NUM)].index(max([objects[i].fitness for i in range(OBJECT_NUM)]))].gene)
        if IsFile is not None:
            writer += "fitness : "+str([objects[i].fitness for i in range(OBJECT_NUM)])+"\n"
            writer += "sum of fitness : "+str(sum([objects[i].fitness for i in range(OBJECT_NUM)]))+"\n"
            writer += "mean of fitness : "+str(sum([objects[i].fitness for i in range(OBJECT_NUM)])/OBJECT_NUM)+"\n"
            writer += "best fitness : "+str(max([objects[i].fitness for i in range(OBJECT_NUM)]))+"\n"
            writer += "best gene : "+str(objects[[objects[i].fitness for i in range(OBJECT_NUM)].index(max([objects[i].fitness for i in range(OBJECT_NUM)]))].gene)+"\n"
    if printer == 0 :
        print("==Selection==")
        if IsFile is not None : writer += "==Selection==\n"
    objects = selection(objects)
    bestChromosome = objects.copy()
    if printer == 0 :
        printGene(objects)
        print("==CrossOver==")
        if IsFile is not None : writer += '\n'.join([str(i.gene) for i in objects])+"\n"
        if IsFile is not None : writer += "==Crossover==\n"
    a = random.randint(0,GENE_NUM-1)
    objects = crossover(objects,slice = (a,random.randint(a,GENE_NUM-1)))
    if printer == 0 :
        printGene(objects)
        print("==Mutation==")
        if IsFile is not None : writer += '\n'.join([str(i.gene) for i in objects])+"\n"
        if IsFile is not None : writer += "==Mutation==\n"
    objects = mutation(objects,bestChromosome,30)
    if printer == 0 :
        printGene(objects)
        if IsFile is not None : writer += '\n'.join([str(i.gene) for i in objects])+"\n"
    if IsFile is not None : IsFile.write(writer)
    return objects
def getData(IsFile = False,generation = 100):
    formatted = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file = open(f'./simulationResult/{formatted}.txt','w') if IsFile else None
    grand = makeParents(OBJECT_NUM)
    for i in range(generation):grand = oneCycle(grand,i,printer=1,IsFile = file)
    if file is not None:file.close()
if __name__ == "__main__":
    getData(IsFile = True, generation = 15)