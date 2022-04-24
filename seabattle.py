from random import randint, choice
import sys
import os

if sys.platform.startswith("win32"):
    os.system("color")
elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
    os.system("clear")

global colors
# resetall, green, yellow, lightyellow, lightgreen, 
# lightcyan, lightmagenta, lightred, red, magenta, lightgray 
colors = ["\033[0m", "\033[32m", "\033[33m", "\033[93m", "\033[92m", 
          "\033[96m", "\033[95m", "\033[91m", "\033[31m", "\033[35m", "\033[37m"]

"""
# список деяких стандартних кодів кольору для терміналів
# текст
resetall        = "\033[0m"  
default         = "\033[39m" 
black           = "\033[30m" 
red             = "\033[31m" 
green           = "\033[32m" 
yellow          = "\033[33m" 
blue            = "\033[34m" 
magenta         = "\033[35m" 
cyan            = "\033[36m" 
lightgray       = "\033[37m" 
darkgray        = "\033[90m" 
lightred        = "\033[91m" 
lightgreen      = "\033[92m" 
lightyellow     = "\033[93m" 
lightblue       = "\033[94m" 
lightmagenta    = "\033[95m" 
lightcyan       = "\033[96m" 
white           = "\033[97m" 

# тло
bgdefault      = "\033[49m"
bgblack        = "\033[40m"
bgred          = "\033[41m"
bggreen        = "\033[42m"
bgyellow       = "\033[43m"
bgblue         = "\033[44m"
bgmagenta      = "\033[45m"
bgcyan         = "\033[46m"
bglightgray    = "\033[47m"
bgdarkgray     = "\033[100m"
bglightred     = "\033[101m"
bglightgreen   = "\033[102m"
bglightyellow  = "\033[103m"
bglightblue    = "\033[104m"
bglightmagenta = "\033[105m"
bglightcyan    = "\033[106m"
bgwhite        = "\033[107m"
"""

def ascii_logo():
    '''Трішки ASCII-арту.'''
    print('''
                    __/___            
          _____/______|           
  _______/_____\_______\_____     
  \              < < <       |    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ''')

def print_board(board, size_board):
    '''Друкувати мапу.'''
    # варіант 1
    print(" ", end=" ")
    for c in range(size_board):
        print(c, end=" ")
    print()  
    r = 0    
    for row in board:
        print(r, " ".join(row))
        r += 1
    
    # варіант 2
    """
    print(" ", *[c for c in range(size_board)])
    r = 0    
    for row in board:
        print(r, *row)    
        r += 1
    """   

def map_ships(ships_board, coords, current_sign):
    '''Нанести на мапу позначки кораблів/навколо кораблів.'''
    for co in coords:
        x = co[0]
        y = co[1]
        ships_board[x][y] = current_sign
              
def free_cells_in_line_for_ship(line, sign_sea, sign_deck, sign_min_distance):
    '''Шукати координати вільних клітинок на довільній лінії мапи.'''
    positions = []
    k = 0
    current_pos = [False, False]
    for i in range(len(line)):
        if line[i] == sign_sea:
            k += 1 
            if current_pos[0] is False:    
                current_pos[0] = i
        elif (line[i] == sign_deck or line[i] == sign_min_distance) and k != 0:
            if current_pos[1] is False:    
                current_pos[1] = i - 1
                positions.append((current_pos[0], current_pos[1], k))
                k = 0
                current_pos = [False, False]
    if current_pos[0] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] and current_pos[1] is False:     
        positions.append((current_pos[0], i, k))       
    return positions
    
def place_for_current_ship(positions, name_current_ship, len_current_ship):
    '''Випадково обрати серед вільних клітинок лінії мапи 
       місця (координати) для поточного корабля.'''
    free_cells = positions[:]
    for t in positions:
        if t[0] == 0 and t[2] >= len_current_ship + 1:
            continue    
        if t[2] < len_current_ship + 2:
            free_cells.remove(t)
    if not free_cells:
        # print("Для корабля {} на цій лінії немає місця".format(name_current_ship))
        return False
    coords_cells = choice(free_cells)
    return coords_cells 
    
