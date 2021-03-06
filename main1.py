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
    # ch???ng n??o yf,xf kh??ng c?? trong board
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

def get_points(lst,x,y):
	total_point=0
	if lst.find(x*5) != -1: #rrrrr
		return 100
	elif lst.find(" "+x*4 + " ") != -1:  # ' rrrr ' 
		return 90
	else:
		if(lst.find(y+x*4+y)) != -1:   #'prrrrp'
			lst.replace(y+x*4+y,y*2)
		if(lst.find(y+x*3+" "+x+y)) != -1: #'prrr rp'
			lst.xeplace(y+x*3+" "+x+y,y*2)
		if(lst.find(y+x+" "+x*3+y)) != -1:#'pr rrrp'
			lst.replace(y+x+" "+x*3+y,y*2) 
		if(lst.find(y+x*2+" "+x*2+y)) != -1:  #'prr rrp'
			lst.replece(y+x*2+" "+x*2+y,y*2)
		if(lst.find(y+x*3+y)) != -1 :  #'prrrp'
			lst.replace(y+x*3+y,y*2)  
		if(lst.find(y+x*2+y)) != -1: #'prrp'
			lst.replace(y+x*2+y,y*2) 
		if(lst.find(y+x+y)) != -1:  #'prp'
			lst.replace(y+x+y,y*2)
		total_point = 5*lst.count(" "+x*3+" ") + 2*lst.count(x*3+" "+x) + 2*lst.count(x+" "+x*3) + 5*lst.count(x*2+" "+x*2) + 4*lst.count(x*4) + 4*lst.count(x*3) + lst.count(x*2)
	return total_point


def score_of_cord_color(board,x,y,status):
    '''
    Return maximum points for the move (x, y)
    '''
    if(status=='attack'):
        p1,p2 = 'r','p'
    else:
        p1,p2= 'p','r'
    score = 0
    score = score +  get_points(''.join(get_list(board,march(board,x,y,0,-1,4), 0, 1,march(board,x,y,0,1,4))),p1,p2)
    
    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,0,4), 1, 0,march(board,x,y,1,0,4))),p1,p2)
    
    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,-1,4), 1, 1,march(board,x,y,1,1,4))),p1,p2)

    score = score + get_points(''.join(get_list(board,march(board,x,y,-1,1,4), 1,-1,march(board,x,y,1,-1,4))),p1,p2)
    
    return score


def get_score(board,color,anticol,x,y):
    '''
    Try play at (x,y) and get the score the move.
    '''

    #Attack
    board[x][y] = color
    score1 = score_of_cord_color(board,x,y,'attack')
    #Defence
    board[x][y] = anticol
    score2 = score_of_cord_color(board,x,y,'defence')
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
    
    if win == True:
        print("Plase turn off the canvas!")
        return

    if not is_in_board(x, y, board): # do nothing if it's out of board
        return

    if board[x][y] == ' ':
        draw_circle(x, y, colors[person])
        board[x][y] = person
        move_history.append((x, y, person))
        if 5 == evaluate_win_state(board, move_history, person): # Check the state after person's move
            print("Person win!")
            win = True
            return

        if (is_full_filled_board(board) == True) :
            print("Draw")
            win = True
            return
        rx, ry = best_move_func(board, 0, 'r')
        draw_circle(rx, ry, colors[robot])
        board[rx][ry] = robot
        move_history.append((rx, ry, robot))

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