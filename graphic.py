from geneticAlgorithm import *
import re,os,time
FOOD_PER_GENERATION = 2
def printWithSave(contents="",save = []):
    if contents == "__save__":
        formattedDate = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file = open(f".\\graphics\\{formattedDate}.save",'a',encoding="utf-8")
        if not os.path.isfile(f".\\graphics\\{formattedDate}.save"):
            file.write("\n")
        file.write('\n'.join(save))
        file.close()
        return
    print(contents)
    save.append(str(contents))
class Food():
    def __init__(self,my_map,pos,seed,players,mod = False) -> None:
        self.map = my_map
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        self.seed = seed
        self.players = players
        my_map.contents[pos[1]][pos[0]] = "F"
    def move(self):
        self.map.contents[self.y][self.x] = '0'
        x_option = [-1,0,1]
        if self.x == self.map.size[0]-1:del x_option[2]
        if self.x == 0:del x_option[0]
        random.seed(self.seed)
        self.x += random.choice(x_option)
        y_option = [-1,0,1]
        if self.y == self.map.size[1]-1:del y_option[2]
        if self.y == 0:del y_option[0]
        random.seed(self.seed)
        self.y += random.choice(y_option)
        if tuple((self.x,self.y)) == (0,0):
            y_option = [-1,1]
            if self.y == self.map.size[1]-1:del y_option[1]
            if self.y == 0:del y_option[0]
            random.seed(self.seed)
            self.y += random.choice(y_option)
        self.seed += random.randint(1,50000)
        for player in self.players:
            if [self.x,self.y] == [player.x,player.y]:
                player.strength += min(player.chromosome[0],player.reward)
                self.map.foods.remove(self)
                del self
                return
        self.pos = [self.x,self.y]
        self.map.contents[self.y][self.x] = 'F'
    
    def __repr__(self) -> str:
        return str(self.pos)

class Player():
    def __init__(self,my_map,chromosome,mod = False,player = 1) -> None:
        self.x = list(my_map.getObjectPosition('P'))[player-1][0]
        self.y = list(my_map.getObjectPosition('P'))[player-1][1]
        self.map = my_map
        self.mod = mod
        self.seed = my_map.seed
        self.chromosome = chromosome
        self.strength = chromosome[0]
        self.vision = chromosome[1]/5
        self.reward = chromosome[3]
        self.effectiveness = 100*1/((chromosome[1]+chromosome[2]+self.reward)/2)
        self.speed = max(1,int(chromosome[2]/5))
        self.state = 1
        self.map.players.append(self)

    def getDistance(self,position):
        return math.sqrt((self.x - position[0])**2 + (self.y - position[1])**2)
    def getAbleFoods(self):
        return [food for food in self.map.foods if self.getDistance([food.x,food.y]) < self.vision]
    def detect(self) -> int:
        foods = self.getAbleFoods()
        temp = [self.getDistance([food.x,food.y]) for food in foods]
        #formatting = '\n'.join([f"{i} : {j}" for i,j in list(zip(foods,temp))])
        #print(f"foods - temp : \n{formatting}")
        best = 0
        for i in range(1,len(temp)):
            if temp[i] < temp[best]:best = i
        if len(foods) == 0:
            best = None
        return best

    def getFood(self,target):
        self.map.foods.remove(target)
        del target
        self.strength += min(self.chromosome[0],self.reward)

    def move(self):
        for i in range(self.speed):
            foods = self.getAbleFoods()
            target = self.detect()
            self.map.contents[self.y][self.x] = '0'
            '''if self.mod:
                printWithSave([self.x,self.y])
                printWithSave("strength : "+str(self.strength))
                printWithSave("="*10)'''
            if target is None:
                #if self.mod:printWithSave(f"타겟 : None")
                x_option = [-1,0,1]
                if self.x == self.map.size[0]-1:del x_option[2]
                if self.x == 0:del x_option[0]
                random.seed(self.seed)
                self.x += random.choice(x_option)
                y_option = [-1,0,1]
                if self.y == self.map.size[1]-1:del y_option[2]
                if self.y == 0:del y_option[0]
                random.seed(self.seed)
                self.y += random.choice(y_option)
                if tuple((self.x,self.y)) == (0,0):
                    y_option = [-1,1]
                    if self.y == self.map.size[1]-1:del y_option[1]
                    if self.y == 0:del y_option[0]
                    random.seed(self.seed)
                    self.y += random.choice(y_option)
                self.seed += random.randint(1,50000)
            else:
                #if self.mod:printWithSave(f"타겟 : {foods[target]}")
                target = foods[target]
                if self.x < target.x:
                    self.x += 1
                elif self.x > target.x:
                    self.x -= 1
                elif self.y < target.y:
                    self.y += 1
                if self.y > target.y:
                    self.y -= 1
                if target.x == self.x and target.y == self.y:
                    self.getFood(target)
            self.strength -= 15 * (100-self.effectiveness)/100
            '''if self.mod:
                printWithSave([self.x,self.y])
                printWithSave("strength : "+str(self.strength))'''
            if self.strength <= 0:
                self.state = 0
            self.map.contents[self.y][self.x] = 'P'

