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

    def printPages(self):
        
        for i in range(self.n):
            if not self.leaf:
                if self.children[i]:
                    self.children[i].printPages()
                else:
                    print('[    ]')
        print(self.keys)
        
        print('\n')

        if not self.leaf: 
            if not self.children[i]:
                print('[    ]', end = '')
            else:
                self.children[i].printPages()
            
    def search(self, x):

        if x in self.keys:
            return 1
        if not self.leaf:
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    try:
                        return self.children[i].search(x)
                    except:
                        pass
                
                if i < self.n-1 and x > self.keys[i] and x < self.keys[i+1]:
                    try:
                        return self.children[i+1].search(x)
                    except:
                        pass

                if i == self.n-1 and x > self.keys[i]:
                    try:
                        return self.children[i+1].search(x)
                    except:
                        pass

    def getParent(self, parent, x):
        
        if parent.leaf:
            return None

        elif self in parent.children:
            return parent
        
        else:
            for i in range(len(parent.children)):
                if parent.children[i] and not parent.children[i].leaf:
                    return parent.children[i].getParent(parent.children[i], x)


    def split(self, x):
        global root 
        newNode = Node()
        parent = self.getParent(root, self)
        k = 0

        self.insertKey(x)
        k = self.keys.pop(int(self.n/2))
        self.n -= 1

        for i in range(self.m):
            if not self.leaf:
                if self.children[0]:
                    newNode.leaf = False
                    newNode.children[0] = self.children.pop(0)

            newNode.insertKey(self.keys.pop(0))
            self.n -= 1

        if parent == None:
            newParent = Node()
            newParent.insertKeyParent(k, newNode, self)
            newParent.leaf = False
            root = newParent
            return 1

        elif parent.n < parent.m * 2:
            parent.insertKeyParent(k, newNode, self)
            return 1

        else: 
            return parent.split(k)
        
    
    def insertKeyParent(self, x, childLeft, childRight):

        self.insertKey(x)
        l = self.keys.index(x)
        listA = []
        
        if self.children[l]:
            for i in range(l, len(self.children)):
                listA.append(self.children[i])

        self.children[l] = childLeft            
        self.children[l+1] = childRight

        if len(listA) > 0:
            while len(listA) > 0 and l+1 < len(self.children):
                self.children[l+1] = listA.pop(0)
                l += 1
    
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
                    if self.children[i]: 
                        return self.children[i].insertion(x)
                    else: 
                        self.children[i] = Node()
                        self.children.insertKey(x)
                        return 1
                
                if i < self.n-1 and x > self.keys[i] and x < self.keys[i+1]:
                    if self.children[i+1]:
                        return self.children[i+1].insertion(x)
                    else: 
                        self.children[i+1] = Node()
                        self.children[i+1].insertKey(x)
                        return 1

                if i == self.n-1 and x > self.keys[i]:
                    if self.children[i+1]:
                        return self.children[i+1].insertion(x)
                    else: 
                        self.children[i+1] = Node()
                        self.children[i+1].insertKey(x)
                        return 1

                    
        return 0
                
root = Node()

c = 0

while True: 
    random.seed()
    x = random.randint(0,50)
    if not root.search(x):
        print('Inserindo ', x)
        if root.insertion(x):
            c += 1
        root.printPages()
    if c == 24:
        break

print(c, ' elementos. ')