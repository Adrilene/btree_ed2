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

    def borrow(self, my_idx, parent, brother):
        try:
            new_element = parent.keys[my_idx - 1]
            print(f'new element {new_element}')
        except IndexError:
            return
        parent.keys[my_idx - 1] = brother.keys[-1]
        # print(f'parent now {parent.keys[my_idx - 1]}')
        substituito = brother.mv_nearest_element()
        # print(f' substituito {substituito} newelement {new_element}')
        if not substituito or substituito == new_element:
            print('deleting {brother.keys[-1]}')
            brother.keys.remove(parent.keys[my_idx - 1])
            brother.n -= 1
        self.keys.insert(0, new_element)
        self.n += 1
        return True

    def borrow_right(self, my_idx, parent, brother):
        try:
            new_element = parent.keys[my_idx + 1]
        except IndexError:
            return
        parent.keys[my_idx + 1] = brother.keys[0]
        substituito = brother.mv_nearest_element()
        if not substituito:
            del brother.keys[0]
            brother.n -= 1
        self.keys.append(new_element)
        self.n += 1
        return True

    # def join_pages(self, element, element_idx, page1, page2):
    #     del self.keys[element_idx]
    #     page2.n -= 1
    #     page1.keys.extend(page2.keys)
    #     page1.children.extend(page2.children)
    #     self.children.remove(page2)
    #     del page2

    def mv_nearest_element(self):
        new_nearest_element = None
        nearest_element = self.keys[-1]
        last_child = self.children[self.n]
        if last_child:
            new_nearest_element = last_child.mv_nearest_element()
        if not new_nearest_element and nearest_element:
            self.removesKey(self.keys[-1])
            self.balance_page()
            return nearest_element
        return new_nearest_element if new_nearest_element else nearest_element

    def balance_page(self):
        print(f'Balance function keys: {self.keys}, n: {self.n}')
        global root
        if self.n < self.m:
            my_idx = self.parent.children.index(self)
            if my_idx != 0:
                try:
                    left_brother = self.parent.children[my_idx - 1]
                except IndexError:
                    pass

                if left_brother and left_brother.n + self.n >= 2 * self.m:
                    print(f'my_idx {my_idx} and self.parent.keys: {self.parent.keys}')
                    parent_element = self.parent.keys.pop(my_idx - 1)  # noqa: E501
                    self.parent.n -= 1
                    self.parent.insertKey(left_brother.keys.pop(-1))  # noqa: E501
                    self.insertKey(parent_element)

                else:
                    left_brother.keys.extend(self.keys)
                    self.keys = left_brother
                    self.parent.children.remove(left_brother)
                    print(f'my_idx {my_idx} and self.parent.keys: {self.parent.keys}')
                    # element_to_pop = self.parent.keys[my_idx]
                    self.parent.n -= 1
                    self.insertKey(self.parent.keys.pop(my_idx - 1))  # noqa: E501 MUDEI AGR
                    if self.parent == root and self.parent.n == 0:
                        root = self
                        return
                    self.parent.balance_page()
            else:
                try:
                    right_brother = self.parent.children[my_idx + 1]
                except IndexError:
                    pass
                if right_brother and right_brother.n + self.n >= 2 * self.m:
                    print(f'my_idx {my_idx} and self.parent.keys: {self.parent.keys}')
                    parent_element = self.parent.keys.pop(my_idx)  # noqa: E501
                    self.parent.n -= 1
                    self.parent.insertKey(right_brother.keys.pop(0))  # noqa: E501
                    self.insertKey(parent_element)

                else:
                    self.keys.extend(right_brother.keys)
                    self.parent.children.remove(right_brother)
                    print(f'my_idx {my_idx} and self.parent.keys: {self.parent.keys}')
                    self.parent.n -= 1
                    self.insertKey(self.parent.keys.pop(my_idx))  # noqa: E501
                    self.parent.balance_page()

    def removes(self, element):
        global root
        if self.leaf:
            self.removesKey(element)
            self.balance_page()

        else:
            # if self == root:
            #     new_element = self.mv_nearest_element()
            #     self.insertKey(new_element)
            #     return
            element_idx = self.keys.index(element)
            left_child = self.children[element_idx]
            self.removesKey(element)
            new_element = left_child.mv_nearest_element()
            self.insertKey(new_element)

        # if self.n - 1 >= self.m or self.n < self.m or not self.parent:
        #     if self.leaf:
        #         print('deleting item in leaf')
        #         del self.keys[element_idx]
        #         self.n -= 1
        #     else:
        #         try:
        #             left_child = self.children[element_idx]
        #             right_child = self.children[element_idx + 1]
        #         except IndexError:
        #             pass

        #         if left_child:
        #             nearest = left_child.mv_nearest_element()
        #             if nearest:
        #                 print('pulling left nearest element')
        #                 self.keys[element_idx] = nearest
        #                 return

        #         if left_child and right_child:
        #             print('join childs')
        #             self.join_pages(
        #                 element, element_idx, left_child, right_child)

        # else:
        #     my_idx = parent.children.index(self)
        #     try:
        #         left_brother = parent.children[my_idx - 1]
        #     except IndexError:
        #         print('error')
        #         pass

        #     if left_brother and left_brother.n - 1 >= left_brother.m and left_brother.keys:   # noqa: E501
        #         print('pedindo emprestado para a page esquerda')
        #         ok = self.borrow(my_idx, parent, left_brother)
        #         if ok:
        #             parent.printPages()
        #             self.removes(parent, element)
        #             return True
        #     try:
        #         right_brother = parent.children[my_idx + 1]
        #     except IndexError:
        #         print('error')
        #         pass

        #     if right_brother and right_brother.n - 1 >= right_brother.m and right_brother.keys:   # noqa: E501
        #         print('pedindo emprestado para a page direita')
        #         ok = self.borrow_right(my_idx, parent, right_brother)
        #         if ok:
        #             parent.printPages()
        #             self.removes(parent, element)
        #             return True

        # self.n = len(self.keys)

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
                root.printPages()
                print(c, ' elementos.')
        count = 0
        for i in a:
            count += 1
            print(f'removes {i}')
            page = root.search(i)
            if page:
                page.removes(i)
            root.printPages()
            if count == 30:
                break

        print('after:')
        root.printPages()
