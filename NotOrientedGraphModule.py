import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class NotOrientedGraph():

    """
    Данный класс создает неориентированный граф.
    С заданным количеством вершин (N)
    Если параметр <complete> == 'yes',
    то создает полный граф,
    если он равен 'no' - неполный граф.
    Lower & Upper Bounds - границы (нижняя и верхняя соотв.)
    интервала значений для матрицы смежности (веса ребер графа!)
    (все ребра, веса которых выходят за его границы - отсекаются).
    Далее матрица смежности используется для построения
    неориентированного графа заданной полноты (атрибут "complete").
    В случае графа с одинаковыми весами ребер (аттрибут <weighted> == 'no')
    им всем присваивается значение 1!
    """

    def __init__(self,
                 N:int=100,
                 complete:str='no',
                 lower_bound:float=0.1,
                 upper_bound:float=0.8,
                 weighted:str='yes'):
        self.__N = int(N)
        self.__complete = complete.lower().strip()
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__weighted = weighted


    # методы-геттеры аттрибутов
    def get_N(self):
        return self.__N


    def get_complete(self):
        return self.__complete


    def get_lower_bound(self):
        return self.__lower_bound


    def get_upper_bound(self):
        return self.__upper_bound


    def get_weighted(self):
        return self.__weighted


    # методы-сеттеры аттрибутов
    def set_N(self, N: int):
        try:
            N = int(N)
            if 1001 > N > 0:
                self.__N = N
            elif N > 1000:
                print(f'Поданное значение <N>, равное {N}, вероятно, очень большое...')
                print('Предполагается, что <N> - целое число и лежит в диапазоне от 1 до 1000!')
            else:
                print('N (число вершин графа) - целое положительное число')
                print(f'N не может быть равно: <{N}>')
        except:
            self.wrong_format('N', N)
            print('Предполагается, что <N> - целое число и лежит в диапазоне от 1 до 1000!')

    def set_complete(self, complete: str):
        try:
            complete = complete.lower().strip()
            if (complete == 'yes' or complete =='no'):
                self.__complete = complete
            else:
                print('Недопустимое значение аттрибута <complete>:')
                print(f'{complete}')
        except:
            self.wrong_format('complete',complete)

    def set_lower_bound(self, lower_bound):
        upper_bound = self.get_upper_bound()
        try:
            if (1.0 >= lower_bound >= 0.0 and
            lower_bound < upper_bound):
                self.__lower_bound = lower_bound
            elif lower_bound >= upper_bound:
                print('Нижняя должна быть СТРОГО меньше верхней границы интервала!!!')
                print('Интервал развесовки ребер графа: ')
                print(f'Нижняя граница: {lower_bound}')
                print(f'Верхняя граница: {upper_bound}')
            else:
                print('Недопустимое значение аттрибута <lower_bound>:')
                print(f'{lower_bound}')
                print('Предполагается, что значение данного атрибута должно быть в пределах от 0 до 1 включительно')
        except:
            self.wrong_format('lower_bound', lower_bound)


    def set_upper_bound(self, upper_bound):
        lower_bound = self.get_lower_bound()
        try:
            if (1.0 >= upper_bound >= 0.0 and
            lower_bound < upper_bound):
                self.__upper_bound = upper_bound
            elif lower_bound >= upper_bound:
                print('Нижняя должна быть СТРОГО меньше верхней границы интервала!!!')
                print('Интервал развесовки ребер графа: ')
                print(f'Нижняя граница: {lower_bound}')
                print(f'Верхняя граница: {upper_bound}')
            else:
                print('Недопустимое значение аттрибута <upper_bound>:')
                print(f'{upper_bound}')
                print('Предполагается, что значение данного атрибута должно быть в пределах от 0 до 1 включительно')
        except:
            self.wrong_format('upper_bound', upper_bound)


    def set_weighted(self, weighted: str):
        try:
            weighted = weighted.lower().strip()
            if (weighted == 'yes' or weighted =='no'):
                self.__weighted = weighted
            else:
                print('Недопустимое значение аттрибута <weighted>:')
                print(f'{weighted}')
        except:
            self.wrong_format('weighted',weighted)


    def wrong_format(self, variable_name, variable_value):
        """
        Срабатывает в том случае,
        когда аттрибуту пытаются с помощью метода-сеттера
        пытаются присвоить невалидное значение
        :param variable_name: наименование аттрибута
        :param variable_value: переданное для присвоения значение аттрибута
        :return:
        """
        print(f'Неверный формат.'
              f'В качестве <{variable_name}> подано: <{variable_value}>; '
              f'формата: <{type(variable_value)}>')


    def build_graph(self):
        """
        данный метод
        :return: граф с заданными ранее параметрами
        """
        N = self.get_N() # Количество вершин
        complete = self.get_complete() # граф - полносвязный?
        lower_bound = self.get_lower_bound() # нижняя граница весов ребер
        upper_bound = self.get_upper_bound() # верхняя граница весов ребер
        weighted = self.get_weighted() # граф - со взвешенными ребрами
        # Генерация матрицы смежности
        A = np.triu(np.random.exponential(0.1, [N, N]), 1)
        if complete == 'no': # Убрать часть ребер, иначе граф получится полносвязным
            A[A<lower_bound]=0
            A[A>upper_bound] = 0
        else: # полносвязный граф
            pass
        if weighted == 'no':
            A[A>0]=1 # граф со невзвешенными ребрами
        G = nx.from_numpy_matrix(A)
        return G

    def draw_graph(self):
        """
        Данный метод рисует граф
        :param G: граф из метода build_graph
        :return: нарисованный граф с заданными ранее параметрами
        """
        graph = self.build_graph()
        plt.figure(figsize=(8, 8))
        nx.draw(graph, with_labels=True, font_size=10)
        return graph

