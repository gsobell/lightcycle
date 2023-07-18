#!/usr/bin/env python3
from sys import argv, exit
import curses
from random import choice
from curses import wrapper

# Paths:
h = '─'
v = '│'
turn = ['┌', '┐', '└', '┘']

# Consts
VERSION = "0.1.0"
DIRECTIONS = [curses.KEY_UP, curses.KEY_DOWN,
              curses.KEY_LEFT, curses.KEY_RIGHT]
V = [curses.KEY_UP, curses.KEY_DOWN]
H = [curses.KEY_LEFT, curses.KEY_RIGHT]

# Global defaults:
FPS = 30
COLOR = 2       # user, 1-3
SCORE = [0, 0]  # user v. program


# Flag handling:
def show_usage():
    print("\033[1;94mlight\033[0m\033[1;96mcycle\033[0m.py")
    print("the grid, in your terminal")
    print("usage: python lightcycle.py [options]")
    print("Options:")
    print(" -h,  --help     display this help message")
    print(" -v,             print version number.")


def flag_error():
    print("One or more arguments are invalid.")
    show_usage()
    exit()


def flags():
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "-h" or arg == "--help":
            show_usage()
            exit()
        elif arg == "-v":
            print(f"version {VERSION}")
            exit()
        i += 1


def curses_setup(stdscr):
    stdscr.clear()   # Clear the screen
    curses.noecho()  # Turn off echoing of keys
    curses.cbreak()  # Turn off normal tty line buffering
    stdscr.keypad(True)     # Enable keypad mode

    curses.curs_set(0)      # Hide cursor
    curses.start_color()    # Enable colors if supported
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # user
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # user
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)   # user
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # CLU
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # program
    stdscr.refresh()


def get_input(c, head, heading):
    if c == curses.KEY_LEFT or c == ord('h'):
        if heading != curses.KEY_RIGHT:
            return curses.KEY_LEFT, (head[0], head[1] - 1)
    elif c == curses.KEY_RIGHT or c == ord('l'):
        if heading != curses.KEY_LEFT:
            return curses.KEY_RIGHT, (head[0], head[1] + 1)
    elif c == curses.KEY_UP or c == ord('k'):
        if heading != curses.KEY_DOWN:
            return curses.KEY_UP, (head[0] - 1, head[1])
    elif c == curses.KEY_DOWN or c == ord('j'):
        if heading != curses.KEY_UP:
            return curses.KEY_DOWN, (head[0] + 1, head[1])
    return get_input(heading, head, heading)  # recursive call


def is_valid(head, visited):
    if ((head in visited) or
            head[1] > curses.COLS - 2 or
            head[0] > curses.LINES - 2 or
            head[0] <= 0 or head[1] <= 0):
        return False
    return True


def adjacent(cell):
    """Returns in same order as DIRECTIONS"""
    y, x = cell
    return [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]


def genmove1(program, program_dir, user, visited):
    adj = adjacent(program)
    moves = []
    for i, a in enumerate(adj):
        if is_valid(a, visited):
            if DIRECTIONS[i] == program_dir:
                moves.append(DIRECTIONS[i])
            else:
                if is_valid(adjacent(a)[i], visited):
                    moves.append(DIRECTIONS[i])
    # Calculate the differences in coordinates between AI and user
    diff = (user[0] - program[0], user[1] - program[1])
    # Check if the user is above or below the AI
    if abs(diff[0]) > abs(diff[1]):
        if diff[0] > 0 and (program_dir != curses.KEY_UP):
            if curses.KEY_DOWN in moves:
                return curses.KEY_DOWN
        elif diff[0] < 0 and (program_dir != curses.KEY_DOWN):
            if curses.KEY_UP in moves:
                return curses.KEY_UP
        else:
            # Move left or right to avoid getting stuck
            if program_dir != curses.KEY_LEFT:
                if curses.KEY_RIGHT in moves:
                    return curses.KEY_RIGHT
            else:
                if curses.KEY_LEFT in moves:
                    return curses.KEY_LEFT
    else:
        # Check if the user is on the left or right side of the AI
        if diff[1] > 0 and (program_dir != curses.KEY_LEFT):
            if curses.KEY_RIGHT in moves:
                return curses.KEY_RIGHT
        elif diff[1] < 0 and (program_dir != curses.KEY_RIGHT):
            if curses.KEY_LEFT in moves:
                return curses.KEY_LEFT
        else:
            # Move up or down to avoid getting stuck
            if program_dir != curses.KEY_UP:
                if curses.KEY_DOWN in moves:
                    return curses.KEY_DOWN
            else:
                if curses.KEY_UP in moves:
                    return curses.KEY_UP
    if moves:
        return program_dir if program_dir in moves else choice(moves)
    else:
        return program_dir


