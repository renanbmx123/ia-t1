import wx

from geneticalgorithm import GeneticAlgorithm
from maze_gui import GridPanelFrame

if __name__ == '__main__':
    print("***** Initiate genetic algorithm *****\n")
    ga = GeneticAlgorithm()
    generation = ga.run()

    moves = generation[0]
    print(f'\nBest solution {moves}\n')

    app = wx.App()
    frame = GridPanelFrame(None)

    frame.PlayGame([move for move in list(moves[0])])

    app.MainLoop()
