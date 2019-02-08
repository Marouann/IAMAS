from abc import ABCMeta, abstractmethod


class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        self.goals_list = {}
        # self.boxes_list = {}
        self.nb_goals = 0


        for row in range(len(initial_state.goals)-1):
            for col in range(len(initial_state.goals[row])-1):

                if initial_state.goals[row][col]:
                    if not initial_state.goals[row][col] in self.goals_list:
                        self.goals_list[initial_state.goals[row][col]] = []
                    self.goals_list[initial_state.goals[row][col]].append((row,col, self.nb_goals * 200))
                    self.nb_goals += 1
                # if initial_state.boxes[row][col]:
                #     if self.boxes_list[initial_state.boxes[row][col]] == None:
                #         self.boxes_list[initial_state.boxes[row][col]] = []
                #     self.boxes_list[initial_state.boxes[row][col]].append((row,col))


    def h(self, state: 'State') -> 'int':
        res = 0
        current_boxes = {}
        agent = (state.agent_row, state.agent_col)
        man_dist = lambda a,b : abs(a[0]-b[0]) + abs(a[1]-b[1])

        def subH(agent, goal, box):
            if man_dist(box, goal) == 0:
                return 0
            return man_dist(box, goal) + man_dist(agent, box) + goal[2]

        # file = open("log.txt", 'w')
        for row in range(len(state.goals)):
            for col in range(len(state.goals[row])):
                box_name = state.boxes[row][col]
                if box_name != None and not box_name in current_boxes:
                    current_boxes[box_name] = []

                # file.write(str(current_boxes)+str(box_name)+str(self.goals_list)+str((row,col))+ str(state.goals[row][col])+'\n')
                if box_name != None:
                    current_boxes[box_name.upper()].append((row,col))

        for goals_name in self.goals_list.keys():
            for goal in self.goals_list[goals_name]:
                try:
                    res += min(subH(agent,goal,box) for box in current_boxes[goals_name.upper()])

                except:
                    res = 0

        # file = open("log.txt", 'w')
        # file.write(str(current_boxes))
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
