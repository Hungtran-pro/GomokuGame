import re

def score_of_list_6(lst, c):
    '''
    Return value of the list corresponding to the color
    '''
    total_point=0
    if c == 'p': a = 'r'
    else: a = 'p'
    if lst.find(c*5) != -1: #rrrrr
        return 1000
    elif lst.find(" "+c*4 + " ") != -1:  # ' rrrr ' 
        return 1000
    else:
        lst = re.sub(f'{a}....{a}', '', lst)
        lst = re.sub(f'{a}...{a}', '', lst)
        lst = re.sub(f'{a}..{a}', '', lst)
        lst = re.sub(f'{a}.{a}', '', lst)
        lst = re.sub(f'{a}{a}', '', lst)
        total_point = 7*lst.count("  "+c*3+" ") + 7*lst.count(" "+c*3+"  ") + 5*lst.count(" "+c*3+" ") + 5*lst.count(c*3+" "+c) + 5*lst.count(c+" "+c*3) + 5*lst.count(c*2+" "+c*2) + 3*lst.count(c*4) + 3*lst.count(c*3) + lst.count(c*2)
    return total_point

print(score_of_list_6('rpp p ', 'p'))