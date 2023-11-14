import time, random, csv
que = -1 #Чей ход: -1 - крестики, 0 - нолики
move = None 
game_amount = 0

grid = [0, 0, 0, 0, 0, 0, 0, 0, 0] #Игровое поле

last_game = []#Запись поля игры плюс 1 - чей следующий ход, 2 - колличество стадий
stage = []
move_stage = []
moves = []

winner = None
draw = False

def win_checker():
    global grid, winner, draw

    for row in range(0, 7, 3):
        if (grid[row] == grid[row +1] == grid[row + 2]) and (grid[row] != 0):
            winner = grid[row]
            break

    for column in range(3):
        if (grid[column] == grid[column+3] == grid[+6]) and (grid[column] != 0):
            winner = grid[column]
            break
    
    if (grid[0] == grid[4] == grid[8]) and (grid[0] != 0):
        winner = grid[0]

    if (grid[2] == grid[4] == grid[6]) and (grid[2] != 0):
        winner = grid[2]

    if (grid.count(0) == 0) and winner is None:
        draw = True


    if winner == -1:
        data_save()
    if winner == 1:
        data_save()

    if draw:
        data_save()


def check_next_move():
    global grid, mov_grid, move
    mov_grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    move = None

    for row in range(0, 7, 3):
        r = grid[row] + grid[row + 1] + grid[row + 2]
        if abs(r) == 2:
            if grid[row] == 0:
                mov_grid[row] = (abs(mov_grid[row]) + abs(int(r/2))) * int(r/2)
            elif grid[row + 1] == 0:
                mov_grid[row+1] = (abs(mov_grid[row+1]) + abs(int(r/2))) * int(r/2)
            elif grid[row + 2] == 0:
                mov_grid[row + 2] = (abs(mov_grid[row + 2]) + abs(int(r/2))) * int(r/2)

    for column in range(3):
        r = grid[column] + grid[column + 3] + grid[column + 6]
        if abs(r) == 2:
            if grid[column] == 0:
                mov_grid[column] = (abs(mov_grid[column]) + abs(int(r/2))) * int(r/2)
            elif grid[column + 3] == 0:
                mov_grid[column + 3] = (abs(mov_grid[column + 3]) + abs(int(r/2))) * int(r/2)     
            elif grid[column + 6] == 0:
                mov_grid[column + 6] = (abs(mov_grid[column + 6]) + abs(int(r/2))) * int(r/2)

    left_diag = grid[0] + grid[4] + grid[8]
    if abs(left_diag) == 2:
        if grid[0] == 0:
            mov_grid[0] = (abs(mov_grid[0]) + abs(int(left_diag/2))) * int(left_diag/2)
        elif grid[4] == 0:
            mov_grid[4] = (abs(mov_grid[4]) + abs(int(left_diag/2))) * int(left_diag/2)
        elif grid[8] == 0:
            mov_grid[8] = (abs(mov_grid[8]) + abs(int(left_diag/2))) * int(left_diag/2)
    
    right_diag = grid[2] + grid[4] + grid[6]
    if abs(right_diag) == 2:
        if grid[2] == 0:
            mov_grid[2] = (abs(mov_grid[2]) + abs(int(right_diag/2))) * int(right_diag/2)
        elif grid[4] == 0:
            mov_grid[4] = (abs(mov_grid[4]) + abs(int(right_diag/2))) * int(right_diag/2)
        elif grid[6] == 0:
            mov_grid[6] = (abs(mov_grid[6]) + abs(int(right_diag/2))) * int(right_diag/2)

    if mov_grid.count(que) > 0 and mov_grid.count(-1*que) > 0:
        move = mov_grid.index(que)
    if mov_grid.count(que) > 0 and mov_grid.count(-1*que) == 0:
        move = mov_grid.index(que)
    if mov_grid.count(-1*que) > 0 and mov_grid.count(que) == 0:
        move = mov_grid.index(-1*que)
    
    if mov_grid.count(2) > 0:
        move = mov_grid.index(2)
    if mov_grid.count(-2) > 0:
        move = mov_grid.index(-2)


def new_game():
    global grid, new_grid, winner, que, draw, game_amount
    game_amount+=1
    print("Game №", game_amount, (" - X won" if winner == -1 else " - O won") if winner else "Draw", f"process of learning {game_amount/50000*100:.2f}%")

    que= -1
    draw = False
    winner = None
    grid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    


def data_save():
    global last_game
    for item in last_game:
        if draw is True:
            item.append(9)
        else:
            item.append(len(last_game))

    filename = "data.csv"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            nums = list(map(int, row))
            for item in last_game:
                if item == nums:
                    last_game.remove(item)
    file.close()

    with open(filename, "a", newline = "") as file:
        writer = csv.writer(file)
        for item in last_game:
            writer.writerow(item)
    file.close()
    last_game.clear()


def for_file():
    global grid, last_game, move
    if new_grid.count(0)<=8:
        new_grid.append((move + 1) * que)

        extra_grid = new_grid.copy()
        last_game.append(extra_grid)
        new_grid.pop()


while game_amount <= 50000:

    if winner is None:
        new_grid = grid.copy()
        check_next_move()
        if move is None:
            while True:

                move = random.randint(0, 8)
                if grid[move] == 0:
                    break

        grid[move] = que

        for_file()
        win_checker()
        que *= -1

    if (winner or draw):
        new_game()