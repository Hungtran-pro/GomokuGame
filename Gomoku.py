import turtle
from cmath import inf 

def is_in_board(x, y, board):
    '''
    Check whether the clicked position is in board or not
    '''
    return 0 <= x <= len(board) - 1 and 0 <= y <= len(board) - 1

def is_empty_board(board):
    '''
    Check whether the board is empty or not
    '''
    return board == ([[' '] * len(board)] * len(board))

def is_full_filled_board(board):
    for i in range(len(board)):
        if " " in board[i]:
            return False
    return True

def make_board(size):
    board = []
    for i in range(size):
        board.append([" "]*size)
    return board

def get_list(board,cord_s,dx,dy,cord_d):
    '''
    Return a list including the value of each cell (' ' or 'p' or 'r')
        x, y: the coordinates (x, y) of the start point of the list
        xd, yd: the coordicates (x, y) of the destination point of the list
        dx, dy: direction moves
    '''
    x, y = cord_s
    xd,yd = cord_d
    lst = []
    while  x != xd + dx or y != yd + dy:
        lst.append(board[x][y])
        x += dx
        y += dy
    return lst

def score_of_list(lst, color):
    '''
    Return value of the list corresponding to the color
    '''
    blank = lst.count(' ')
    filled = lst.count(color)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

def score_of_full_list(board,cord_s,dx,dy,cord_d,color):
    '''
    Return a list containing marks corresponding to an 5-element list
        cord_s: a tuple contains the coordinates (x, y) of the start point of the list
        cord_d: a tuple contains the coordicates (x, y) of the destination point of the list
        dx, dy: direction moves
        color: indicate color of robot of person
    '''
    scores = []
    row = get_list(board,cord_s,dx,dy,cord_d)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],color)
        scores.append(score)
    
    return scores

def summarize_score(score_dir):
    '''
    Get the highest score of all directions
    '''
    score_max = -1
    for key in score_dir:
        score_max_tmp = -1
        score_max_tmp = max(max(score_dir[key]),score_max_tmp)
        score_max = max(score_max, score_max_tmp)
    return score_max

def evaluate_win_state(board, move_history, color):
    '''
    Evaluate the current state of the board (WIN or KEEP PLAYING)
    Đánh giá trạng thái hiện tại của bảng (Thắng hay tiếp tục chơi)
    '''

    score_dir = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    board_length = len(board)
    for i in range(board_length):
        score_dir[(0,1)].extend(score_of_full_list(board,(i, 0), 0, 1,(i,board_length-1), color))
        score_dir[(1,0)].extend(score_of_full_list(board,(0, i), 1, 0,(board_length-1,i), color))
        score_dir[(1,1)].extend(score_of_full_list(board,(i, 0), 1,1,(board_length-1,board_length-1-i), color))
        score_dir[(-1,1)].extend(score_of_full_list(board,(i,0), -1, 1,(0,i), color))
        
        if i + 1 < len(board):
            score_dir[(1,1)].extend(score_of_full_list(board,(0, i+1), 1, 1,(board_length-2-i,board_length-1), color)) 
            score_dir[(-1,1)].extend(score_of_full_list(board,(board_length -1 , i + 1), -1,1,(i+1,board_length-1), color))
    
    return summarize_score(score_dir)

def march(board,x,y,dx,dy,length):
    '''
    Find the furthest available move
    '''
    xd = x + length*dx
    yd = y + length*dy 
    # chừng nào yf,xf không có trong board
    while not is_in_board(xd,yd,board):
        yd -= dy
        xd -= dx
        
    return xd,yd

def possible_moves(board):  
    '''
    Initilize a list of unmarked cell within a radius of 3 unit
        taken: a list stores marked cell in the board (played by person and robot)
        direction: contains 8 directions
        cords: stores unmarked cell in the board

    '''
    taken = []
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    cord = []
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))

    for direction in directions:
        dx,dy = direction
        for coord in taken:
            x,y = coord
            for length in [1]:
                move = march(board,x,y,dx,dy,length)
                if move not in taken and move not in cord:
                    cord.append(move)
    return cord

CONSTANT_LST = ['rrrrr','prrrrp', 'prrrr', 'rrrrp', 'rrrr', 'prrr', 'rrrp', 'rrr'
, 'rrr r', 'r rrr', 'rr rr', 'prrr rp', 'pr rrrp','prr rrp'
, 'prr r', 'pr rr', 'r rrp', 'rr rp', 'prrp', 'prr', 'rrp', 'r']

def get_points(lst):
    total_point = 0
    if lst.find('rrrrr') != -1:
        return 100
    elif(lst.find(' rrrr ') != -1):
        return 90
    else:
        if(lst.find('prrrrp') != -1):
            lst.replace('prrrrp', 'pp')
        if(lst.find('prrr rp') != -1):
            lst.replace('prrr rp', 'pp')
        if(lst.find('pr rrrp') != -1):
            lst.replace('pr rrrp', 'pp')
        if(lst.find('prr rrp') != -1):
            lst.replace('prr rrp', 'pp')
        if(lst.find('prrrp') != -1):
            lst.replace('prrrp', 'pp')
        if(lst.find('prrp') != -1):
            lst.replace('prrp', 'pp')
        if(lst.find('prp') != -1):
            lst.replace('prp', 'pp')
        total_point = 5*lst.count(' rrr ') + 2*lst.count('rrr r') + 2*lst.count('r rrr') + 5*lst.count('rr rr') + 4*lst.count('rrrr') + 4*lst.count('rrr') + lst.count('rr')
    return total_point

