import matplotlib.pyplot as plt
import numpy as np
import os
class Result():
    def __init__(self,fileName = None) -> None:
        if fileName is None:
            dirs = os.listdir('./simulationResult')
            fileSelect = input("===CHOOSE FILE===\n"+'\n'.join([f"[{i}] {dirs[i]}" for i in range(len(dirs))])+"\n>>> ")
            self.fileName = dirs[int(fileSelect)]            
        else:
            self.fileName = fileName
    
    def dump(self):
        result = []
        file = open(f'./simulationResult/{self.fileName}','r')
        allLines = [i[:-1] for i in file.readlines()]
        for i in range(0,len(allLines),6):
            result.append({"fitness":eval(allLines[i+1][10:]),
            "sum of fitness":eval(allLines[i+2][17:]),
            "mean of fitness":eval(allLines[i+3][18:]),
            "best fitness":eval(allLines[i+4][15:]),
            "best gene":eval(allLines[i+5][12:])})
        file.close()
        return result
    
    def dumpAll(self):
        if type(self.fileName) == list or type(self.fileName) == tuple:
            for i in self.fileName: yield self.dump()

    def drawGraph(self,value = None,slice = (0,-1)):
        if value is None:
            OPTIONS = ["fitness","sum of fitness","mean of fitness","best fitness","best gene"]
            optionSelect = input("===CHOOSE VALUES===\n"+'\n'.join([f"[{i}] {OPTIONS[i]}" for i in range(len(OPTIONS))])+"\n>>> ")
            value = OPTIONS[int(optionSelect)]
        data = [i[value] for i in self.dump()][slice[0]:slice[1]]
        plt.plot(list(range(int(len(data)))),data)
        plt.show()
Result().drawGraph()