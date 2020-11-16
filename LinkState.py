"""
Derek Marshall - 170223090
---------------------------------------------
A3 - CP372
"""

import re, sys
class AdjMatrix:
    def __init__ (self, input):
        input = re.split('[\s \n]', input)
        input = list(filter(None, input))

        
        for i in range(len(input)):
            input[i] = int(input[i])


        self.vertices = input[0]
        self.graph = [0] * self.vertices
        for i in range(self.vertices):
            self.graph[i] = input[i*self.vertices + 1:self.vertices * i + self.vertices + 1]

        self.gateways = input[self.vertices*self.vertices + 1:]

    def _minDist(self, dist, queue):
        ##Calculates minimum distance from from vertecies set
        min = 255 ##Use big number for initial min
        minIndex = -1
        #search not nearest vertex in the spt
        for v in range(len(dist)):
            if dist[v] < min and v in queue:
                min = dist[v]
                minIndex = v
        return minIndex

    def _printPath(self, parent, j, a): #J is gateway node - 1
          
        #Base Case : If j is source 
        if parent[j] == -1 :  
            return
        self._printPath(parent , parent[j], a) 
        a.append(j+1)
        return a

    def printSol(self, dist, parent, tables, gateways):
        src = 0
        for i in range(len(tables)): #Do len tables for printing dist
            print("Forwarding Table for {}".format(tables[i]))
            print("{:>10} {:>10} {:>10}".format("To", "Cost", "Next Hop"))
            for x in gateways:
                a = [] 
                self._printPath(parent[i],x-1, a)
                if a == []:
                    a = [-1]
                print("{:>10} {:>10} {:>10}".format(x, dist[i][x-1], a[0]))

            print()


    def dijkstras(self, src):
        ##Src
        dist = [255] * self.vertices
        parent = [-1] * self.vertices #-1 rep root of tree

        dist[src] = 0

        queue = []
        for v in range(self.vertices):
            queue.append(v) #Add all vertices to queue

        while queue: #While queue not empty
            #Pick min dist vertex from queue set
            minDist = self._minDist(dist, queue)
            
            #remove min from queue
            if (minDist == -1):
                dist[queue.pop(0)] = -1
            else:
                queue.remove(minDist)

            #Update values of dist and parent of adj vertices
            #Only update vertices still in queue
            for v in range(self.vertices):
                if self.graph[minDist][v] > 0 and v in queue:
                    if dist[minDist] + self.graph[minDist][v] < dist[v]:
                        dist[v] = dist[minDist] + self.graph[minDist][v]
                        parent[v] = minDist
            
        return dist, parent


##Driver
f = open(sys.argv[1], "r")
input = f.read()
f.close()

g = AdjMatrix(input)
d = []
p = []
t = []
for i in range(g.vertices):
    if (i+1 not in g.gateways):
        t.append(i+1) #List of tables to be printed
        #d.append(g.dijkstras(i))
        a, b = g.dijkstras(i)
        d.append(a)
        p.append(b)

print(d)
g.printSol(d, p, t, g.gateways)