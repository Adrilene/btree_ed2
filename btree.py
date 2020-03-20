import random
from PyQt5.QtWidgets import QApplication
from btree_interface import Window, execute_interface
import os
import sys

root = None


class Page:
    def __init__(self):
        self.keys = []
        self.n = 0  # número de espaços ocupados
        self.m = 2  # mínimo de chaves
        self.leaf = True
        self.children = self.initChild()
        self.parent = None

    def initChild(self):
        children = []
        for i in range(self.m * 2 + 1):
            children.append(None)
        return children

    def printPages(self):
        stack = []
        stack.append(self)  # Adiciona a página atual em stack
        countK = 0
        while len(stack) > 0:
            count = len(stack)
            while count > 0:  # Percorre as páginas contidas em stack
                if stack[0]:
                    # temp recebe a primeira página de stack, e a remove de
                    # stack
                    temp = stack.pop(0)
                else:
                    temp = None
                try:
                    print(temp.keys, end='')
                    countK += temp.n
                except BaseException:
                    print('[    ]', end='')

                if temp:
                    # Percorre as páginas filhas de temp, e as adiciona em
                    # stack.
                    for i in range(len(temp.children)):
                        if temp.children[i]:
                            stack.append(temp.children[i])
                count -= 1
            print(' ')

        print('\n')
        print(f'{countK} chaves')

    def search(self, x):

        if x in self.keys:  # Retorna verdadeiro se x está contido na página atual.
            return self

        # Caso não esteja e a página não for folha(página interna da árvore).
        elif not self.leaf:
            for i in range(self.n):  # Quantidade de itens em self.keys.
                # Caso x seja menor que a primeira chave em self.keys.
                if i == 0 and x < self.keys[0]:
                    try:
                        return self.children[0].search(x)
                    except BaseException:
                        return 0
                # Caso x esteja entre qualquer valor em self.keys.
                if i < self.n - \
                        1 and x > self.keys[i] and x < self.keys[i + 1]:
                    try:
                        return self.children[i + 1].search(x)
                    except BaseException:
                        return 0
                # Caso x seja maior que o último item em self.keys.
                if i == self.n - 1 and x > self.keys[i]:
                    try:
                        return self.children[i + 1].search(x)
                    except (IndexError, AttributeError):
                        return 0
        return 0

    def split(self, x):
        global root
        newPage = Page()
        k = 0

        self.insertKey(x)
        k = self.keys.pop(self.m)
        self.n -= 1

        # Recebe os itens "esquerdos". Logo self fica com os itens "direitos".
        newPage.keys = self.keys[0:self.m]
        newPage.parent = self.parent  # Pega o mesmo pai de self.
        self.keys = self.keys[self.m:]
        self.n = self.m
        newPage.n = newPage.m

        if not self.leaf:  # Caso self não seja folha, reorganizamos os filhos.
            newPage.children = self.children[0:self.m + 1]
            self.children = self.children[self.m + 1:]
            for filho in range(self.m + 1):
                self.children[filho].parent = self
                newPage.children[filho].parent = newPage

            # Faz com que self e newPage tenham 2m+1 filhos.
            for i in range(self.m, self.m * 2):
                self.children.append(None)
                newPage.children.append(None)

            newPage.leaf = False

        if self.parent is None:
            newParent = Page()  # Novo pai de ambas as páginas(self e newPage)
            newParent.leaf = False
            newParent.insertKeyParent(k, newPage, self)
            # Como não existe nenhuma página acima de self, seu pai será o mais
            # alto, e consequentemente a root.
            root = newParent
            self.parent = root
            newPage.parent = root
            return 1

        if self.parent.n < self.m * 2:  # Caso o pai de self ainda possua espaços disponíveis
            self.parent.insertKeyParent(k, newPage, self)
            return 1

        if self.parent.n >= self.m * 2:  # Caso o pai de self não possua espaços disponíveis
            self.parent.children.insert(
                self.parent.children.index(self), newPage)
            return self.parent.split(k)

        return 1

    def insertKeyParent(self, x, childLeft, childRight):

        global root

        self.insertKey(x)
        l = self.keys.index(x)  # l recebe o índice onde foi inserido x.
        listA = self.children

        listA.insert(l, childLeft)
        listA.insert(l + 1, childRight)

        for i in listA:
            if listA.count(i) > 1 and i is not None:
                listA.remove(i)
                pass

        self.children = listA

    def insertKey(self, x):

        if self.n == 0:  # Se ainda não houverem chaves na página.
            self.keys.append(x)
        else:
            # Percorre as chaves de self a fim de identificar onde inserir x.
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    self.keys.insert(i, x)
                    break
                if i < self.n - \
                        1 and x > self.keys[i] and x < self.keys[i + 1]:
                    self.keys.insert(i + 1, x)
                    break
                if i == self.n - 1 and x > self.keys[i]:
                    self.keys.append(x)
                    break

        self.n = len(self.keys)  # Atualiza o valor de self.n
        return 1

    def insertion(self, x):
        global root

        if self.leaf:
            # Se ainda houver espeço na página, insere o  item.
            if self.n < self.m * 2:
                self.insertKey(x)
                return 1
            else:  # Caso contrário, chama split da página atual.
                return self.split(x)
        else:
            for i in range(self.n):
                if i == 0 and x < self.keys[i]:
                    if self.children[i]:
                        return self.children[i].insertion(x)
                    else:
                        self.children[i] = Page()
                        self.children[i].parent = self
                        self.children[i].insertKey(x)
                        return 1
                if i < self.n - \
                        1 and x > self.keys[i] and x < self.keys[i + 1]:
                    if self.children[i + 1]:
                        return self.children[i + 1].insertion(x)
                    else:
                        self.children[i + 1] = Page()
                        self.children[i + 1].parent = self
                        self.children[i + 1].insertKey(x)
                        return 1
                if i == self.n - 1 and x > self.keys[i]:
                    if self.children[i + 1]:
                        return self.children[i + 1].insertion(x)
                    else:
                        self.children[i + 1] = Page()
                        self.children[i + 1].parent = self
                        self.children[i + 1].insertKey(x)
                        return 1
        return 0

    def mv_nearest_element(self):
        """
            Retorna o maior valor da subarvore esquerda
        """ 
        
        if self.leaf: 
            return self
        
        last_child = self.children[0]
        for i in range(1, len(self.children) - 1):
            if self.children[i+1]:
                last_child = self.children[i+1]

        return last_child.mv_nearest_element()

    def redistribute(self, brother):
        idx = self.parent.children.index(self)

        if self.parent.children.index(brother) < idx:
            if idx >= self.parent.n:
                idx=self.parent.n-1
            else:
                idx-= 1
        
        parent_element = self.parent.keys.pop(idx)
        self.parent.n -= 1
        self.insertKey(parent_element)
        self.parent.insertKey(brother.keys.pop(-1))
        brother.n -= 1

    def join_brothers(self, brother): 
        global root 

        idx = self.parent.children.index(self)

        if self.parent.children.index(brother) < idx:
            if idx >= self.parent.n:
                idx=self.parent.n-1
            else:
                idx-= 1
            
            parent_element = self.parent.keys.pop(idx)
            self.parent.n -= 1
            brother.keys.extend(self.keys)
            brother.n = len(brother.keys)
            brother.insertKey(parent_element)
            self.parent.insertKey(brother.keys.pop(-1))    
            brother.n -= 1
            
            if not self.leaf:
                new_children = brother.children
                new_children.extend(self.children)
                j = 0
                for i in range(len(new_children)):
                    if new_children[i]:
                        new_children[i].parent = self
                        brother.children[j] = new_children[i]
                        j+=1
                    
                for i in range(brother.n, 2*brother.m+1):
                    brother.children.append(None)

                for i in self.children:
                    if i:
                        i.parent = self

            self.keys = brother.keys
            self.children = brother.children
            self.n = brother.n

        else:
            
            parent_element = self.parent.keys.pop(idx)
            self.parent.n -= 1
            self.keys.extend(brother.keys)
            self.n = len(self.keys)
            self.insertKey(parent_element)
            self.parent.insertKey(brother.keys.pop(-1))
            brother.n -= 1

            if not brother.leaf:
                new_children = self.children
                new_children.extend(brother.children)

                j = 0
                for i in range(len(new_children)):
                    if new_children[i]:
                        new_children[i].parent = self
                        brother.children[j] = new_children[i]
                        j+=1
                    
                for i in range(self.n, 2*self.m+1):
                    self.children.append(None)
            
                for i in self.children:
                    if i:
                        i.parent = self
            
        self.parent.children.remove(brother)
        del brother
        if len(self.parent.children) < self.n:
            self.parent.children.append(None)
        #self.parent.children[idx] = self
        
        if self.parent == root and root.n == 0:
            root = self

    def balance_page(self):
        """
            Balanceia a pagina, se tiver inferior ao valor a m
        """
        global root
        
        try:
            my_idx = self.parent.children.index(self)
        except Exception:
            print('Nada feito')
            return
        
        if self.n == 0: 
            self.parent.children.remove(self)
            del self
            return

        if self.n < self.m and self != root:
            left_brother, right_brother = None, None
            try:
                left_brother = self.parent.children[my_idx - 1]
            except (IndexError, AttributeError):
                pass
            try:
                right_brother = self.parent.children[my_idx + 1]
            except (IndexError, AttributeError):
                pass
            
            if left_brother and left_brother.n + self.n >= 2 * self.m:
                self.redistribute(left_brother)

            elif right_brother and right_brother.n + self.n >= 2 * self.m:
                self.redistribute(right_brother)

            elif left_brother and left_brother.n + self.n < 2 * self.m:
                self.join_brothers(left_brother)
                self.parent.balance_page()

            elif right_brother and right_brother.n + self.n < self.m * 2:
                self.join_brothers(right_brother)
                self.parent.balance_page()
            
            
        has_child = False
        
        for i in self.children:
            if i:
                has_child = True

        if not has_child:
            print('Sou folha')
            self.leaf = True
        else:
            self.leaf = False
    
    def removes(self, element):
        global root

        if self.leaf:
            print('remove folha')
            self.removesKey(element)
            self.balance_page()

        else:
            print(f'filho do meio: {self.keys}. {self.children[0]} {self.leaf}')
            idx_r = self.keys.index(element)
            nearest_child = self.children[idx_r].mv_nearest_element()
            nearest_element = nearest_child.keys[-1]
            nearest_child.keys.remove(nearest_element)
            nearest_child.n -= 1
            self.keys.remove(element)
            self.n -= 1
            self.insertKey(nearest_element)
            print(f'elemento inserido: {nearest_element} em {self.keys}')
            nearest_child.balance_page()

        if self.n < self.m:
            self.balance_page()
 

    def removesKey(self, x):
        self.keys.remove(x)
        self.n -= 1

    def get_pages_and_parents(self):
        stack = []
        stack.append(self) #Adiciona a página atual em stack
        pages = set()
        i = 0
        while len(stack) > 0:
            count = len(stack)
            while count > 0: #Percorre as páginas contidas em stack
                if stack[0]: 
                    temp = stack.pop(0) #temp recebe a primeira página de stack, e a remove de stack
                    pages.add(temp)
                    
                else: 
                    temp = None
                if temp: 
                    for i in range(len(temp.children)): #Percorre as páginas filhas de temp, e as adiciona em stack.
                        if temp.children[i]:
                            stack.append(temp.children[i])
                count -= 1

        pages_to_interface = []
        first_execute = True
        while True:
            if len(pages_to_interface) == len(pages):
                break
            for page in pages:
                if not page.parent and first_execute:
                    pages_to_interface.append(['root', page.keys, 0])
                    first_execute = False
                for keys in pages_to_interface:        
                    if page.parent != None:
                        complete_page = [keys[1], page.keys, keys[2]+1]
                        if page.parent.keys == keys[1] and complete_page not in pages_to_interface:
                            pages_to_interface.append(complete_page)
        
        return pages_to_interface

