from classes.game import Game

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

if __name__ == '__main__':
	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
	game.mainloop()