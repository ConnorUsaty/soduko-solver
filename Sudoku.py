# Sudoku.py
import sys
import time
import random
import pygame

pygame.init()
pygame.font.init()


def randomize_board(board):
    """Randomizes the playing board"""
    for i in range(15):
        while True:
            spot = random.randint(0, 80)
            row = spot // 9
            col = spot % 9
            if board[row][col] == 0:
                val = random.randint(1, 9)
                if valid_location(board, row, col, val):
                    board[row][col] = val
                    break
    return board


def valid_location(board, row, col, val):
    """Makes sure that number is allowed in selected location"""
    if not (valid_row(board, row, val)):
        return False
    elif not (valid_col(board, col, val)):
        return False
    elif not (valid_box(board, row, col, val)):
        return False
    return True


def valid_row(board, row, val):
    """Makes sure number is not already in row"""
    if val in board[row]:
        return False
    return True


def valid_col(board, col, val):
    """Makes sure number is not already in column"""
    for i in range(0, 9):
        if board[i][col] == val:
            return False
    return True


def valid_box(board, row, col, val):
    """Checks 3x3 sub-box to make sure number is not already used"""
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, (box_row + 3)):
        for j in range(box_col, (box_col + 3)):
            if board[i][j] == val:
                return False
    return True


class Grid:
    """Class for the grid/board"""
    board = [[0 for i in range(9)] for j in range(9)]
    board = randomize_board(board)

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None

    def reset_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = 0
                self.update_model()

    def randomize_board(self):
        for i in range(15):
            while True:
                spot = random.randint(0, 80)
                row = spot // 9
                col = spot % 9
                if self.board[row][col] == 0:
                    val = random.randint(1, 9)
                    if valid_location(self.model, row, col, val):
                        self.board[row][col] = val
                        self.update_model()
                        break

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        # Sets proper gap and sets thickness for sub-box separators
        gap = self.width / 9
        for i in range(1, self.rows + 1):
            if i % 3 == 0:
                thick = 3
            else:
                thick = 1

            # Draws horizontal lines
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            # Draws vertical lines
            pygame.draw.line(self.screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.screen)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            row = pos[1] // gap
            col = pos[0] // gap
            return int(row), int(col)
        else:
            return None

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def place(self, val):
        row, col = self.selected
        if (self.cubes[row][col].value == 0) and (valid_location(self.model, row, col, val)):
            self.cubes[row][col].set(val)
            self.update_model()
            return True
        else:
            self.cubes[row][col].set(0)
            self.cubes[row][col].set_temp(0)
            self.update_model()
            return False

    def find_empty(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cubes[row][col].value == 0:
                    return row, col
        return None

    def game_over(self):
        empty = self.find_empty()
        if empty is not None:
            return False
        elif empty is None:
            return True

    def solve_board(self):
        empty = self.find_empty()
        if empty is None:
            return True
        else:
            row, col = empty

        for i in range(1, 10):
            if valid_location(self.model, row, col, i):
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.screen, True)
                self.update_model()
                pygame.display.update()
                # pygame.time.delay(50)

                if self.solve_board():
                    return True

                self.cubes[row][col].set(0)
                self.cubes[row][col].draw_change(self.screen, False)
                self.update_model()
                pygame.display.update()
                # pygame.time.delay(50)

        return False


class Cube:
    """Class for each of the 81 cubes in the grid"""
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, screen):
        font = pygame.font.SysFont("TimesNewRoman", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), True, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(screen, (pygame.Color('Purple')), (x, y, gap, gap), 3)

    def draw_change(self, screen, g=True):
        font = pygame.font.SysFont("TimesNewRoman", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(screen, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), True, (0, 0, 0))
        screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def update_screen(screen, board, time_secs):
    """Updates game screen"""
    # Fills background white
    screen.fill((255, 255, 255))
    # Draws time
    font = pygame.font.SysFont("TimesNewRoman", 30)
    text = font.render('Time: ' + format_time(time_secs), True, (0, 0, 0))
    text_rect = text.get_rect(center=(540 / 2, 570))
    screen.blit(text, text_rect)
    # Draws board
    board.draw()


def format_time(time_secs):
    """Takes in time in seconds. Outputs time in a minutes : seconds format"""
    seconds = time_secs % 60
    minutes = time_secs // 60
    if seconds < 10:
        return f'{minutes}:0{seconds}'
    return f'{minutes}:{seconds}'


def game_end_screen(screen, completion_time, solver_used):
    """Draws game finished screen"""
    # Uploads background
    bg = pygame.image.load('background.png')
    screen.blit(bg, (0, 0))

    # Draws congratulations message
    font = pygame.font.SysFont("TimesNewRoman", 40)
    text = font.render('Congratulations!', True, (0, 0, 0))
    text_rect = text.get_rect(center=(540/2, 125))
    screen.blit(text, text_rect)

    # Draws time played
    font = pygame.font.SysFont("TimesNewRoman", 25)
    text = font.render('Completion Time:', True, (0, 0, 0))
    screen.blit(text, (100, 185))
    text = font.render(f'{format_time(completion_time)}', True, (0, 0, 0))
    screen.blit(text, (350, 185))

    # Draws solver used yes or no
    text = font.render('Solver Used:', True, (0, 0, 0))
    screen.blit(text, (100, 235))
    if solver_used:
        text = font.render('Yes', True, (0, 0, 0))
    else:
        text = font.render('No', True, (0, 0, 0))
    screen.blit(text, (350, 235))

    # Draws instructions for next steps
    text = font.render('Press Escape to view previous game', True, (0, 0, 0))
    text_rect = text.get_rect(center=(540/2, 450))
    screen.blit(text, text_rect)
    text = font.render('Press Enter to load up a new game', True, (0, 0, 0))
    text_rect = text.get_rect(center=(540/2, 500))
    screen.blit(text, text_rect)


def game_end_loop(screen, board, play_time, solver_used):
    """Loop for game finished screen"""
    game_end = True
    game_end_screen(screen, play_time, solver_used)

    while game_end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    update_screen(screen, board, play_time)
                if event.key == pygame.K_RETURN:
                    game_end = False

        pygame.display.update()


def game_loop(screen):
    """Official game loop"""
    board = Grid(9, 9, 540, 540, screen)
    board.reset_board()
    board.randomize_board()
    start_time = time.time()
    num = None
    solver_used = False
    running = True

    while running:

        play_time = round(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    num = 1
                if event.key == pygame.K_2:
                    num = 2
                if event.key == pygame.K_3:
                    num = 3
                if event.key == pygame.K_4:
                    num = 4
                if event.key == pygame.K_5:
                    num = 5
                if event.key == pygame.K_6:
                    num = 6
                if event.key == pygame.K_7:
                    num = 7
                if event.key == pygame.K_8:
                    num = 8
                if event.key == pygame.K_9:
                    num = 9

                if event.key == pygame.K_RETURN:
                    row, col = board.selected
                    if board.cubes[row][col].temp != 0:
                        board.place(board.cubes[row][col].temp)
                    num = None

                if event.key == pygame.K_SPACE:
                    solver_used = True
                    board.solve_board()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    num = None

        if board.selected and num is not None:
            board.sketch(num)

        update_screen(screen, board, play_time)
        pygame.display.update()

        if board.game_over():
            running = False
    return board, round(time.time() - start_time), solver_used


def main():
    """Main loop to rotate through game loop and game over loop"""
    screen = pygame.display.set_mode((540, 600))
    while True:
        board, finish_time, solver_used = game_loop(screen)
        game_end_loop(screen, board, finish_time, solver_used)


if __name__ == '__main__':
    main()
