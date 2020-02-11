root = None
parent = None

class Node:
    def __init__(self):
        self.keys = []
        self.n = 0 #número de espaços ocupados
        self.m = 2 #mínimo de chaves
        self.leaf = True
        self.children = []

        self.createChildren()

    def createChildren(self): 
        for i in range(self.n+1):
            self.children[i] = Node()

    def printPages(self):
        print(self.keys)
        if self.leaf == False:
            for i in range(len(self.children)):
                print(self.children[i].keys)
                if self.children[i].leaf == False: 
                    return self.children[i].printPages

    def search(self, x):
     
        if self.n == 0: 
            return 0 

        if self.leaf: 
            for i in range(self.n):
                print('t ', self.n)
                if self.keys[i] == x:
                    return self
        
        if not self.leaf:
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    return self.children[i].search(x)
                if i == self.n-1 and x > self.keys[i]:
                    return self.children[i+1].search(x)

        return 0

    def getParent(self, root):
        
        if root == self:
            return None

        else: 
            for i in len(root.children):
                if root.children[i] == self:
                    return root
            for i in len(root.children):
                return self.getParent(root.children[i])

    def split(self, x):
        global root 
        newNode = Node()
        parent = self.getParent(root)
        k = 0
        
        for i in range(self.m):
            newNode.keys.append(self.keys[0])
            newNode.n += 1
            self.n -= 1
            del(self.keys[0])
       
        if x < newNode.keys[0]:
            self.insertKey(x)
            k = self.keys[self.n-1]

        else: 
            newNode.insertKey(x)
            k = newNode.keys[0]

        if parent = None:
            newParent = Node()
            newParent.keys.append(x)
            newParent.children.append(newNode)
            newParent.children.append(self)
            root = newParent

        elif len(parent.keys) < parent.n:
            parent.insertKey(x)
            parent.children[parent.keys.index(x)-1] = newNode 
            parent.children[parent.keys.index(x)-1] = self

        else: 
            return parent.split(k)
        
    def insertKey(self, x):

        if self.n == 0: 
            self.keys.append(x)

        elif self.n == 1:
            if x < self.keys[0]:
                self.keys.insert(0, x)
            else: 
                self.keys.append(x)

        else: 
            for i in range(1, self.n):
                if x < self.keys[i]:
                    self.keys.insert(i-1, x)
                elif i == self.n-1 and x > self.keys[i]:
                    self.keys.append(x)          
        
        self.n += 1         

    def insertion(self, x):
        '''if self.search(x): 
            print("Elemento já está na árvore.")
            return 0 '''

        if len(self.keys) == self.n:
            self.leaf = False

        if self.leaf:
            if len(self.keys) < self.m * 2:
                self.insertKey(x)

            else: 
                self.split()
        
        else: 
            if x < self.keys[0]: 
                return self.children[0].insertion(x)
            elif x > self.keys[self.n-1]:
                return self.children[self.n]
            else:
                for i in range(1, self.n-1):
                    if x > self.keys[i] and x < self.keys[i+1]: 
                        return self.children[i].insertion(x)

root = Node()
for i in range(20): 
    x = int(input("N: "))
    root.insertion(x)
    root.printPages()