def ship_horizontal(place, row_ship, len_current_ship, size_board):
    '''Розташувати горизонтальні кораблі.'''
    increase = 0
    if place[0] != 0:
        increase += 1
    
    # згенерувати випадковий стовпець першої позиції корабля
    col = randint(place[0] + increase, place[1] - len_current_ship)
    
    # створити список значень стовпців-позицій корабля
    col_ship = list(range(col, col + len_current_ship))
    
    # сформувати координати палуб горизонтального корабля 
    coords = tuple(zip(row_ship * len_current_ship, col_ship))    
    
    # розрахувати координати клітинок моря навколо горизонтального корабля
    around_the_ship = []
    top = list(zip([row_ship[0] - 1] * (len_current_ship + 2), range(col - 1, col + len_current_ship + 2)))
    bottom = list(zip([row_ship[0] + 1] * (len_current_ship + 2), range(col - 1, col + len_current_ship + 2)))
    left = [(row_ship[0], col - 1)]
    right = [(row_ship[0], col + len_current_ship)]
    along = top + right + bottom + left
    for c in along:
        if (c[0] >= 0 and c[0] < size_board) and (c[1] >= 0 and c[1] < size_board):
            around_the_ship.append(c)   
    return coords, around_the_ship
    
def ship_vertical(place, col_ship, len_current_ship, size_board):
    '''Розташувати вертикальні кораблі.'''
    increase = 0
    if place[0] != 0:
        increase += 1
        
    # згенерувати випадковий рядок першої позиції корабля
    row = randint(place[0] + increase, place[1] - len_current_ship)
    
    # створити список значень рядків-позицій корабля
    row_ship = list(range(row, row + len_current_ship))
    
    # сформувати координати позицій вертикального корабля 
    coords = tuple(zip(row_ship, col_ship * len_current_ship))    
    
    # розрахувати координати клітинок моря навколо вертикального корабля
    around_the_ship = []
    top = [(row - 1, col_ship[0])]
    bottom = [(row_ship[-1] + 1, col_ship[0])]
    left = list(zip(range(row - 1, row + len_current_ship + 2), [col_ship[0] - 1] * (len_current_ship + 2)))
    right = list(zip(range(row - 1, row + len_current_ship + 2), [col_ship[0] + 1] * (len_current_ship + 2)))
    along = top + right + bottom + left
    for c in along:
        if (c[0] >= 0 and c[0] < size_board) and (c[1] >= 0 and c[1] < size_board):
            around_the_ship.append(c)
    return coords, around_the_ship       

def get_random_line_board(direction, size_board, ships_board, name_current_ship, len_current_ship, sign_sea, sign_deck, sign_min_distance):
    '''Отримати випадкову (вертикальну чи горизонтальну) лінію мапи.'''
    limit = 0
    line_numbers = [i for i in range(size_board)]   
    while True:
        line_ship = [choice(line_numbers)]
        line_numbers.remove(line_ship[0])
        if direction == 0:
            line = ships_board[line_ship[0]]
        else:
            line = [ships_board[i][j] for i in range(size_board) for j in range(size_board) if j == line_ship[0]] 
        
        positions = free_cells_in_line_for_ship(line, sign_sea, sign_deck, sign_min_distance)
        place = place_for_current_ship(positions, name_current_ship, len_current_ship)
        if place or size_board - 1 == limit:
            break
        limit += 1    
    
    if limit == size_board or not place:
        # print("На усіх лініях відсутня можливість розмістити корабель {}".format(name_current_ship))
        return False, False
    return place, line_ship
    
def build_ship(len_current_ship, size_board, name_current_ship, ships_board, sign_sea, sign_deck, sign_min_distance):
    '''Побудовати корабель.'''
    # згенерувати положення корабля - 0 (горизонтальне) чи 1 (вертикальне)
    direction = randint(0, 1)
    
    place, line_ship = get_random_line_board(direction, size_board, ships_board, name_current_ship, len_current_ship, sign_sea, sign_deck, sign_min_distance)
    
    # якщо корабель не можна розмістити, то вмикається непередбачувана ситуація на морі
    if not place and not line_ship:
        return False, False
    
    # сформувати координати горизонтальних і вертикальних кораблів    
    if direction == 0:
        coords = ship_horizontal(place, line_ship, len_current_ship, size_board)
    else:
        coords = ship_vertical(place, line_ship, len_current_ship, size_board) 
    return list(coords[0]), coords[1]

