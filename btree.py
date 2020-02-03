root = None

class Node:
    def __init__(self):
        self.keys = []
        self.n = 0 #número de espaços ocupados
        self.m = 2 #mínimo de chaves
        self.leaf = True
        self.children = []

    def printPages(self):
        print(self.keys)
        print(self.children)
        for i in range(len(self.children)):
            return self.children[i].printPages()

    def search(self, x):
     
        if self.n == 0: 
            return 0 

        if self.leaf: 
            for i in range(self.n):
                if self.keys[i] == x:
                    return self
        
        if not self.leaf:
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    return self.children[i].search(x)
                if i == self.n-1 and x > self.keys[i]:
                    return self.children[i+1].search(x)

        return 0

    def split(self, x, parent):
        newNode = Node()
        for i in range(int(self.n/2)):
            newNode.keys.append(self.keys[i])
            newNode.n += 1
            self.n -= 1
            del(self.keys[i])
        
        for i in range(self.n):
            if i == 0 and x < self.keys[i]:
                self.keys.insert(0, x)

            elif i == self.n-1: 
                self.keys.append(x)
            
            elif i > self.keys[i] and i < self.keys[i+1]:
                self.keys.insert(i, x)

        k = self.keys[self.n-1]
        del(self.keys[self.n-1])

        if parent == None: 
            global root
            root.n = 1  
            root.keys.append(k)
            root.children.append(newNode)
            root.children.append(self)
            root.leaf = False
        
        elif parent.n < parent.m*2:
            parent.insertKey(k)

        elif parent.n == parent.m*2:
            parent.split(k)

    def insertKey(self, x):
        print('insert ', x)
        for i in range(self.n):
            if i == 0 and x < self.keys[i]:
                self.keys.insert(0, x)
                self.n += 1
            elif i == self.n-1: 
                self.keys.append(x)
                self.n += 1
            elif x > self.keys[i] and x < self.keys[i+1]:
                self.keys.insert(i+1,x)
                self.n += 1

    def insertion(self, x):
        '''if self.search(x): 
            return 0'''
        
        parent = None

        if self.n == 0:
            self.n += 1
            self.keys.append(x)

        if self.leaf: 
            if self.n == self.m*2:
                self.split(x, parent)

            else: 
                self.insertKey(x)
            return self

        if not self.leaf: 
            for i in range(self.n):
                if i == 0 and x < self.keys[i] and self.children[i]:
                    parent = self
                    return self.children[i].insertion(x)
                if i == self.n-1 and x > self.keys[i] and self.children[i+1]:
                    parent = self
                    return self.children[i+1].insertion(x)
        

root = Node()
for i in range(7): 
    x = int(input("N: "))
    root.insertion(x)

root.printPages()