root = Page()
c = 0
menu = 0
if os.path.exists("data_to_interface.txt"):
    os.remove("data_to_interface.txt")
interface_file = open('data_to_interface.txt', 'a')

while menu != 3:
    print('=== B Tree ===')
    print('Digite uma das opções:')
    print('(1) para o método interativo')
    print('(2) para o método automático')
    print('(3) para sair')
    menu = int(input())

    if menu == 1:
        resposta = 0
        while(resposta != 99):
            resposta = int(input(
                "Digite 1 para adicionar um elemento, 2 para buscar a página do elemento, ou 99 para sair: "))
            if resposta == 1:
                chave = int(input("Digite a chave à ser adicionada: "))
                print('Inserindo ', chave)
                root.insertion(chave)
                root.printPages()
                c += 1
                print(c, " elementos.")
            if resposta == 2:
                chave = int(input("Digite a chave à ser buscada: "))
                pagina = root.search(chave)
                print("Chaves da página: ", pagina.keys)
                count = 0
                if pagina.parent:
                    print("Chaves do pai: ", pagina.parent.keys)
                for filho in pagina.children:
                    if filho:
                        print("Chaves do", count, "filho: ", filho.keys)
                    count += 1
    if menu == 2:
        a = []
        while c < 40:
            random.seed()
            x = random.randint(0, 50)
            a.append(x)
            # Insere apenas itens não repetidos
            if not root.search(x):
                print('Inserindo ', x)
                if root.insertion(x):
                    c += 1
                root.printPages()
                print(c, ' elementos.')
                if c == 40:
                    pages_parents = root.get_pages_and_parents()
                    interface_file.writelines(str(root.m) + ';')
                    for page in pages_parents:
                        interface_file.writelines(str(page) + ';')
                    interface_file.close()
                    execute_interface()
        
        count = 0

        '''root.printPages()
        x = a.pop(0)
        count = 0
        while len(a) > 0:
            page = root.search(x)
            if page: 
                print(f'Removendo {x}')
                page.removes(x)
                count += 1
                root.printPages()
            x = a.pop(0)
        print(f'{count} removidos')'''
