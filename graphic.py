from geneticAlgorithm import *
import re
FOOD_PER_GENERATION = 5
class Object():
    def __init__(self,position,chromosome) -> None:
        self.x = position[0]
        self.y = position[1]
        self.chromosome = chromosome
class Map():
    def __init__(self,mapName) -> None:
        self.map = mapName
        file = open(f"./map/{mapName}.map",'r')
        contents = file.readlines()
        self.size = [int(re.match('(\d*)( )*,( )*(\d*),( )*(\d*)',contents[0]).group(i)) for i in [1,4,6]]
        self.seed = self.size.pop(2)
        self.contents = [contents[i][0:self.size[0]] for i in range(1,self.size[1]+1)]
        self.contents = [[j for j in i] for i in self.contents]
    def getPosition(self,seed) :
        random.seed(seed)
        x = random.choice(list(range(self.size[0])))
        random.seed(seed)
        random.seed(int(str(random.random())[2:]))
        y = random.choice(list(range(self.size[1])))
        while self.contents[y][x] == "P" or self.contents[y][x] == "F":
            random.seed(seed)
            move = random.sample([-1,-1,1,1],2)
            x,y = x+move[0] , y+move[1]
        return x, y
    def makeFood(self):
        for i in range(FOOD_PER_GENERATION):
            position = list(self.getPosition(self.seed))
            self.contents[position[0]][position[1]] = "F"
            random.seed(self.seed)
            self.seed = int(str(random.random())[2:])
    def printMap(self):
        converter = {"0" : "🟩", "P" : "🧑", "F" : "🍎"}
        print('\n'.join([''.join([converter[j] for j in i]) for i in self.contents]))
    def getObjectPosition(self):
        for i in range(len(self.contents)):
            for j in range(len(self.contents[i])):
                if self.contents[i][j] == 'P':
                    yield [j,i]
map = Map("01")
map.makeFood()
map.printMap()
(list(map.getObjectPosition()),)