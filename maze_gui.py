import wx
import wx.grid
from maze import MazeGame
from manhattan_dist import getManhattanDistance


# A panel that is used as a cell in the main grid panel
class Cell(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

    def SetRed(self):
        self.SetBackgroundColour((255, 0, 0))

    def SetGreen(self):
        self.SetBackgroundColour((0, 255, 0))

    def SetBlue(self):
        self.SetBackgroundColour((0, 0, 255))

    def SetWhite(self):
        self.SetBackgroundColour((255, 255, 255))

    def SetBlack(self):
        self.SetBackgroundColour((0, 0, 0))




# Main grid panel
class GridPanelFrame(wx.Frame):
    game = None
    timer = None
    locked = False
    cells = []
    lastX = 0
    lastY = 0
    presetMoves = []
    moveItr = 0

    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Initialize Maze Game UI
        self.SetTitle('Maze Game')

        panel = wx.Panel(self)
        panel.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        panel.SetFocus()
        gridSizer = wx.GridSizer(12, 12, 0, 0)

        self.game = MazeGame()
        self.game.open_maze('map.txt')
        self.lastX = self.game.x
        self.lastY = self.game.y
        print(self.game.board)

        # Create cells according to maze values
        for i in range(len(self.game.board)):
            self.cells.append([])
            for j in range(len(self.game.board[i])):
                cell = Cell(panel)
                if self.game.board[i][j] == '0':
                    cell.SetWhite()
                elif self.game.board[i][j] == '1':
                    cell.SetBlack()
                elif self.game.board[i][j] == 'E':
                    cell.SetBlue()
                elif self.game.board[i][j] == 'S':
                    cell.SetGreen()


                gridSizer.Add(cell, 0, wx.EXPAND)
                self.cells[i].append(cell)

        panel.SetSizer(gridSizer)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetSize(0, 0, 512, 503)
        self.Centre()
        self.Show()

        # Ticker for playing the game based on cli input
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Tick, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def PlayGame(self, moves):
        self.presetMoves = moves
        self.timer.Start(300)

    def Tick(self, event):
        if not self.locked:
            if self.moveItr < len(self.presetMoves):
                self.locked = True
                self.PlayMove(self.presetMoves[self.moveItr])
                self.moveItr += 1
                self.locked = False
            else:
                self.timer.Stop()

    def PlayMove(self, char):
        result = 0
        if char == 0:
            result = self.game.up()

        elif char == 1:
            result = self.game.down()

        elif char == 2:
            result = self.game.left()

        elif char == 3:
            result = self.game.right()

        if result == 1 or result == 2:
            self.cells[self.lastY][self.lastX].SetRed()
            self.cells[self.game.y][self.game.x].SetBlue()

            self.lastY = self.game.y
            self.lastX = self.game.x

            self.Refresh()

        self.SetTitle(
            'Maze Game (Steps: {}, Penalties: {}, Distance: {})'.format(
                self.game.steps,
                self.game.faults,
                getManhattanDistance(self.game.x, self.game.y, self.game.goalX, self.game.goalY)
            )
        )

    def OnKeyPress(self, event):
        char = chr(event.GetKeyCode())
        if (char == 'Q'):
            self.timer.Stop()
            self.Destroy()


    def OnClose(self, event):
        self.timer.Stop()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = GridPanelFrame(None)
    app.MainLoop()