def genmove(program, program_dir, user, visited):
    adj = adjacent(program)
    moves = []
    for i, a in enumerate(adj):
        if is_valid(a, visited):
            if DIRECTIONS[i] == program_dir:
                moves.append(DIRECTIONS[i])
            else:
                if is_valid(adjacent(a)[i], visited):
                    moves.append(DIRECTIONS[i])
    if moves:
        return program_dir if program_dir in moves else choice(moves)
    else:
        return program_dir


# forward declaration?
AI = genmove
AI_COLOR = 4


def draw_cycle(stdscr, head, heading, prev_head, prev_heading, color):
    if heading == curses.KEY_LEFT:
        if prev_heading == curses.KEY_UP:
            stdscr.addstr(*prev_head, turn[1], curses.color_pair(color))
        if prev_heading == curses.KEY_DOWN:
            stdscr.addstr(*prev_head, turn[3], curses.color_pair(color))
        stdscr.addstr(*head, h, curses.color_pair(color))
    if heading == curses.KEY_RIGHT:
        if prev_heading == curses.KEY_UP:
            stdscr.addstr(*prev_head, turn[0], curses.color_pair(color))
        if prev_heading == curses.KEY_DOWN:
            stdscr.addstr(*prev_head, turn[2], curses.color_pair(color))
        stdscr.addstr(*head, h, curses.color_pair(color))
    if heading == curses.KEY_UP:
        if prev_heading == curses.KEY_LEFT:
            stdscr.addstr(*prev_head, turn[2], curses.color_pair(color))
        if prev_heading == curses.KEY_RIGHT:
            stdscr.addstr(*prev_head, turn[3], curses.color_pair(color))
        stdscr.addstr(*head, v, curses.color_pair(color))
    if heading == curses.KEY_DOWN:
        if prev_heading == curses.KEY_LEFT:
            stdscr.addstr(*prev_head, turn[0], curses.color_pair(color))
        if prev_heading == curses.KEY_RIGHT:
            stdscr.addstr(*prev_head, turn[1], curses.color_pair(color))
        stdscr.addstr(*head, v, curses.color_pair(color))


def play(stdscr):
    global SCORE
    global AI, AI_COLOR
    visited = []
    screen_height, screen_width = stdscr.getmaxyx()
    center_y = screen_height // 2
    center_x = screen_width // 2
    user = center_y, center_x + 30
    user_dir = curses.KEY_LEFT
    program = center_y, center_x - 30
    program_dir = curses.KEY_RIGHT
    while True:
        # user:
        prev_user, prev_user_dir = user, user_dir
        user_dir, user = get_input(stdscr.getch(), user, user_dir)
        draw_cycle(stdscr, user, user_dir, prev_user, prev_user_dir, COLOR)
        if not is_valid(user, visited):
            SCORE[1] += 1
            break
        visited.append(user)
        # program
        prev_program, prev_program_dir = program, program_dir
        c = AI(program, program_dir, user, visited)
        program_dir, program = get_input(c, program, program_dir)
        draw_cycle(stdscr, program, program_dir,
                   prev_program, prev_program_dir, AI_COLOR)
        if not is_valid(program, visited):
            SCORE[0] += 1
            break
        visited.append(program)
        if user_dir in V:
            if program_dir in H:
                curses.napms(int(1000/FPS))
                prev_program, prev_program_dir = program, program_dir
                c = AI(program, program_dir, user, visited)
                program_dir, program = get_input(c, program, program_dir)
                draw_cycle(stdscr, program, program_dir,
                           prev_program, prev_program_dir, AI_COLOR)
                if not is_valid(program, visited):
                    SCORE[0] += 1
                    break
                visited.append(program)
                curses.napms(int(1000/FPS))
            else:
                curses.napms(int(2000/FPS))
        elif program_dir in V:
            if user_dir in H:
                curses.napms(int(1000/FPS))
                prev_user, prev_user_dir = user, user_dir
                user_dir, user = get_input(stdscr.getch(), user, user_dir)
                draw_cycle(stdscr, user, user_dir,
                           prev_user, prev_user_dir, COLOR)
                if not is_valid(user, visited):
                    SCORE[1] += 1
                    break
                visited.append(user)
                curses.napms(int(1000/FPS))
        else:
            curses.napms(int(1000/FPS))


