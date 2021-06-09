simple = [1,2]
cimple = simple
for i in range(len(simple)):
    simple.append(i+1)
simple[0] = 7
print(cimple)
