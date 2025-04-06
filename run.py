import curses
import random

def draw_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def settings_menu(stdscr):
    options = [
        ("Slow", 150),
        ("Normal", 100),
        ("Fast", 60),
        ("Extreme", 30)
    ]
    selected = 1
    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Settings - Pilih kecepatan:")
        for i, (label, _) in enumerate(options):
            if i == selected:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(3+i, 4, f"> {label}")
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(3+i, 6, label)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:
            return options[selected][1]

def skin_menu(stdscr, current_skin, current_color):
    skins = ['#', '*', 'O', '@', '+']
    colors = [
        ("Green", 1),
        ("Cyan", 4),
        ("Magenta", 5),
        ("Yellow", 2),
        ("Blue", 6)
    ]
    selected_skin = 0
    selected_color = 0
    stage = 0

    while True:
        stdscr.clear()
        if stage == 0:
            stdscr.addstr(1, 2, "Custom Skin - Pilih karakter ular:")
            for i, s in enumerate(skins):
                if i == selected_skin:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(3+i, 4, f"> {s}")
                    stdscr.attroff(curses.color_pair(2))
                else:
                    stdscr.addstr(3+i, 6, s)
        elif stage == 1:
            stdscr.addstr(1, 2, "Custom Skin - Pilih warna ular:")
            for i, (label, color_code) in enumerate(colors):
                if i == selected_color:
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(3+i, 4, f"> {label}")
                    stdscr.attroff(curses.color_pair(2))
                else:
                    stdscr.addstr(3+i, 6, label)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            if stage == 0:
                selected_skin = (selected_skin - 1) % len(skins)
            else:
                selected_color = (selected_color - 1) % len(colors)
        elif key == curses.KEY_DOWN:
            if stage == 0:
                selected_skin = (selected_skin + 1) % len(skins)
            else:
                selected_color = (selected_color + 1) % len(colors)
        elif key in [10, 13]:
            if stage == 0:
                stage = 1
            else:
                return skins[selected_skin], colors[selected_color][1]

def play_game(stdscr, speed, skin_char, color_pair):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(speed)

    snake = [[sh//2, sw//4 + i] for i in range(3)][::-1]
    food = [sh//2, sw//2]
    win.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(3))

    direction = curses.KEY_RIGHT
    score = 0

    while True:
        key = win.getch()
        if key != -1:
            if (key == curses.KEY_UP and direction != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and direction != curses.KEY_UP) or \
               (key == curses.KEY_LEFT and direction != curses.KEY_RIGHT) or \
               (key == curses.KEY_RIGHT and direction != curses.KEY_LEFT):
                direction = key

        head = [snake[0][0], snake[0][1]]
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1
        snake.insert(0, head)

        if head == food:
            score += 1
            while True:
                food = [random.randint(1, sh-2), random.randint(1, sw-2)]
                if food not in snake:
                    break
            win.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(3))
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        if head[0] in [0, sh-1] or head[1] in [0, sw-1] or head in snake[1:]:
            break

        win.addch(head[0], head[1], skin_char, curses.color_pair(color_pair))
        win.addstr(0, 2, f'Skor: {score}', curses.color_pair(2))

    win.clear()
    msg1 = "GAME OVER!"
    msg2 = f"Skor akhir: {score}"
    msg3 = "Tekan 1 untuk main lagi atau Q untuk keluar"
    win.addstr(sh // 2 - 1, sw // 2 - len(msg1)//2, msg1, curses.color_pair(2))
    win.addstr(sh // 2, sw // 2 - len(msg2)//2, msg2, curses.color_pair(2))
    win.addstr(sh // 2 + 1, sw // 2 - len(msg3)//2, msg3, curses.color_pair(2))
    win.refresh()

    while True:
        retry = win.getch()
        if retry == ord('1'):
            return True
        elif retry in [ord('q'), ord('Q')]:
            return False

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_BLUE, -1)

    speed = 100
    skin_char = '#'
    skin_color = 1

    menu = ['Play', 'Settings', 'Custom Skin', 'Exit']
    selected_idx = 0

    while True:
        draw_menu(stdscr, selected_idx, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % len(menu)
        elif key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % len(menu)
        elif key in [10, 13]:  # Enter
            if menu[selected_idx] == 'Play':
                play_again = play_game(stdscr, speed, skin_char, skin_color)
                if not play_again:
                    break
            elif menu[selected_idx] == 'Settings':
                speed = settings_menu(stdscr)
            elif menu[selected_idx] == 'Custom Skin':
                skin_char, skin_color = skin_menu(stdscr, skin_char, skin_color)
            elif menu[selected_idx] == 'Exit':
                break

curses.wrapper(main)
