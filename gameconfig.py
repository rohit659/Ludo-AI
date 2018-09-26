class Color:

    GREEN = '#3EB62B'
    RED = '#F71313'
    YELLOW = '#F3F012'
    BLUE = '#3575EC'
    DEFAULT = '#E9E9E9'
    PINK = '#FFB6C1'
    CYAN = '#4EB1BA'
    GRAY = '#A9A9A9'


class Board:

    SQUARE_SIZE = 55
    PANEL_WIDTH = 600
    PANEL_HEIGHT = 640
    BOARD_WIDTH = 900
    BOARD_HEIGHT = 880
    POINTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
    SAFE_V = [(6, 2), (8, 1), (6, 13), (8, 12)]
    SAFE_H = [(1, 6), (2, 8), (13, 8), (12, 6)]

class Text:

    MADE_BY = 'Made By: Mansi Agrawal & Shivam Gupta'
    HEADER =  'LUDO - THE GAME'
