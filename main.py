import turtle
from cmath import inf 

def make_board_ones(size):
    '''
    Create a marked board with initial value = 1
    ''' 
    board_row = [1] * size
    board = []
    for i in range(size):
        board.append(board_row)
    return board

def is_in_board(x, y, board):
    '''
    Check whether the clicked position is in board or not
    '''
    return 0 <= x <= len(board) and 0 <= y <= len(board)

def is_empty_board(board):
    '''
    Check whether the board is empty or not
    '''
    return board == ([[' '] * len(board)] * len(board))

def make_board(size):
    board = []
    for i in range(size):
        board.append([" "]*size)
    return board

def evaluate(board, move_history):
    '''
    Evaluate the current node/status
    '''
    # score_dir = {(0,1): 0, (1, 1): 0, (1, 0): 0, (1, -1): 0, (0, -1): 0, (-1, -1): 0, (-1, 0): 0, (-1, 1): 0}
    score_dir = [0, 0, 0, 0, 0, 0, 0, 0]
    dir = [(0,1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    score_person = +inf
    score_robot  = -inf
    for moved_position in move_history:
        if(board[moved_position[0]][moved_position[1]] == 'r'):
            for idx in range(len(dir)):
                score_dir[idx] = score_per_dir((dir[idx]), board, (moved_position[0], moved_position[1]))
                score_robot = max(score_robot, score_dir[idx])
        else:
            for idx in range(len(dir)):
                score_dir[idx] = score_per_dir((dir[idx]), board, (moved_position[0], moved_position[1]))
                score_person = min(score_person, score_dir[idx])
    if move_history[-1][2] == 'p':
        return score_person
    return score_robot

def score_per_dir(dir, board, cur_position):
    '''
    Get score per direction regarding the current state
    '''
    dx, dy = dir
    x, y = cur_position
    balance = 1 if board[x][y] == 'r' else -1
    point = get_point_dir(x, y, dx, dy, board)
    if point == 5 or point == -5:
        return 25 * balance
    # Check whether it is blocked or not
    block = get_blocked_point(board[x][y], board[0-dx][0-dy]) + get_blocked_point(board[x][y], board[x + point * dx][y + point * dy])
    if block == 2:
        return 0
    return (point - block) * 5 * balance

def get_point_dir(x, y, dx, dy, board):
    point = 1
    max_move_step = 5
    while(is_in_board(x+dx, y+dy, board)):
        if(board[x][y] != board[dx+x][dy+y]):
            break #Do not satisfy the condition
        point += 1
        x += dx
        y += dy
        if(point >= max_move_step):
            return point
    return point

def get_blocked_point(pos1, pos2):
    if pos1 == ' ' or pos2 == ' ':
        return 0
    return int(pos1 == pos2)

def best_move_func(board, depth , color, move_history):
    dir = [(0,1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    best_move = (0, 0)
    best_val = -inf
    alpha = -inf
    beta = inf
    for moved_history in move_history:
        for i in range(len(dir)):
            cur_x = moved_history[0] + dir[i][0]
            cur_y = moved_history[1] + dir[i][1]
            print(move_history)
            if (board[cur_x][cur_y] == ' ') :
                board[cur_x][cur_y] = color
                move_history.append((cur_x, cur_y, color)) # Add current node to move_history
                move_val = minimax(board, depth, 'p', move_history, alpha, beta)
                move_history.pop() # Delete current node from move_history
                board[cur_x][cur_y] = ' '
                if (move_val > best_val) :               
                    best_move = (cur_x, cur_y)
                    best_val = move_val
    return best_move

def minimax(board, depth , color, move_history, alpha, beta):
    score = evaluate(board, move_history)
    if(depth == 1):
        return score

    # If robot or player has won the game return the evaluated score
    if (score == 25) :
        return score
    if (score == -25) :
        return score
    # If there are no more moves and no winner then it is a tie
    if (is_empty_board(board)):
        return score
    # If this robot's move
    dir = [(0,1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    if (color == 'r') :    
        best = -inf
        for moved_history in move_history:
            for i in range(len(dir)):
                cur_x = moved_history[0] + dir[i][0]
                cur_y = moved_history[1] + dir[i][1]
                # Check if cell is empty
                if (board[cur_x][cur_y]==' ') :
                    board[cur_x][cur_y] = 'r'
                    move_history.append((cur_x, cur_y, 'r'))
                    best = max(best, minimax(board,depth + 1,'p',move_history, alpha, beta))
                    alpha = max(best, alpha)
                    board[cur_x][cur_y] = ' '
                    move_history.pop()
                    if alpha >= beta:
                        break
        return alpha
 
    # If this minimizer's move
    else :
        best = inf
        for moved_history in move_history:
            for i in range(len(dir)):
                cur_x = moved_history[0] + dir[i][0]
                cur_y = moved_history[1] + dir[i][1]
                # Check if cell is empty
                if (board[cur_x][cur_y]==' '):
                    board[cur_x][cur_y] = 'p'
                    move_history.append((cur_x, cur_y, 'p'))
                    best = min(best, minimax(board,depth + 1,'r',move_history, alpha, beta))
                    beta = min(best, beta)
                    board[cur_x][cur_y] = ' '
                    move_history.pop()
                    if alpha >= beta:
                        break
        return beta
    return 0


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

if __name__ == '__main__':
    '''
    Start a game!
    '''
    initialize(15)
