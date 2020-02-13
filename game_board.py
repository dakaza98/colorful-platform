import curses



board = open('Ascii board.txt','r')
board_txt = board.read()
board.close



def fix_board(screen):
    screen.clear()
    splitted_board = board_txt.split
    first_line = splitted_board[0]
    _, num_cols = screen.getmaxyx()

    # Add some top margin on the title to get some space between the top and the title
    top_margin = 2

    # All lines start at the same x position so that the ascii art looks like intended
    x = int(num_cols / 2) - int(len(first_line) / 2)

    for index, line in enumerate(splitted_board):
        screen.addstr(index + top_margin, x, splitted_board[index])


    


