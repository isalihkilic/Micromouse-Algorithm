import random

#Storage of the labyrinth is a bit different from the one in the labyrinth.py, it stores 2 different representations of the labyrinth and it is imaginary
#First 4 bits is the walls of closed maze, last 4 bits is the walls of open maze
#So default value for cells are 11110000, equal to 240 in decimal
class Micromouse:
    def __init__(self):
        self.cells = [[0b11110000 for _ in range(16)] for i in range(16)]
        self.cells[0][0] = 0b11011101
        self.floodmaze = [[-1 for _ in range(16)] for i in range(16)]
        self.floodclosedmaze = [[-1 for _ in range(16)] for i in range(16)]
        self.starting_cell = (0, 0)
        self.target_cell = (8, 8)
        self.current_position = (0, 0)
        self.heading = 2
        self.returning = False
        self.found_shortest = False
        self.shortest_path = []

    def add_observation(self, left, front, right):   #Adds observation to "imaginary" labyrinth
        match self.heading:
            case 1:                               #Looking up
                cell = 0b10110000
                cell += 8 if left else -128
                cell += 1 if front else -16
                cell += 2 if right else -32
                if self.current_position[0] > 0:              #Update upper cell
                    if front:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] |= 0b00000100
                    else:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] &= 0b10111111
                if self.current_position[1] > 0:              #Update left cell
                    if left:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] |= 0b00000010
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] &= 0b11011111
                if self.current_position[1] < 15:              #Update right cell
                    if right:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] |= 0b00001000
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] &= 0b01111111
                self.cells[self.current_position[0]][self.current_position[1]] = cell
            case 2:                               #Looking right
                cell = 0b01110000
                cell += 1 if left else -16
                cell += 2 if front else -32
                cell += 4 if right else -64
                if self.current_position[0] > 0:              #Update upper cell
                    if left:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] |= 0b00000100
                    else:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] &= 0b10111111
                if self.current_position[0] < 15:              #Update below cell
                    if right:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] |= 0b00000001
                    else:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] &= 0b11101111
                if self.current_position[1] < 15:              #Update right cell
                    if front:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] |= 0b00001000
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] &= 0b01111111
                self.cells[self.current_position[0]][self.current_position[1]] = cell
            case 4:                               #Looking down
                cell = 0b11100000
                cell += 2 if left else -32
                cell += 4 if front else -64
                cell += 8 if right else -128
                if self.current_position[0] < 15:              #Update bottom cell
                    if front:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] |= 0b00000001
                    else:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] &= 0b11101111
                if self.current_position[1] > 0:              #Update left cell
                    if right:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] |= 0b00000010
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] &= 0b11011111
                if self.current_position[1] < 15:              #Update right cell
                    if left:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] |= 0b00001000
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] + 1] &= 0b01111111
                self.cells[self.current_position[0]][self.current_position[1]] = cell
            case 8:                               #Looking left
                cell = 0b11010000
                cell += 4 if left else -64
                cell += 8 if front else -128
                cell += 1 if right else -16
                if self.current_position[0] > 0:              #Update upper cell
                    if right:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] |= 0b00000100
                    else:
                        self.cells[self.current_position[0] - 1][self.current_position[1]] &= 0b10111111
                if self.current_position[0] < 15:              #Update bottom cell
                    if left:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] |= 0b00000001
                    else:
                        self.cells[self.current_position[0] + 1][self.current_position[1]] &= 0b11101111
                if self.current_position[1] < 15:              #Update left cell
                    if front:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] |= 0b00000010
                    else:
                        self.cells[self.current_position[0]][self.current_position[1] - 1] &= 0b11011111
                self.cells[self.current_position[0]][self.current_position[1]] = cell
        if self.current_position == self.target_cell:
            if self.current_position != self.starting_cell:       #Returns true if done
                self.returning = True
                self.target_cell = self.starting_cell
            else:
                return True

    def floodfill_openmaze(self):
        self.floodmaze = [[-1 for _ in range(16)] for i in range(16)]
        distance = 0
        cells = [self.target_cell]
        temp_cells = []
        while True:
            for cell in cells:
                self.floodmaze[cell[0]][cell[1]] = distance
                if self.cells[cell[0]][cell[1]] & 1 == 0 and cell[0] > 0:
                    if self.floodmaze[cell[0] - 1][cell[1]] == -1:
                        temp_cells.append((cell[0] - 1, cell[1]))
                if self.cells[cell[0]][cell[1]] & 2 == 0 and cell[1] < 15:
                    if self.floodmaze[cell[0]][cell[1] + 1] == -1:
                        temp_cells.append((cell[0], cell[1] + 1))
                if self.cells[cell[0]][cell[1]] & 4 == 0 and cell[0] < 15:
                    if self.floodmaze[cell[0] + 1][cell[1]] == -1:
                        temp_cells.append((cell[0] + 1, cell[1]))
                if self.cells[cell[0]][cell[1]] & 8 == 0 and cell[1] > 0:
                    if self.floodmaze[cell[0]][cell[1] - 1] == -1:
                        temp_cells.append((cell[0], cell[1] - 1))
            cells = temp_cells
            #print(cells)
            if cells == []:
                break
            temp_cells = []
            distance += 1
        self.open_dist = self.floodmaze[8][8] if self.returning else self.floodmaze[0][0]
    
    def floodfill_closedmaze(self):
        self.floodclosedmaze = [[-1 for _ in range(16)] for i in range(16)]
        distance = 0
        cells = [self.target_cell]
        temp_cells = []
        while True:
            for cell in cells:
                self.floodclosedmaze[cell[0]][cell[1]] = distance
                if self.cells[cell[0]][cell[1]] & 16 == 0 and cell[0] > 0:
                    if self.floodclosedmaze[cell[0] - 1][cell[1]] == -1:
                        temp_cells.append((cell[0] - 1, cell[1]))
                if self.cells[cell[0]][cell[1]] & 32 == 0 and cell[1] < 15:
                    if self.floodclosedmaze[cell[0]][cell[1] + 1] == -1:
                        temp_cells.append((cell[0], cell[1] + 1))
                if self.cells[cell[0]][cell[1]] & 64 == 0 and cell[0] < 15:
                    if self.floodclosedmaze[cell[0] + 1][cell[1]] == -1:
                        temp_cells.append((cell[0] + 1, cell[1]))
                if self.cells[cell[0]][cell[1]] & 128 == 0 and cell[1] > 0:
                    if self.floodclosedmaze[cell[0]][cell[1] - 1] == -1:
                        temp_cells.append((cell[0], cell[1] - 1))
            cells = temp_cells
            #print(cells)
            if cells == []:
                break
            temp_cells = []
            distance += 1
        self.closed_dist = self.floodclosedmaze[8][8] if self.returning else self.floodclosedmaze[0][0]
        if self.closed_dist == self.open_dist and not self.found_shortest:
            print("Shortest path/one of the shortest paths from starting point to finish is found. Distance is {}".format(self.closed_dist))
            self.calculate_shortest_path()
            self.found_shortest = True
        
    def move_to_best(self):
        floodmaze = self.floodclosedmaze if self.closed_dist == self.open_dist else self.floodmaze
        current_cell = self.cells[self.current_position[0]][self.current_position[1]]
        min_dirs = []
        min_dist = 1000
        if current_cell & 1 == 0:
            dist = floodmaze[self.current_position[0] - 1][self.current_position[1]]
            if dist == min_dist:
                min_dirs.append(1)
            elif dist < min_dist:
                min_dirs = [1]
                min_dist = dist
        if current_cell & 2 == 0:
            dist = floodmaze[self.current_position[0]][self.current_position[1] + 1]
            if dist == min_dist:
                min_dirs.append(2)
            elif dist < min_dist:
                min_dirs = [2]
                min_dist = dist
        if current_cell & 4 == 0:
            dist = floodmaze[self.current_position[0] + 1][self.current_position[1]]
            if dist == min_dist:
                min_dirs.append(4)
            elif dist < min_dist:
                min_dirs = [4]
                min_dist = dist
        if current_cell & 8 == 0:
            dist = floodmaze[self.current_position[0]][self.current_position[1] - 1]
            if dist == min_dist:
                min_dirs.append(8)
            elif dist < min_dist:
                min_dirs = [8]
                min_dist = dist
        self.heading = min_dirs[random.randint(0, len(min_dirs) - 1)] if len(min_dirs) > 1 else min_dirs[0]
        #print(self.heading)
        if self.heading == 1:
            self.current_position = (self.current_position[0] - 1, self.current_position[1])
        if self.heading == 2:
            self.current_position = (self.current_position[0], self.current_position[1] + 1)
        if self.heading == 4:
            self.current_position = (self.current_position[0] + 1, self.current_position[1])
        if self.heading == 8:
            self.current_position = (self.current_position[0], self.current_position[1] - 1)
        #print(self.current_position)

    def calculate_shortest_path(self):
        target_cell = (0, 0) if self.returning else (8, 8)
        starting_cell = (8, 8) if self.returning else (0, 0)
        path = [starting_cell]
        
        current_cell = starting_cell
        
        while current_cell != target_cell:
            current_dist = self.floodclosedmaze[current_cell[0]][current_cell[1]]
            if self.cells[current_cell[0]][current_cell[1]] & 64 == 0:
                if current_dist - 1 == self.floodclosedmaze[current_cell[0] + 1][current_cell[1]]:
                    current_cell = (current_cell[0] + 1, current_cell[1])
            if self.cells[current_cell[0]][current_cell[1]] & 32 == 0:
                if current_dist - 1 == self.floodclosedmaze[current_cell[0]][current_cell[1] + 1]:
                    current_cell = (current_cell[0], current_cell[1] + 1)
            if self.cells[current_cell[0]][current_cell[1]] & 128 == 0:
                if current_dist - 1 == self.floodclosedmaze[current_cell[0]][current_cell[1] - 1]:
                    current_cell = (current_cell[0], current_cell[1] - 1)
            if self.cells[current_cell[0]][current_cell[1]] & 16 == 0:
                if current_dist - 1 == self.floodclosedmaze[current_cell[0] - 1][current_cell[1]]:
                    current_cell = (current_cell[0] - 1, current_cell[1])
            if current_cell == starting_cell:
                break
            current_dist -= 1
            path.append(current_cell)
        self.shortest_path = path

            