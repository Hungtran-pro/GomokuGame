import turtle
from func import *

def click(x, y):
    '''
    handle the process of clicking mouse
    '''

    global colors, move_history, screen, win, result

    x, y = getIndexPosition(x, y)
    
    if win == True:
        print("Plase turn off the canvas!")
        return

    if not is_in_board(x, y, board): # do nothing if it's out of board
        return


    if board[x][y] == ' ':
        draw_circle(x, y, colors['p'])
        board[x][y] = 'p'
        move_history.append((x, y, 'p'))
        print(x,y)
        game_res = evaluate(board, move_history) # Check the state after person's move
        print(f"Player: {game_res}")
        if(game_res == -25):
            result = "Player"
            print(result)
            win = True
            return
        
        if (is_empty_board(board) == True) :
            print("Draw")
            win = True
            return
        rx, ry = best_move_func(board, 0, 'r', move_history)
        draw_circle(rx, ry, colors['r'])
        board[rx][ry] = 'r'
        move_history.append((rx, ry, 'r'))

        game_res = evaluate(board, move_history) # Check the state after person's move
        print(f"Robot: {game_res}")
        if(game_res == 25):
            result = "Robot"
            print(result)
            win = True
            return

def getIndexPosition(x, y):
    '''
    get coordinates of the clicked position of the mouse
    '''
    return round(x), round(y)

def draw_circle(x, y, colturtle):
    colturtle.goto(x,y-0.3)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()

def initialize(size):
    '''
    Initialize the board
    '''
    global screen, colors, move_history, board, win, STATE, result

    STATE = ["You won", "Robot won", "Draw"]
    move_history = []
    win = False
    board = make_board(size)

    screen = turtle.Screen()
    screen.onclick(click)
    screen.setup(screen.screensize()[1]*2, screen.screensize()[1]*2)
    screen.setworldcoordinates(-1,size,size,-1)
    screen.bgcolor('white')
    screen.tracer(500)

    colors = {'p':turtle.Turtle(),'r':turtle.Turtle(), 'g':turtle.Turtle()}
    colors['p'].color('grey') # color for person's move
    colors['r'].color('gold') # color for robot's move

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(9)

    border = turtle.Turtle()
    border.speed(9)
    border.penup()
    border.ht()

    side = (size - 1) / 2

    i = - 1
    for start in range(size):
        border.goto(start, side + side * i)
        border.pendown()
        i *= -1
        border.goto(start, side + side * i)
        border.penup()

    i=1
    for start in range(size):
        border.goto(side + side *i,start)
        border.pendown()
        i *= -1
        border.goto(side + side *i,start)
        border.penup()
    
    screen.listen() # pass (x, y) coordinates to click func
    screen.mainloop()



'''
Start the game
'''
initialize(15)