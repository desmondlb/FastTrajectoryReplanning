class Node():
    '''
        Here we create a node class which store the following
            1. Position of the node in the grid
            2. Parent of the node
            3. f(n),g(n) and h(n) values for the node
    '''
    def __init__(self, position=None, parent=None) -> None:
        self.position = position
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0


class FastTrajectoryReplanning():

    def __init__(self) -> None:
        self.open_list = []
        self.closed_list = []

        #-----------------------------------
        # Valid moves: up, down, left, right
        #-----------------------------------
        self.valid_moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        self.grid = None

        self.counter = 0
        self.search = dict()

    
    def print_path(self, current) -> None:
        '''
            This function prints a list of positions that
            the agent travels to get from start to the goal state.
        '''
        path = []

        while(current.parent):
            path.append(current.position)
            current = current.parent
        
        print(path[::-1])
        
    def get_manhattan_dist(self, start, goal) -> int:
        '''
            This function returns Norm 1 distance between start and the goal state
        '''
        return abs(start[0]-goal[0]) + abs(start[1]-goal[1])

    def get_priority_node(self) -> Node:
        '''
            This function returns the node with the least f value
            from the Open list
            TBD: Implementation with priority heap/queue
        '''
        priority_node = self.open_list[0]

        for n in self.open_list:
            if(n.f <= priority_node.f):
                priority_node = n

        return priority_node

    def get_valid_moves(self, current) -> list:
        '''
            Here we check the following
                1. Does the node lie within grid boundaries
                2. Is there an obstacle?
        '''
        current_legal_moves = []

        for move in self.valid_moves:

            #---------------------------------------------------------
            # Adding the move to current position updates the position
            #---------------------------------------------------------
            new_position = tuple(map(sum, zip(move, current.position)))

            if(new_position[0] >= 0 and new_position[1] >= 0):
                if(new_position[0] < len(self.grid) and new_position[1] < len(self.grid)):
                    if not self.grid[new_position[0]][new_position[1]]==1:
                        current_legal_moves.append(new_position)

        return current_legal_moves


    def perform_move(self, move, current_position) -> tuple:
        '''
            This function performs the selected move on the current_position
            Returns the updated position
        '''
        return tuple(map(sum, zip(move, current_position)))

    def check_node_in_open_list(self, child_state) -> bool:
        '''
            This function checks whether a child node is in the open list
            and whether it has a better f value
        '''
        for n in self.open_list:
            if(n.position == child_state.position):
                return True             
            
        return False

    def check_node_in_closed_list(self, child_state) -> bool:
        '''
            This function checks whether a child node is in the closed list
            and whether it has a better f value
        '''
        for n in self.closed_list:
            if((n.position == child_state.position) and n.f < child_state.f):
                return True             
            
        return False

    def compute_path(self, grid, start_node, goal_node) -> None:
        '''
            Implementation of the simple A* algorithm
        '''
        s = self.get_priority_node()
        while(goal_node.g > s.f):
            self.open_list.remove(s)
            self.closed_list.append(s)

            moves = self.get_valid_moves(s)

            for succ in moves:
                succ_node = Node(position=succ)
                if self.search(succ) < self.counter:
                    
                    succ_node.g = pow(len(self.grid),2) + 10
                    self.search[succ_node.position] = self.counter

                if succ_node.g > s.g + 1:

                    succ_node.g = s.g + 1
                    succ_node.f = s.g + self.get_manhattan_dist(succ, goal_node.position)
                    succ_node.parent = s
                    if self.check_node_in_open_list(succ_node):
                        self.open_list.remove(succ_node)

                    self.closed_list.append(succ_node)
            


    def repeated_forward_a_star(self, start, goal):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.search[tuple(i,j)] = 0
        
        while(start!=goal):
            self.counter += 1

            start_node = Node(position=start)
            start_node.g = 0
            self.search[start_node.position] = self.counter

            goal_node = Node(position=start)
            goal_node.g = pow(len(self.grid),2) + 10
            self.search[goal_node.position] = self.counter

            self.open_list = []
            self.closed_list = []

            start_node.h = self.get_manhattan_dist(start, goal)
            start_node.f = start_node.g + start_node.h

            self.open_list.append(start_node)

            self.compute_path(start_node, goal_node)

            if not self.open_list:
                print("Cannot reach the target")
                return

        
            if curr:
            self.print_path(curr)

        print("I reached the target")
        return
    
    def run(self, start=None, goal=None) -> None:
        '''
            This function runs the A* algorithm on the generated grid
        '''
        self.generate_grid()

        self.repeated_forward_a_star(self.grid, start, goal)
        

    def generate_grid(self) -> None:
        '''
            This function generates N*N grid with the following properties
                1. Obstacles generated with 30% probability to construct a maze like structure
                2. Target position denoted with "X"
                3. Obstacles denoted with 1
        '''
        #-----------
        # Dummy grid
        #-----------
        self.grid = [[0,0,1,0,0],
                    [0,0,1,0,0],
                    [0,0,1,0,0],
                    [0,0,1,"X",0],
                    [0,0,0,0,0]]



if __name__ == "__main__":
    obj = FastTrajectoryReplanning()

    obj.run(start = (0, 0), goal = (3,3))