class Map():
    def __init__(self,mapName,mod = False) -> None:
        self.map = mapName
        self.mod = mod
        self.players = []
        self.foods = []
        if type(mapName) != str :
            self.map = ("0"*mapName[0]+"\n")*mapName[1]
            self.map = self.map[:int((mapName[1] * (mapName[0]+1))/2)-1] + "P" +self.map[int((mapName[1] * (mapName[0]+1))/2):-1]
            self.size = [mapName[0],mapName[1]]
            self.seed = mapName[2]
            self.contents = [[j for j in i] for i in self.map.split("\n")]
        else:
            file = open(f"./map/{mapName}.map",'r')
            contents = file.readlines()
            self.size = [int(re.match('(\d*)( )*,( )*(\d*),( )*(\d*)',contents[0]).group(i)) for i in [1,4,6]]
            self.seed = self.size.pop(2)
            self.contents = [contents[i][0:self.size[0]] for i in range(1,self.size[1]+1)]
            self.contents = [[j for j in i] for i in self.contents]

    def getPosition(self,seed):
        self.seed += random.randint(1,50000)
        random.seed(self.seed)
        x = random.choice(list(range(self.size[0])))
        random.seed(self.seed+1)
        y = random.choice(list(range(self.size[1])))
        while self.contents[y][x] == "P" or self.contents[y][x] == "F":
            print(self.seed)
            random.seed(self.seed)
            x = random.choice(list(range(self.size[0])))
            random.seed(self.seed+1)
            y = random.choice(list(range(self.size[1])))
            random.seed(self.seed)
            self.seed += random.randint(1,50000)
            #print(self.contents[y][x])
        
        return x, y
    def makeFood(self):
        for i in range(FOOD_PER_GENERATION):
            position = list(self.getPosition(self.seed))
            self.foods.append(Food(self,position,self.seed,self.players))
            random.seed(self.seed)
            self.seed += random.randint(1,50000)

    def makeOneFood(self):
        position = list(self.getPosition(self.seed))
        self.foods.append(Food(self,position,self.seed,self.players))
        random.seed(self.seed)
        self.seed += random.randint(1,50000)
        #print(self.foods)
        return position
    
    def moveFoods(self):
        [food.move() for food in self.foods]

    def printMap(self):
        converter = {"0" : "🟦", "P" : "🐙", "F" : "🟡"}
        if self.mod: printWithSave('\n'.join([''.join([converter[j] for j in i]) for i in self.contents]))
    def getObjectPosition(self,thing):
        for i in range(len(self.contents)):
            for j in range(len(self.contents[i])):
                if self.contents[i][j] == thing:
                    yield [j,i]
def get_fitness(chromosome,mod = False):
    my_map = Map([40,15,150],mod=mod)
    my_map.makeFood()
    #if mod : printWithSave()
    player1 = Player(my_map,chromosome,mod=mod)
    for i in range(1000):
        if player1.state:
            player1.move()
            my_map.moveFoods()
            my_map.printMap()
            if i % 30 == 0:
                player1.map.makeOneFood()
            if mod : printWithSave()
            time.sleep(0.1)
        else:
            if mod : printWithSave("="*10+"died at "+str(i)+"="*10)
            return i
    return 1000
def viewer(chromosome):
    view = []
    my_map = Map("01")
    my_map.makeFood()
    player1 = Player(my_map,chromosome)
    for i in range(1000):
        view.append([])
        last = len(view)-1
        if player1.state:
            player1.move()
            my_map.moveFoods()
            converter = {"0" : "🟦", "P" : "🐙", "F" : "🟡"}
            view[last].append('\n'.join([''.join([converter[j] for j in i]) for i in my_map.contents]))
            if i % 20 == 0:
                player1.map.makeOneFood()
            view[last].append("")
            time.sleep(0.1)
        else:
            converter = {"0" : "🟦", "P" : "💀", "F" : "🟡"}
            view[last].append('\n'.join([''.join([converter[j] for j in i]) for i in my_map.contents]))
            view[last] = '\n'.join(view[last])
            return view
        view[last] = '\n'.join(view[last])
    return view
if __name__ == "__main__":
    get_fitness([900, 827, 9, 659],mod=True)
    printWithSave("__save__")