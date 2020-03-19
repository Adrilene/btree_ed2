import random

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
        if not self.leaf: 
            last_child = self.children[self.n]
            if last_child: 
                return last_child.mv_nearest_element()
            last_child = self.children[self.n-1]
            return last_child.mv_nearest_element()
        
        else: 
            return self

    def redistribute(self, brother):
        idx = self.parent.children.index(self)

        if self.parent.children.index(brother) < idx:
            idx-= 1
        
        parent_element = self.parent.keys.pop(idx)
        self.parent.n -= 1
        self.insertKey(parent_element)
        self.parent.insertKey(brother.keys.pop(-1))
        brother.n -= 1

        print(f'Redistribuí. Pai: {self.parent.keys}. Irmão: {brother.keys}. Eu: {self.keys}')

    def join_brothers(self, brother): 
        global root 

        idx = self.parent.children.index(self)
        if self.parent.children.index(brother) < idx:
            idx -= 1
        
        parent_element = self.parent.keys.pop(idx)
        self.parent.n -= 1

        if parent_element > brother.keys[0]:
            brother.keys.extend(self.keys)
            brother.n += self.n
            brother.insertKey(parent_element)
            if not self.leaf:
                brother.children = brother.children[:self.n+1]
                for i in self.children:
                    if i:
                        brother.children.append(i)
                for i in range(self.n+1, 2 * self.m):
                    brother.children.append(None)

            self = brother
            
        else:
            self.keys.extend(brother.keys)
            self.n += brother.n
            self.insertKey(parent_element)

            if not brother.leaf:
                self.children = self.children[:self.n+1]
                for i in brother.children: 
                    if i: 
                        self.children.append(i)
                for i in range(self.n+1, 2*self.m):
                    self.children.append(None)
            
        self.parent.children.remove(brother)
        del brother
        self.parent.children.append(None)
        if self.parent == root and root.n == 0:
            root = self

        print(f'Concatenei. Pai: {self.parent.keys}. Eu: {self.keys}')

    def balance_page(self):
        """
            Balanceia a pagina, se tiver inferior ao valor a m
        """
        print(f'Balance function keys: {self.keys}, n: {self.n}')
        global root
        try:
            my_idx = self.parent.children.index(self)
        except Exception:
            print('Nada feito')
            return
        
        if self.n == 0: 
            self.parent.children[my_idx] = None
            del self
            return

        if self.n < self.m and self != root:
            
            left_brother, right_brother = None, None
            try:
                left_brother = self.parent.children[my_idx - 1]
                # print(f'left brother.n {left_brother.n}')
            except (IndexError, AttributeError):
                pass
            try:
                right_brother = self.parent.children[my_idx + 1]
                # print(f'right brother.n {right_brother.n}')
            except (IndexError, AttributeError):
                pass

            if my_idx != 0:

                if left_brother and left_brother.n + self.n >= 2 * self.m:
                    self.redistribute(left_brother)

                elif right_brother and right_brother.n + self.n >= 2 * self.m:
                    self.redistribute(right_brother)

                else:
                    if left_brother and left_brother.n + self.n < 2 * self.m:
                        self.join_brothers(left_brother)
                        self.parent.balance_page()

                    elif right_brother and right_brother.n + self.n < self.m * 2:
                        self.join_brothers(right_brother)
                        self.parent.balance_page()
            
            else:
    
                if right_brother and right_brother.n + self.n >= 2 * self.m:
                    self.redistribute(right_brother)

                if right_brother and right_brother.n + self.n < self.m * 2:
                    self.join_brothers(right_brother)

        has_child = False
        
        for i in self.children:
            if i:
                has_child = True

        if not has_child:
            self.leaf = False
 
    def removes(self, element):
        global root
        
        if self.leaf:
            self.removesKey(element)
            self.balance_page()

        else:
            nearest_child = self.children[0].mv_nearest_element()
            nearest_element = nearest_child.keys[-1]
            nearest_child.removesKey(nearest_element)
            self.removesKey(element)
            self.insertKey(nearest_element)
            nearest_child.balance_page()

        if self.n < self.m:
            self.balance_page()


    def removesKey(self, x):
        self.keys.remove(x)
        self.n -= 1

root = Page()
c = 0
menu = 0
while menu != 3:
    menu = int(input(
        "Digite 1 para o método interativo, 2 para o método automático, e 3 para sair."))
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
        while c < 50:
            random.seed()
            x = random.randint(0, 50)
            a.append(x)
            # Insere apenas itens não repetidos
            if not root.search(x):
                print('Inserindo ', x)
                if root.insertion(x):
                    c += 1
                #root.printPages()
                print(c, ' elementos.')
        count = 0
        root.printPages()
        for i in a:
            count += 1
            page = root.search(i)
            if page: 
                print(f'removes {i}')
                page.removes(i)
                root.printPages()
            a.remove(i)
            if count == 50:
                break

        
