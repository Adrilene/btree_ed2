import random

root = None
parent = None

class Node:
    def __init__(self):
        self.keys = []
        self.n = 0 #número de espaços ocupados
        self.m = 2 #mínimo de chaves
        self.leaf = True
        self.children = []

        for i in range(self.m*2+1):
            self.children.append(None)

    def printPages(self, l):
        node = self
        print('{}: {}'.format(l, self.keys))
        i = 0

        print('{}:'.format(l), end="")
        for i in range(self.m*2+1):
            if node.children[i]:
                print(node.children[i].keys, end="")
            else: 
                print('[]', end="")
        print('\n')
        
    def search(self, x):
        
        if x in self.keys:
            return 1
        if not self.leaf:
            for i in range(len(self.children)):
                try: 
                    return self.children[i].search(x)
                except:
                    pass
        return 0

    def getParent(self, root):
        
        aux = None
        for i in range(len(root.children)):
            aux = root.children[i]
            if aux != None: 
                break
        
        if aux == None:
            return None 

        else:
            for i in range(len(root.children)):
                if root.children[i] == self:
                    return root
            
            for i in range(len(root.children)):
                if root.children[i] != None: 
                    return self.getParent(root.children[i])     

    def split(self, x):
        global root 
        newNode = Node()
        parent = self.getParent(root)
        k = 0

        for i in range(self.m): 
            newNode.insertKey(self.keys[0])
            self.n -= 1
            self.keys.pop(0)

        if x < self.keys[0]:
            newNode.insertKey(x)
            k = newNode.keys.pop(newNode.n-1)
            newNode.n -= 1

        else: 
            self.insertKey(x)
            k = self.keys.pop(0)
            self.n -= 1

        if parent == None:
            newParent = Node()
            newParent.insertKey(k)
            newParent.children[0] = newNode
            newParent.children[1] = self
            newParent.leaf = False
            root = newParent
            return 1

        elif parent.n < parent.m * 2:
            parent.insertKey(k)
            parent.children[parent.keys.index(k)] = newNode 
            parent.children[parent.keys.index(k)+1] = self
            return 1

        else: 
            return parent.split(k)
        
    def insertKey(self, x):
        if self.n == 0:
            self.keys.append(x)
        else: 
            for i in range(self.n):
                if x < self.keys[i]:
                    if x not in self.keys:
                        self.keys.insert(i, x)
                    break

                if i == self.n-1 and x > self.keys[i]:
                    if x not in self.keys:
                        self.keys.append(x)
                    break
        
        self.n = len(self.keys)
        return 1

    def insertion(self, x):
        global root 

        if self.leaf:
            if self.n < self.m * 2:
                self.insertKey(x)
                return 1

            else:
                return self.split(x)
        
        else:    
            for i in range(self.n):  
                
                if i == 0 and x < self.keys[i]:
                    if self.children[0] != None:
                        return self.children[0].insertion(x)
                    else: 
                        self.children[0] = Node()
                        self.children[0].insertKey(x)
                        return 1    

                if x > self.keys[i]:
                    if self.children[i+1] != None:
                        return self.children[i+1].insertion(x)
                    else: 
                        self.children[i+1] = Node()
                        self.children[i+1].insertKey(x)
                        return 1
                


root = Node()

for i in range(40): 
    random.seed()
    x = random.randint(0,100)
    if not root.search(x):
        print('Inserindo ', x)
        root.insertion(x)
        root.printPages(0)