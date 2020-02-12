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
        
        if root == self:
            return None

        else: 
            for i in range(len(root.children)):
                if root.children[i] == self:
                    return root
            for i in range(len(root.children)):
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

        if x < self.keys[0]:
            newNode.insertKey(x)
            k = newNode.keys[newNode.n-1]
            del(newNode.keys[newNode.n-1])
            newNode.n -= 1

        else: 
            self.insertKey(x)
            k = self.keys[0]
            del(self.keys[0])
            self.n -= 1

        if parent == None:
            newParent = Node()
            newParent.keys.append(k)
            newParent.children[0] = newNode
            newParent.children[1] = self
            newParent.leaf = False
            root = newParent

        elif parent.n < parent.m * 2:
            parent.insertKey(k)
            parent.children[parent.keys.index(k)] = newNode 
            parent.children[parent.keys.index(k)+1] = self

        else: 
            return parent.split(k)
        
    def insertKey(self, x):
        if self.n == 0:
            self.keys.append(x)
        else: 
            for i in range(self.n):
                if x < self.keys[i]:
                    self.keys.insert(i, x)
                    break

                if i == self.n-1 and x > self.keys[i]:
                    self.keys.append(x)
                    break
        
        self.n += 1
                        

    def insertion(self, x):
        global root 

        if self.leaf:
            if self.n < self.m * 2:
                self.insertKey(x)

            else:
                self.split(x)
        
        else:              

            for i in range(self.n):
                if x < self.keys[i]:
                    if self.children[i] != None:
                        if self.children[i].n < self.children[i].m*2:
                            self.children[i].insertKey(x)
                            return 1
                        else: 
                            return self.children[i].insertion(x)
                    else: 
                        self.children[i] = Node()
                        self.children[i].insertKey(x)
                        return 1
                
                if i == self.n-1 and x > self.keys[i]:
                    if self.children[self.n] != None:
                        if self.children[self.n].n < self.children[self.n].m*2:
                                self.children[self.n].insertKey(x)
                                return 1
                        else: 
                            return self.children[self.n].insertion(x)
                    else: 
                        self.children[self.n] = Node()
                        self.children[self.n].insertKey(x)
                        return 1
                    

root = Node()
for i in range(20): 
    random.seed()
    x = random.randint(0,40)
    print(x)
    if not root.search(x):
        root.insertion(x)

root.printPages(0)