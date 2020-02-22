import random

root = None
parent = None

class Node:
    def __init__(self):
        self.keys = []
        self.n = 0 #número de espaços ocupados
        self.m = 2 #mínimo de chaves
        self.leaf = True
        self.children = self.initChild()        
    
    def initChild(self):
        children = []
        for i in range(self.m*2+1):
            children.append(None)
        return children

    def printPages(self):
        stack = []
        stack.append(self)

        while len(stack) > 0:
            count = len(stack)
            while count > 0:
                if stack[0]: 
                    temp = stack.pop(0)
                else: 
                    temp = None
                try: 
                    print(temp.keys, end = '')
                except: 
                   print('[    ]', end = '')

                if temp: 
                    for i in range(len(temp.children)):
                        if temp.children[i]:
                            stack.append(temp.children[i])
                    
                count -= 1
            print(' ')

        print('\n')
            
    def search(self, x):

        if x in self.keys:
            return 1
        
        elif not self.leaf:
            for i in range(self.n):
                if i == 0 and x < self.keys[0]:
                    try: 
                        return self.children[0].search(x)
                    except:
                        return 0 
                if i < self.n-1 and x > self.keys[i] and x < self.keys[i+1]:
                    try: 
                        return self.children[i+1].search(x)
                    except:
                        return 0
                if i == self.n-1 and x > self.keys[i]:
                    try:
                        return self.children[i+1].search(x)
                    except:
                        return 0 
        return 0 

    def getParent(self, parent, x):
        if parent.leaf: 
            return None
        
        if self in parent.children:
            return parent
        
        for i in range(parent.n):
            if i == 0 and x < parent.keys[i]:
                return self.getParent(parent.children[i], x)
            if i < parent.n-1 and x > parent.keys[i] and x < parent.keys[i+1]:
                return self.getParent(parent.children[i+1], x)
            if i == parent.n-1 and x > parent.keys[i]:
                return self.getParent(parent.children[i+1], x)

    def split(self, x):
        global root 
        newNode = Node()
        parent = self.getParent(root,x)
        k = 0

        self.insertKey(x)
        k = self.keys.pop(self.m)
        self.n -= 1

        newNode.keys = self.keys[0:self.m]
        self.keys = self.keys[self.m:]
        self.n = newNode.m
        newNode.n = newNode.m
        
        if not self.leaf:
            newNode.children = self.children[0:self.m+1]
            self.children = self.children[self.m+1:]

            for i in range(self.m, self.m*2):
                self.children.append(None)
                newNode.children.append(None)
            
            newNode.leaf = False

        if parent == None:
            newParent = Node()
            newParent.insertKeyParent(k, newNode, self)
            newParent.leaf = False
            root = newParent
            return 1

        root.findPlace(k, parent, newNode, self)
        return 1
                   
    def findPlace(self, k, parent, childLeft, childRight):       

        if self == parent:
            if root.n < root.m*2:
                root.insertKeyParent(k, childLeft, childRight)
                return 1
            else:
                self.insertKey(k)
                self.children.insert(self.children.index(childRight), childLeft)
                root.split(k)
                return 1
    
        if parent in self.children: 
            self.children[self.children.index(parent)].insertKeyParent(k, childLeft, childRight)     
            return 1
        
        for i in range(self.n):
            if i == 0 and k < self.keys[i]:
                return self.children[i].findPlace(k, parent, childLeft, childRight)
            if i < self.n-1 and k > self.keys[i] and k < self.keys[i+1]:
                return self.children[i+1].findPlace(k, parent,childLeft, childRight)
            if i == self.n-1 and k > self.keys[i]:
                return self.children[i+1].findPlace(k, parent, childLeft, childRight)

    def insertKeyParent(self, x, childLeft, childRight):
        
        global root 

        self.insertKey(x)
        l = self.keys.index(x)
        listA = self.children

        listA.insert(l, childLeft)
        listA.insert(l+1, childRight)

        for i in listA:
            if listA.count(i) > 1 and i != None: 
                listA.remove(i)
                pass

        self.children = listA  
     
    def insertKey(self, x):
       
        if self.n == 0:
            self.keys.append(x)
        else: 
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    self.keys.insert(i, x)
                    break
                if i < self.n-1 and x > self.keys[i] and x < self.keys[i+1]:
                    self.keys.insert(i+1, x)
                    break
                if i == self.n-1 and x > self.keys[i]:
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
                        self.children[i].insertKey(x)   
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
while c<50: 
    random.seed()
    x = random.randint(0,50)
    if not root.search(x):
        print('Inserindo ', x)
        if root.insertion(x):
            c += 1
        root.printPages()