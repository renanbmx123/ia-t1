import wx

from geneticalgorithm import GeneticAlgorithm
from maze_gui import GridPanelFrame

if __name__ == '__main__':
    print("***** Initiate genetic algorithm *****")
    ga = GeneticAlgorithm()
    generation = ga.run()
    ## TODO
    ## Generate moves with only the maximum steps taken.
    moves = generation[0]
    print(f'\nBest solution {moves}\n')

    app = wx.App()
    frame = GridPanelFrame(None)

    for i in range(len(moves)):
        if moves[i] == '0':
            moves[i] = 'W'
        elif moves[i] == '1':
            moves[i] = 'S'
        elif moves[i] == '2':
            moves[i] = 'A'
        elif moves[i] == '3':
            moves[i] = 'D'
    frame.PlayGame([move for move in list(moves)])

    app.MainLoop()
