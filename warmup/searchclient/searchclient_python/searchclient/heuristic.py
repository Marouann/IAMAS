from abc import ABCMeta, abstractmethod

man_dist = lambda a,b : abs(a[0]-b[0]) + abs(a[1]-b[1])

def subH(agent, box, goal):
    if man_dist(box, goal) == 0:
        return 0
    if man_dist(box, agent) == 1:
        return goal[2] + man_dist(box, goal)
    return man_dist(box, goal) + man_dist(agent, box) + goal[2]

class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        # Initialisation of the goals
        self.goals_list = {}
        self.count_goals = 0
        
        for row in range(len(initial_state.goals)):
            for col in range(len(initial_state.goals[row])):
                if initial_state.goals[row][col]:
                    if not initial_state.goals[row][col] in self.goals_list:
                        self.goals_list[initial_state.goals[row][col]] = []
                    self.goals_list[initial_state.goals[row][col]].append((row,col,(70 - self.count_goals) * 140))
                    self.count_goals += 1

    def h(self, state: 'State') -> 'int':
        res = 0
        current_boxes = {}

        for row in range(len(state.goals)):
            for col in range(len(state.goals[row])):
                if state.boxes[row][col] != None:
                    if not state.boxes[row][col] in current_boxes:
                        current_boxes[state.boxes[row][col]] = []
                    current_boxes[state.boxes[row][col]].append((row,col))
    
        for goals_name in self.goals_list.keys():
            for goal in self.goals_list[goals_name]:
                res += min(subH([state.agent_row, state.agent_col], box, goal) for box in current_boxes[goals_name.upper()])
        return res
    
    @abstractmethod
    def f(self, state: 'State') -> 'int': pass
    
    @abstractmethod
    def __repr__(self): raise NotImplementedError


class AStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)
    
    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w
    
    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)
    
    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)
    
    def f(self, state: 'State') -> 'int':
        return self.h(state)
    
    def __repr__(self):
        return 'Greedy evaluation'