def draw_menu(stdscr, selected_row_idx, items):
    for idx, item in enumerate(items):
        x = curses.COLS // 2 - len(item) // 2
        y = curses.LINES // 2 - len(items) // 2 + idx
        if idx == selected_row_idx:
            stdscr.addstr(y, x, f"> {item} <",
                          curses.A_BOLD | curses.color_pair(COLOR))
        else:
            stdscr.addstr(y, x, f"  {item}  ")
    stdscr.refresh()


def clear_menu(stdscr, items):
    for idx in range(len(items)):
        x = curses.COLS // 2 - len(items[idx]) // 2
        y = curses.LINES // 2 - len(items) // 2 + idx
        stdscr.addstr(y, x, " " * (len(items[idx]) + 4))
    stdscr.refresh()


def speed(stdscr):
    global FPS
    level = FPS // 10
    x = curses.COLS // 2
    y = curses.LINES // 2 - 1
    stdscr.addstr(y, x, f"< {level} >", curses.A_BOLD | curses.color_pair(3))
    stdscr.addstr(y + 2, x - 12,
                  "Use ← → to select, then enter.", curses.color_pair(3))
    while True:
        stdscr.addstr(y, x, f"< {level} > ",
                      curses.A_BOLD | curses.color_pair(3))
        stdscr.refresh()
        c = stdscr.getch()
        if c == curses.KEY_RIGHT:
            level += 1
        elif c == curses.KEY_LEFT:
            level = max(level - 1, 1)
        elif c == ord('\n') or c == ord(' '):
            FPS = level * 10
            stdscr.move(y + 2, x - 12)  # clear help msg
            stdscr.clrtoeol()
            break