def to_place_ships(navy, navy_ships_from_l_to_s, size_board, ships_board, sign_sea, sign_deck, sign_min_distance, score):
    '''Розмістити на мапі позначки кораблів, просторів навколо. Позначки приховані.'''
    try:
        for current_ship in navy_ships_from_l_to_s:
            name_current_ship = current_ship[:-2]
            amount_current_ship = int(current_ship[-2])
            len_current_ship = int(current_ship[-1])
            for n in range(amount_current_ship):
                design = build_ship(len_current_ship, size_board, name_current_ship, ships_board, sign_sea, sign_deck, sign_min_distance)
                ship, around = design[0], design[1]
                if ship and around:
                    navy[current_ship] += ship
                    # нанести на мапу позначки кораблів
                    map_ships(ships_board, ship, sign_deck)           
                    # нанести на мапу позначки навколо кораблів
                    map_ships(ships_board, around, sign_min_distance) 
                else:
                    print(noncombat_losses_messages(name_current_ship))
                    update_score = score[current_ship]
                    score[current_ship] = update_score[:-int(current_ship[-1])]
        return True, navy
    except Exception as e:
        print(e)
        return False,       
       
def noncombat_losses_messages(name_current_ship):
    '''Непередбачувана ситуація в морі.
       Дркувати випадкове повідомлення.'''
    start_message = "\n{}Розвідка повідомляє: {}".format(colors[10], colors[0])
    end_message = ["Хм, буває ж таке.", "Ваш бойовий дух зміцнів!", "Ваша мотивація зросла в рази!"]        
    message = ["корабель {}{}{} зник з екрану радара. Є думка, що попрацювала українська окрема тракторна бригада. {}", 
               "корабель {}{}{} випадково підірвався на морській міні часів Другої світової війни. {}",
               "корабель {}{}{} поспіхом накивав п'ятами з поля бою. {}"]        
    return start_message + choice(message).format(colors[2], name_current_ship.upper(), colors[0], choice(end_message))

def intro_game(rockets):
    '''Друкувати вітальне повідомлення і правила.'''
    print("{}Гра \"Морський бій\"".format(colors[5]))
    ascii_logo()
    print("Слава Україні! Запрошуємо Вас до морської битви!")
    neptun_message = "У вас в наявності {}{}{}{}{} протикорабельних крилатих ракет Нептун."
    print(neptun_message.format(colors[0], colors[3], rockets, colors[0], colors[5]))
    print("Ваше завдання: знайти і знешкодити кораблі, які заховані на мапі.")
    input_message = "Введіть координати у форматі {}{}рядок стовпець{}{} через пропуск."
    print(input_message.format(colors[0], colors[4], colors[0], colors[5]))
    print("Значення координат додатні, точка у лівому верхньому куті має координати (0, 0).", colors[0]) 

def user_guess():
    '''Ввести користувачем координати цілі''' 
    instruction = "\nВведіть координати через пропуск або {}q{} для виходу з гри: "
    while True:
        try:
            data = input(instruction.format(colors[4], colors[0])).split()
            if 'q' in data[0].lower() and len(data[0]) == 1 and len(data) == 1:
                return 'q'
            guess_row, guess_col = int(data[0]), int(data[1])
            return guess_row, guess_col
        except:
            print("\n{}Некоректні координати.{}".format(colors[10], colors[0]))