def get_points_anti(lst):
    total_point = 0
    if lst.find('ppppp') != -1:
        return 100
    elif lst.find(' pppp ') != -1:
        return 90
    else:
        if(lst.find('rppppr') != -1):
            lst.replace('rppppr', 'rr')
        if(lst.find('rppp pr') != -1):
            lst.replace('rppp pr', 'rr')
        if(lst.find('rp pppr') != -1):
            lst.replace('rp pppr', 'rr')
        if(lst.find('rpp ppr') != -1):
            lst.replace('rpp ppr', 'rr')
        if(lst.find('rpppr') != -1):
            lst.replace('rpppr', 'rr')
        if(lst.find('rppr') != -1):
            lst.replace('rppr', 'rr')
        if(lst.find('rpr') != -1):
            lst.replace('rpr', 'rr')
        total_point = 5*lst.count(' ppp ') + 4*lst.count('ppp p') + 2*lst.count('p ppp') + 4*lst.count('pp pp') + 4*lst.count('pppp') + 3*lst.count('ppp') + lst.count('pp')
    return total_point

def score_of_cord_color(board,x,y):
    '''
    Return maximum points for the move (x, y)
    '''
    score = 0
    score = score +  get_points(''.join(get_list(board,march(board,x,y,0,-1,4), 0, 1,march(board,x,y,0,1,4))))
    
    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,0,4), 1, 0,march(board,x,y,1,0,4))))
    
    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,-1,4), 1, 1,march(board,x,y,1,1,4))))

    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,1,4), 1,-1,march(board,x,y,1,-1,4))))
    
    return score

def score_of_cord_anticol(board,x,y):
    '''
    Return maximum points for the move (x, y)
    '''
    score = 0
    score = score +  get_points_anti(''.join(get_list(board,march(board,x,y,0,-1,4), 0, 1,march(board,x,y,0,1,4))))
    
    score = score + get_points_anti(''.join(get_list(board,march(board,x,y,-1,0,4), 1, 0,march(board,x,y,1,0,4))))
    
    score = score + get_points_anti(''.join(get_list(board,march(board,x,y,-1,-1,4), 1, 1,march(board,x,y,1,1,4))))

    score = score + get_points_anti(''.join(get_list(board,march(board,x,y,-1,1,4), 1,-1,march(board,x,y,1,-1,4))))
    
    return score

def get_score(board,color,anticol,x,y):
    '''
    Try play at (x,y) and get the score the move.
    '''

    #Attack
    board[x][y] = color
    score1 = score_of_cord_color(board,x,y)
    #Defence
    board[x][y] = anticol
    score2 = score_of_cord_anticol(board,x,y)
    board[x][y] = ' '
    return max(score1, score2)

def best_move_func(board, depth , color):
    '''
    Return a tuple containing the cordinates (x, y) for the next move with highest points
        depth: the depth of algorithm
        max_move: the best move we can archieve
        max_score: the best score we can archieve
    '''
    if color == 'p':
        anticol = 'r'
    else: anticol = 'p'

    max_move = (0,0)
    max_score = 0
    moves = possible_moves(board)
    for move in moves:
        x,y = move
        if max_score == 0:
            score_tmp = get_score(board,color,anticol,x,y)
            max_score = score_tmp
            max_move = move
        else:
            score_tmp = get_score(board,color,anticol,x,y)
            if score_tmp > max_score:
                max_score = score_tmp
                max_move = move
    print(max_score)
    return max_move


def minimax(board, depth , color, move_history, alpha, beta):
    score = evaluate_win_state(board, move_history)
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
    person = 'p'
    robot = 'r'
    x, y = getIndexPosition(x, y)
    
    # Đã chiến thắng, dừng chơi.
    if win == True:
        print("Plase turn off the canvas!")
        return

    # Click chuột ra ngoài bảng
    if not is_in_board(x, y, board): # do nothing if it's out of board
        return

    # Bắt đầu điền vị trí ô (người đánh)
    if board[x][y] == ' ':
        draw_circle(x, y, colors[person])
        board[x][y] = person
        move_history.append((x, y, person))
        
        # Điều kiện 5 con thẳng hàng.
        if 5 == evaluate_win_state(board, move_history, person): # Check the state after person's move
            print("Person win!")
            win = True
            return

        # Hết ô trống.
        if (is_full_filled_board(board) == True) :
            print("Draw")
            win = True
            return

        # Bắt đầu máy đánh.
        rx, ry = best_move_func(board, 0, 'r')
        draw_circle(rx, ry, colors[robot])
        board[rx][ry] = robot
        move_history.append((rx, ry, robot))

        # Nếu 5 con thẳng hàng
        if 5 == evaluate_win_state(board, move_history, robot): # Check the state after robot's move
            print("Robot win!")
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