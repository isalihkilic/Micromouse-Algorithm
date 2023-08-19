#üst duvar: 0001   = 1
#sağ duvar: 0010  = 2
#alt duvar: 0100 = 4
#sol duvar: 1000  = 8

class Labyrinth:
    def __init__(self):
        #self.cells = [                      #Hardcoded 6*5 labyrinth
        #    [15, 15, 11, 15, 15],
        #    [9, 5, 4, 5, 3],
        #    [8, 5, 5, 7, 10],
        #    [14, 9, 3, 9, 2],
        #    [9, 2, 12, 6, 10],
        #    [14, 12, 3, 13, 6]
        #]

        self.cells = [                      #Hardcoded 16*16 labyrinth
            [13, 1, 3, 9, 1, 5, 7, 12, 5, 3, 13, 3, 9, 3, 9, 3],
            [9, 6, 12, 6, 14, 9, 1, 5, 7, 10, 9, 6, 10, 12, 6, 10],
            [10, 9, 5, 5, 5, 6, 8, 3, 9, 6, 12, 3, 12, 5, 5, 10],
            [10, 12, 1, 5, 5, 3, 10, 14, 12, 1, 5, 6, 9, 5, 3, 10],
            [10, 9, 6, 9, 3, 10, 10, 9, 3, 12, 5, 3, 10, 11, 12, 2],
            [10, 10, 11, 10, 12, 6, 10, 10, 12, 5, 3, 12, 6, 12, 3, 10],
            [12, 6, 10, 12, 7, 9, 2, 12, 5, 3, 12, 1, 5, 3, 10, 10],
            [9, 7, 10, 9, 5, 6, 10, 9, 3, 10, 13, 4, 7, 12, 4, 6],
            [12, 3, 10, 10, 9, 3, 14, 12, 2, 12, 5, 5, 3, 9, 3, 11],
            [9, 4, 6, 10, 14, 12, 5, 3, 8, 5, 7, 9, 4, 6, 8, 6],
            [10, 9, 3, 10, 9, 5, 3, 8, 0, 3, 9, 6, 13, 3, 8, 7],
            [8, 6, 10, 10, 10, 9, 0, 6, 10, 10, 12, 3, 9, 6, 12, 3],
            [10, 9, 6, 12, 6, 10, 12, 3, 10, 12, 7, 8, 6, 9, 5, 6],
            [10, 10, 9, 5, 3, 10, 13, 6, 14, 9, 3, 12, 3, 12, 5, 7],
            [10, 10, 12, 3, 10, 12, 5, 5, 1, 2, 12, 1, 4, 7, 9, 3],
            [14, 12, 5, 6, 12, 5, 5, 5, 6, 12, 7, 12, 5, 5, 6, 14],
        ]
        
    def get_sensor_data(self, position, heading):   #Order is left of the robot, forward of the robot, right of the robot
        match heading:
            case 1:
                return self.cells[position[0]][position[1]] & 8, self.cells[position[0]][position[1]] & 1, self.cells[position[0]][position[1]] & 2
            case 2:
                return self.cells[position[0]][position[1]] & 1, self.cells[position[0]][position[1]] & 2, self.cells[position[0]][position[1]] & 4
            case 4:
                return self.cells[position[0]][position[1]] & 2, self.cells[position[0]][position[1]] & 4, self.cells[position[0]][position[1]] & 8
            case 8:
                return self.cells[position[0]][position[1]] & 4, self.cells[position[0]][position[1]] & 8, self.cells[position[0]][position[1]] & 1