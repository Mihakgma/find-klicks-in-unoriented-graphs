from pandas import Series as pd_Series

class CliqueFinder():

    """
    Ищет клики с заданным количеством вершин и
    возвращает в виде (метод ...)...
    """

    def __init__(self, graph, method: str='default', clique_vertex_num:int=2, vertex_num_equals: str='no'):
        self.__graph = graph
        self.__method = method
        self.__clique_vertex_num = clique_vertex_num
        self.__vertex_num_equals = vertex_num_equals

    def get_graph(self):
        return self.__graph

    def get_method(self):
        return self.__method

    def get_clique_vertex_num(self):
        return self.__clique_vertex_num

    def get_vertex_num_equals(self):
        return self.__vertex_num_equals


    def default_clique_algorithm(self, G):
        if len(G) == 0:
            return

        adj = {u: {v for v in G[u] if v != u} for u in G}
        Q = [None]

        subg = set(G)
        cand = set(G)
        u = max(subg, key=lambda u: len(cand & adj[u]))
        ext_u = cand - adj[u]
        stack = []

        try:
            while True:
                if ext_u:
                    q = ext_u.pop()
                    cand.remove(q)
                    Q[-1] = q
                    adj_q = adj[q]
                    subg_q = subg & adj_q
                    if not subg_q:
                        yield Q[:]
                    else:
                        cand_q = cand & adj_q
                        if cand_q:
                            stack.append((subg, cand, ext_u))
                            Q.append(None)
                            subg = subg_q
                            cand = cand_q
                            u = max(subg, key=lambda u: len(cand & adj[u]))
                            ext_u = cand - adj[u]
                else:
                    Q.pop()
                    subg, cand, ext_u = stack.pop()
        except IndexError:
            pass

    def find_cliques_sorted(self):

        """
        Данный метод предназначен для поиска клик в исходном графе
        :return:
        список списков упорядоченный по убыванию длины списков
        с длиной списков от значения аттрибута <clique_vertex_num>
        """

        graph = self.get_graph()
        orig_graph_vertexes_num = len(graph)
        method = self.get_method()
        clique_vertex_num = self.get_clique_vertex_num()
        vertex_num_equals = self.get_vertex_num_equals()

        # алгоритм

        if method == 'default':
            clique_lst = self.default_clique_algorithm(graph)

        if vertex_num_equals == 'yes': # количество вершин в кликах СТРОГО ограничено одним значением
            cliques_intersected = [i for i in sorted(clique_lst, key=len)[::-1] if len(i) == clique_vertex_num]

        elif vertex_num_equals == 'no': # кол-во вершин в кликах от (включительно) и более заданного значения
            cliques_intersected = [i for i in sorted(clique_lst, key=len)[::-1] if len(i) >= clique_vertex_num]

        # удаляем задубленные вершины в кликах

        vertex_set = set()
        cliques_not_intersected = []

        for lst in cliques_intersected:
            flag = True
            for elem in lst:
                if elem not in vertex_set:
                    vertex_set.add(elem)
                else:
                    flag = False
            if flag:
                cliques_not_intersected.append(lst)

        self.show_cliques_info(cliques_not_intersected, orig_graph_vertexes_num)

        return cliques_not_intersected


    def show_cliques_info(self, found_cliques_lst, vertexes_num):
        found_vertexes_lst_extended = []
        cliques_num = 0

        for clique in found_cliques_lst:
            cliques_num += 1
            for vertex in clique:
                found_vertexes_lst_extended.append(vertex)

        found_cliques_vertexes_unique = pd_Series(found_vertexes_lst_extended).nunique()

        print(f'В исходном графе с общим количеством вершин, равном <{vertexes_num}> (шт.)\n')

        print(f'Найдено клик: <{cliques_num}> (шт.)\n')

        if found_cliques_vertexes_unique == len(found_vertexes_lst_extended):
            print('Найденные клики НЕ ПЕРЕСЕКАЮТСЯ по вершинам исходного графа.')
            print('ОК!')
            print(f'Уникальных вершин: <{found_cliques_vertexes_unique}> (шт.)')
        else:
            print('Найденные клики ПЕРЕСЕКАЮТСЯ по вершинам исходного графа.')
            print('ЧТО-ТО ПОШЛО НЕ ТАК!')
            print(f'Всего вершин в найденных кликах: <{len(found_vertexes_lst_extended)}> (шт.)')
            print(f'ИЗ НИХ Уникальных вершин: <{found_cliques_vertexes_unique}> (шт.)')


