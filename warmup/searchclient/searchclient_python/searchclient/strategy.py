from abc import ABCMeta, abstractmethod
from collections import deque
from time import perf_counter
from sortedcontainers import SortedDict
import memory


class Strategy(metaclass=ABCMeta):
    def __init__(self):
        self.explored = set()
        self.start_time = perf_counter()

    def add_to_explored(self, state: 'State'):
        self.explored.add(state)

    def is_explored(self, state: 'State') -> 'bool':
        return state in self.explored

    def explored_count(self) -> 'int':
        return len(self.explored)

    def time_spent(self) -> 'float':
        return perf_counter() - self.start_time

    def search_status(self) -> 'str':
        return '#Explored: {:6}, #Frontier: {:6}, #Generated: {:6}, Time: {:3.2f} s, Alloc: {:4.2f} MB, MaxAlloc: {:4.2f} MB'.format(self.explored_count(), self.frontier_count(), self.explored_count() + self.frontier_count(), self.time_spent(), memory.get_usage(), memory.max_usage)

    @abstractmethod
    def get_and_remove_leaf(self) -> 'State': raise NotImplementedError

    @abstractmethod
    def add_to_frontier(self, state: 'State'): raise NotImplementedError

    @abstractmethod
    def in_frontier(self, state: 'State') -> 'bool': raise NotImplementedError

    @abstractmethod
    def frontier_count(self) -> 'int': raise NotImplementedError

    @abstractmethod
    def frontier_empty(self) -> 'bool': raise NotImplementedError

    @abstractmethod
    def __repr__(self): raise NotImplementedError


class StrategyBFS(Strategy):
    def __init__(self):
        super().__init__()
        self.frontier = deque()
        self.frontier_set = set()

    def get_and_remove_leaf(self) -> 'State':
        leaf = self.frontier.popleft()
        self.frontier_set.remove(leaf)
        return leaf

    def add_to_frontier(self, state: 'State'):
        self.frontier.append(state)
        self.frontier_set.add(state)

    def in_frontier(self, state: 'State') -> 'bool':
        return state in self.frontier_set

    def frontier_count(self) -> 'int':
        return len(self.frontier)

    def frontier_empty(self) -> 'bool':
        return len(self.frontier) == 0

    def __repr__(self):
        return 'Breadth-first Search'


class StrategyDFS(Strategy):
    def __init__(self):
        super().__init__()
        self.frontier = deque()
        self.frontier_set = set()

    def get_and_remove_leaf(self) -> 'State':
        leaf = self.frontier.pop()
        self.frontier_set.remove(leaf)
        return leaf

    def add_to_frontier(self, state: 'State'):
        self.frontier.append(state)
        self.frontier_set.add(state)

    def in_frontier(self, state: 'State') -> 'bool':
        return state in self.frontier_set

    def frontier_count(self) -> 'int':
        return len(self.frontier)

    def frontier_empty(self) -> 'bool':
        return len(self.frontier) == 0

    def __repr__(self):
        return 'Depth-first Search'


class StrategyBestFirst(Strategy):
    def __init__(self, heuristic: 'Heuristic'):
        super().__init__()
        self.heuristic = heuristic
        self.frontier = SortedDict()
        # self.frontier = []
        self.frontier_set = set()

    def get_and_remove_leaf(self) -> 'State':
        # min_val = self.frontier[0][1]
        # arg_min = 0
        # for i,s in enumerate(self.frontier):
        #     v = s[1]
        #     if v < min_val:
        #         (min_val, arg_min) = (v, i)
        #
        # leaf = self.frontier.pop(arg_min)
        #
        # self.frontier_set.remove(leaf[0])
        # return leaf[0]

        (key, value) = self.frontier.popitem(0)
        leaf = value.pop()
        if value != []:
            self.frontier[key] = value
        self.frontier_set.remove(leaf)
        return leaf

    def add_to_frontier(self, state: 'State'):
        heur_eval = self.heuristic.f(state)
        value = self.frontier.setdefault(heur_eval, [])
        value.append(state)
        self.frontier[heur_eval] = value

        #
        # self.frontier.append((state, self.heuristic.f(state)))
        self.frontier_set.add(state)

    def in_frontier(self, state: 'State') -> 'bool':
        return state in self.frontier_set

    def frontier_count(self) -> 'int':
        return len(self.frontier)

    def frontier_empty(self) -> 'bool':
        return len(self.frontier) == 0


    def __repr__(self):
        return 'Best-first Search using {}'.format(self.heuristic)