def ship_is_destroyed(score, name_ship):
    '''Корабель цілком знищено?'''
    decks = int(name_ship[-1])
    len_ship_numbering = len(score[name_ship])
    d = []
    # step - крок розділення кораблів одного типу
    step = 0 
    # k = 1 - корабель цілком знищено, k = 0 - ні
    k = 0    
    for i in range(len_ship_numbering // decks): 
        s = sum(score[name_ship][step:decks + step])
        if s == 0:
            score[name_ship][step:decks + step] = [-1] * decks
            k = 1
            d.append(k) 
            k = 0    
        step += decks
    return sum(d)    
    
def update_board(guess, sea_board, size_board, hits, guesses, sign_goal, sign_failure):
    '''Оновити мапу.'''
    guess_row = guess[0]
    guess_col = guess[1]
        
    if guess in guesses:
        print("{}\nВи вже у цю точку вціляли.{}".format(colors[2], colors[0]))
        return sea_board
    
    if (guess_row < 0 or guess_row > size_board - 1) or (guess_col < 0 or guess_col > size_board - 1):
        print("{}\nОй, це десь на суші.{}".format(colors[9], colors[0]))    
        return sea_board
    
    guesses.append(guess)
    if guess in hits:
        print("{}Успіх! Ви влучили в корабель!{}".format(colors[8], colors[0]))
        sea_board[guess_row][guess_col] = "{}{}{}".format(colors[7], sign_goal, colors[0])
        # видалити значення координат корабля при влученні
        hits.remove(guess)
        return sea_board
        
    print("{}Повз цілі!{}".format(colors[1], colors[0]))
    sea_board[guess_row][guess_col] = "{}{}{}".format(colors[4], sign_failure, colors[0])
    return sea_board

def update_flotilla(guess, flotilla, score):
    '''Оновити флотилію.'''
    for name_ship in sorted(flotilla.keys(), key=lambda x: x[-1], reverse=True):  
        coords_ship = flotilla[name_ship]
        if guess in coords_ship:
            # отримати індекс введених координат в списку координат флотилії
            idx = coords_ship.index(guess) 
            # у флотилії на місце ідексу координат попадання вставити від'ємні значення (0 залишається нулем)
            coords_ship[idx] = (-guess[0], -guess[1]) 
            # обнулення позиції в обліку кораблів     
            score[name_ship][idx] = 0 
            return score, name_ship
    return False

def enemy_ships(sea_board, hits, sign_deck):
    '''Показати вцілілі кораблі на мапі.'''
    for coord in hits:
        x = coord[0]
        y = coord[1]
        sea_board[x][y] = "{}{}{}".format(colors[3], sign_deck, colors[0])
    return sea_board

def intelligence(sea_board, hits, size_board, sign_deck):
    '''Показати мапу з результатами.'''
    print_board(enemy_ships(sea_board, hits, sign_deck), size_board)

def number_ships(flotilla):
    '''Порахувати кількість усіх кораблів.'''
    n = 0
    for name_ship in flotilla:
        decks = int(name_ship[-1])
        n += len(flotilla[name_ship]) // decks
    return n

def hitting_ships(score):
    '''Розрахувати кількість набраних очок.'''
    quantity = 0
    for name_ship in score:
        quantity += sum([abs(i) for i in score[name_ship] if i == -1])    
    return quantity
    
def max_hitting_ships(score):
    '''Розрахувати максимальну кількість очок.'''
    max_quantity = 0
    for name_ship in score:
        max_quantity += len(score[name_ship])
    return max_quantity

def gamewords_endings(n, k):
    '''Сформувати закінчення слів за еквівалентом числа.'''
    ships_words = ["кораблів", "кораблі", "корабель"]
    rockets_words = ["ракет", "ракети", "ракета"]
    current_words = rockets_words
    if k == "s":
        current_words = ships_words
    if n % 100 in (11, 12, 13, 14) or n % 10 in (5, 6, 7, 8, 9, 0): 
        return current_words[0]
    elif n % 10 in (2, 3, 4): 
        return current_words[1]
    else: 
        return current_words[2]
 
def main():
    '''Головна програма.'''
    sign_sea = "."          # море
    sign_deck = "O"         # палуби кораблів
    sign_min_distance = "+" # навколо кораблів
    sign_failure = "#"      # невдачі
    sign_goal = "X"         # влучання 
    size_board = 10         # розміри мапи, за замовчуванням 10х10
    guesses = []            # список кортежів координат цілей, які вводить користувач
    hits = []               # список кортежів координат усіх кораблів
    rockets = 30            # кількість ракет Нептун
    starting = 0            # кількість запусків ракет
    success = 0             # кількість кораблів, знищених цілком
    
    # сформувати мапу з морем
    sea_board = [[sign_sea for col in range(size_board)] for row in range(size_board)]

    # сформувати мапу для кораблів 
    ships_board = [[sign_sea for col in range(size_board)] for row in range(size_board)]
        
    # ініціювати флотилію, словник у форматі {НазваКількістьПалубність: список кортежів координат палуб}
    navy = {"battleship14": [], "cruiser23": [], "destroyer32": [], "patrolboat41": []}

    # ініціювати облік кораблів 
    score = {"battleship14": [1, 1, 1, 1], "cruiser23": [1, 1, 1, 2, 2, 2], "destroyer32": [1, 1, 2, 2, 3, 3], "patrolboat41": [1, 2, 3, 4]}
    
    # створити список назв кораблів від найдовшого до найкоротшого
    navy_ships_from_l_to_s = sorted(navy.keys(), key=lambda x: x[-1], reverse=True)
    
    # розпочати з вітального повідомлення і правил
    intro_game(rockets)

    # розмістити кораблі флоту на мапі
    start = to_place_ships(navy, navy_ships_from_l_to_s, size_board, ships_board, sign_sea, sign_deck, sign_min_distance, score)    
    
    # розвідка: показати мапу кораблів
    # print_board(ships_board, size_board)
    
    if start[0]:
        flotilla = start[1]
    
        # зібрати кортежі координат розміщення кораблів на мапі
        for name_ship, coords_ship in flotilla.items():
            for co in coords_ship:
                hits.append(co)    
        
        # обчислити кількість кораблів на мапі на початок битви
        all_ships = number_ships(flotilla)        
        
        while True:
            # друкувати поточну ситуацію на мапі
            print_board(sea_board, size_board)
            
            # ввести користувачем координати
            guess_xy = user_guess()
            if guess_xy == 'q': # достроково завершити гру
                break
            
            # перевірити чи відбулося влучення
            sea_board = update_board(guess_xy, sea_board, size_board, hits, guesses, sign_goal, sign_failure)
            
            # оновити дані про флотилію
            upd_flot = update_flotilla(guess_xy, flotilla, score)
            if upd_flot:
                score, name_ship = upd_flot
                destroyed = ship_is_destroyed(score, name_ship)
                if destroyed:
                    for i in range(destroyed):
                        success += 1
                        victory = "Ви потопили {}{}{}-палубний {}{}{}. Так тримати!"
                        print(victory.format(colors[2], name_ship[-1], colors[0], colors[2], name_ship[:-2].upper(), colors[0]))
            
            # друкувати статистику по кораблям і ракетам
            starting += 1        
            n = rockets - starting
            stat_message = "Залишилося: [{} {} {}] {}, [{} {} {}] {}"
            print(stat_message.format(colors[3], all_ships - success, colors[0], gamewords_endings(all_ships - success, "s"), colors[6], n, colors[0], gamewords_endings(n, "r")))  
            
            # умови завершення гри: ракети закінчилися і деякі кораблі не потоплені
            # або усі кораблі знищені 
            if n == 0 or not hits:
                break
        
        # розрахувати кількість набраних балів і друкувати результати гри
        max_points = max_hitting_ships(score)
        points = hitting_ships(score)
        print("\n{}Результати гри:{}".format(colors[1], colors[0]))
        row_points = "Ви набрали очок: {}{}{} із {}{}{}-ти."
        print(row_points.format(colors[5], points, colors[0], colors[5], max_points, colors[0]))   
        
        # друкувати повідомлення про успішне завершення гри
        # або координати точок вцілілих кораблів чи їх частин
        if not hits:
            total_victory = "{}Перемога! Ви повністю потопили флотилію ворога!{}"
            print(total_victory.format(colors[4], colors[0]))
        else:
            partial = "Координати кораблів, в які ви не поцілили: {}{}{}"
            print(partial.format(colors[2], str(hits).strip("[]"), colors[0]))
            
        # продемонструвати мапу з результатами гри
        print()
        intelligence(sea_board, hits, size_board, sign_deck)  
        print("\n{}Кінець гри.{}".format(colors[6], colors[0]))
        return
    else:
        print("\n{}Несподівана помилка.{}".format(colors[10], colors[0]))

main()
