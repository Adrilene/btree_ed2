root = None
parent = None

class Node:
    def __init__(self):
        self.keys = []
        self.n = 0 #número de espaços ocupados
        self.m = 2 #mínimo de chaves
        self.leaf = True
        self.children = []

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
         
        for i in range(len(root.children)):
            if root.children[i] == self:
                return root
        for i in range(len(root.children)):
            if root.children[i].leaf == False:
                return self.getParent(root.children[i])

    def split(self, x, parent):
        newNode = Node()
        
        for i in range(self.m):
            newNode.keys.append(self.keys[0])
            newNode.n += 1
            self.n -= 1
            del(self.keys[0])
        k = 0
        if x < self.keys[0] and x > newNode.keys[newNode.n-1]:
            newNode.insertKey(x)
            k = newNode.keys[newNode.n-1]
            del(newNode.keys[newNode.n-1])
        else: 
            self.insertKey(x)
            k = self.keys[0]
            del(self.keys[0])
        if parent == None: 
            global root
            newRoot = Node()
            newRoot.keys.append(k)
            newRoot.children.append(newNode)
            newRoot.children.append(self)
            newRoot.n = 1
            newRoot.leaf = False
            root = newRoot
        
        elif parent.n < parent.m*2:
            parent.insertKey(k)
            parent.children.insert(parent.keys.index(k), newNode)
            parent.children.insert(parent.keys.index(k)+1, self)
            parent.leaf = False

        elif parent.n == parent.m*2:
            parent.split(k, parent.getParent(root))
        

    def insertKey(self, x):
        
        if self.n == 0: 
            self.keys.append(x)
            self.n+=1

        elif self.n == 1:
            if x < self.keys[0]:
                self.keys.insert(0, x)
            else: 
                self.keys.append(x)

        else: 
            for i in range(self.n):
                if x < self.keys[i]:
                    self.keys.insert(i-1, x)
                if i == self.n-1 and x > self.keys[i]:
                    self.keys.append(x)          
        self.n += 1         

    def insertion(self, x):
        global parent 

        '''if self.search(x): 
            print("Elemento já está na árvore.")
            return 0 '''

        if self.leaf == False: 
            parent = self
            print(self.n)
            for i in range(self.n):
                if i == 0 and x < self.keys[0]:
                    print('if 1')
                    return self.children[0].insertion(x)
                if i == self.n-1 and x > self.keys[i]:
                    print('if 2')
                    if not self.children[i+1]:
                        return 0 
                    return self.children[i+1].insertion(x)
                if x > self.keys[i] and x < self.keys[i+1]:
                    print('if 3')
                    return self.children[i].insertion(x)

        else: 
            if self.n == self.m*2:
                self.split(x, parent)

            elif self.n<self.m*2: 
                self.insertKey(x)
            return self

root = Node()
for i in range(20): 
    x = int(input("N: "))
    root.insertion(x)
    root.printPages()