import pygame as p;
import ChessEngine 

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_Images():
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Gamestate()
    valid_Moves = gs.get_Valid_Moves()
    move_Made = False
    load_Images()
    running = True
    square_Selected = ()
    player_Clicks = []
    while running: 
        for  e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if square_Selected == (row, col):
                    square_Selected = ()
                    player_Clicks = []
                else:
                    square_Selected = (row, col)
                    player_Clicks.append(square_Selected)
                if len(player_Clicks) == 2:
                    move = ChessEngine.Move(player_Clicks[0], player_Clicks[1], gs.board)
                    for i in range(len(valid_Moves)):
                        if move == valid_Moves[i]:
                            gs.make_Move(valid_Moves[i]) 
                            move_Made = True
                            square_Selected = ()
                            player_Clicks = []
                    if not move_Made:
                        player_Clicks = [square_Selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_Move()
                    move_Made = True
                    
        if move_Made:
            valid_Moves = gs.get_Valid_Moves()
            move_Made = False

        draw_Game_State(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_Game_State(screen, gs):
    draw_Board(screen)
    draw_Pieces(screen, gs.board)

def draw_Board(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_Pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()