def select_ai(stdscr):
    global AI
    global AI_COLOR
    if AI_COLOR == 4:
        selected, old_selected = 1, 0
    else:
        selected, old_selected = 0, 1
    x = curses.COLS // 2
    y = curses.LINES // 2 - 1
    e = len("Rinzler" + "CLU")
    stdscr.addstr(y, x - e // 2, "Rinzler", curses.color_pair(4))
    stdscr.addstr(y, x + e // 2, "CLU", curses.color_pair(5))
    stdscr.addstr(y + 2, x - 12,
                  "Use ← → to select, then enter.", curses.color_pair(3))
    while True:
        stdscr.addstr(y + 1, x + (selected * - 6) + 6, "^ ", curses.A_BLINK)
        if old_selected != selected:
            stdscr.addstr(y + 1, x + (old_selected * - 6) + 6,
                          "  ", curses.A_BLINK)
        stdscr.refresh()
        old_selected = selected
        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            selected = (selected - 1) % 2
        elif c == curses.KEY_RIGHT:
            selected = (selected + 1) % 2
        elif c == ord('\n') or c == ord(' '):
            if selected == 1:
                AI = genmove
                AI_COLOR = 4
            elif selected == 0:
                AI = genmove1
                AI_COLOR = 5
            stdscr.move(y + 2, x - 12)  # clear help msg
            stdscr.clrtoeol()
            stdscr.move(y + 1, x - 12)
            stdscr.clrtoeol()
            stdscr.move(y, x - 12)
            stdscr.clrtoeol()
            break


def select_color(stdscr):
    global COLOR
    selected = 1
    old_selected = 0
    x = curses.COLS // 2
    y = curses.LINES // 2 - 1
    stdscr.addstr(y, x - 2, "  ", curses.A_REVERSE | curses.color_pair(1))
    stdscr.addstr(y, x + 1, "  ", curses.A_REVERSE | curses.color_pair(2))
    stdscr.addstr(y, x + 4, "  ", curses.A_REVERSE | curses.color_pair(3))
    stdscr.addstr(y + 2, x - 12,
                  "Use ← → to select, then enter.", curses.color_pair(3))
    while True:
        stdscr.addstr(y + 1, x + selected * 3 - 2, "^ ", curses.A_BLINK)
        if old_selected != selected:
            stdscr.addstr(y + 1, x + old_selected * 3 - 2,
                          "  ", curses.A_BLINK)
        stdscr.refresh()
        old_selected = selected
        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            selected = (selected - 1) % 3
        elif c == curses.KEY_RIGHT:
            selected = (selected + 1) % 3
        elif c == ord('\n') or c == ord(' '):
            COLOR = selected + 1
            stdscr.move(y + 1, x - 12)  # clear cursor
            stdscr.clrtoeol()
            stdscr.move(y + 2, x - 12)  # clear help msg
            stdscr.clrtoeol()
            break


def controls(stdscr, y):
    y += 1
    messages = ["Greetings user.",
                "Steer with arrow or vim keys.",
                "Press any key to continue"]
    for m in messages:
        # x_centered = x - len(m) // 2
        x = curses.COLS // 2 - len(m) // 2 + 2
        stdscr.addstr(y, x, m, curses.color_pair(3))
        if m == messages[2]:
            stdscr.addstr(y, x, m, curses.color_pair(3) | curses.A_BLINK)
        stdscr.refresh()
        stdscr.getch()
        y += 1
    for _ in messages:
        stdscr.move(y - len(messages), 0)
        stdscr.clrtoeol()
        y += 1
    stdscr.refresh()


def menu(stdscr):
    title = ["light", "cycle"]
    items = ["Start", " Color", "Speed", 'AI', "Rules",  "Exit"]
    x = curses.COLS // 2 - len(title[0] + title[1]) // 2 + 2
    y = curses.LINES // 2 - len(items) // 2 - 1
    stdscr.addstr(y, x, title[0], curses.A_BOLD | curses.color_pair(3))
    stdscr.addstr(y, x+5, title[1], curses.A_BOLD | curses.color_pair(2))
    current_row = 0
    while True:
        draw_menu(stdscr, current_row, items)
        c = stdscr.getch()
        if c == curses.KEY_UP:
            current_row = (current_row - 1) % len(items)
        elif c == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(items)
        elif c == ord('\n') or c == ord(' '):
            if current_row == 0:
                stdscr.clear()
                return
            elif current_row == 1:  # color
                clear_menu(stdscr, items)
                select_color(stdscr)
            elif current_row == 2:  # speed
                clear_menu(stdscr, items)
                speed(stdscr)
            elif current_row == 3:  # ai
                clear_menu(stdscr, items)
                select_ai(stdscr)
            elif current_row == 4:  # controls
                clear_menu(stdscr, items)
                controls(stdscr, y)
            elif current_row == len(items) - 1:
                exit()


def play_again(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    y, x = stdscr.getmaxyx()
    y //= 2
    x //= 2
    while True:
        score = f"USER:{SCORE[0]} PROGRAM:{SCORE[1]}"
        stdscr.addstr(y - 1, x - len(score) // 2, score,
                      curses.color_pair(3) | curses.A_DIM)
        stdscr.addstr(y, x - len("Play again?") // 2, "Play again?",
                      curses.color_pair(2))
        stdscr.addstr(y + 1, x - 2, "Yes", curses.color_pair(3))
        stdscr.addstr(y + 1, x + 2, "No", curses.color_pair(4))
        stdscr.addstr(y + 2, x - 1, "^")
        stdscr.refresh()
        again = True
        while True:
            c = stdscr.getch()
            if c == 10 or c == ord(" "):
                stdscr.clear()
                if again:
                    return True
                return False
            elif c == ord('y'):
                stdscr.clear()
                return
            elif c == ord('n') or c == ord('q'):
                return False
            if (c in H) or c == ord('h') or c == ord('l'):
                if again:
                    stdscr.addstr(y + 2, x + 2, "^")
                    stdscr.addstr(y + 2, x - 1, " ")
                    again = False
                else:
                    stdscr.addstr(y + 2, x - 1, "^")
                    stdscr.addstr(y + 2, x + 2, " ")
                    again = True


def main(stdscr):
    curses_setup(stdscr)
    while True:
        menu(stdscr)
        stdscr.nodelay(1)  # Enable non-blocking input mode
        while True:
            play(stdscr)
            stdscr.nodelay(0)
            if not play_again(stdscr):
                break
            stdscr.nodelay(1)


if __name__ == "__main__":
    flags()
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print('END OF LINE')
    except curses.error:
        print("Terminal not large enough, resize and try again.")
