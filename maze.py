class MazeGame:

    board = [[], [], [], [], [], [], [], [], [], [], [], []]
    goalX = 11
    goalY = 11

    def __init__(self):
        self.x = 0
        self.y = 0
        self.steps = 0
        self.faults = 0
        self.board = [[], [], [], [], [], [], [], [], [], [], [], []]
        # read board
        # get file object
    def open_maze(self,maze:str):
        f = open(maze, "r")
        index = 0
        while True:
            # read next line
            line = f.readline()
            # if line is empty, you are done with all lines in the file
            line = line[:12]
            if index == 12:
                break
            for l in line:
                self.board[index].append(l)

            index += 1
        # close file
        f.close()

    # move return 0 - wall, 1 - walk, 2 - victory
    def up(self):
        if self.y > 0:
            if not self.wall(self.x, self.y - 1):
                self.y -= 1
                self.steps += 1
                return self.goal()
        else:
            self.faults += 5
        return 0

    def down(self):
        if self.y < 11:
            if not self.wall(self.x, self.y + 1):
                self.y += 1
                self.steps += 1
                return self.goal()
        else:
            self.faults += 5
        return 0

    def left(self):
        if self.x > 0:
            if not self.wall(self.x - 1, self.y):
                self.x -= 1
                self.steps += 1
                return self.goal()
        else:
            self.faults += 5
        return 0

    def right(self):
        if self.x < 11:
            if not self.wall(self.x + 1, self.y):
                self.x += 1
                self.steps += 1
                return self.goal()
        else:
            self.faults += 5
        return 0

    def goal(self):
        if self.board[self.y][self.x] == 'S':

            return 2
        else:
            return 1

    def wall(self, x, y):
        if self.board[y][x] == '1':
            self.faults += 1
            return True
        else:
            return False

    def blocked_goal(self):  # If yes, then return penalty
        xLocked = False
        yLocked = False

        if self.x < self.goalX:
            for i in range(self.x + 1, self.goalX + 1):
                if self.board[self.y][i] == '1':
                    xLocked = True
                    break

        elif self.x > self.goalX:
            for i in range(self.x - 1, self.goalX - 1, -1):
                if self.board[self.y][i] == '1':
                    xLocked = True
                    break

        if self.y < self.goalY:
            for i in range(self.y + 1, self.goalY + 1):
                if self.board[i][self.x] == '1':
                    yLocked = True
                    break

        elif self.y > self.goalY:
            for i in range(self.y - 1, self.goalY - 1, -1):
                if self.board[i][self.x] == '1':
                    yLocked = True
                    break

        # penalty
        penalty = 2
        if xLocked and yLocked:
            penalty = 7
        elif self.x == self.goalX and yLocked:
            penalty = 10
        elif self.y == self.goalY and xLocked:
            penalty = 10

        return penalty
