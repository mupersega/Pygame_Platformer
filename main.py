from classes.game import Game

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

if __name__ == '__main__':
	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
	game.mainloop()