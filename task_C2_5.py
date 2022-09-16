import random


# Custom exception classes


class GameplayException(Exception):
    """ Exception class to catch inner game troubles """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"GameplayException has been raised. {self.message}."
        else:
            return "GameplayException has been raised."


class UserException(Exception):
    """ Exception class to catch troubles with user behavior """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"UserException has been raised. {self.message}."
        else:
            return "UserException has been raised."


class BoardOutException(UserException):
    """ Exception class to catch troubles with the dot goes out of board """

    def __str__(self):
        if self.message:
            return f"BoardOutException has been raised. {self.message}."
        else:
            return f"BoardOutException has been raised. You entered value beyond the board."


class IncorrectParametersException(UserException):

    def __str__(self):
        if self.message:
            return f"IncorrectParametersException has been raised. {self.message}."
        else:
            return f"IncorrectParametersException has been raised. You entered wrong value."


# Gameplay classes

class Dot:
    STATE_CHOICES = ["undamaged", "damaged", "missed", "hidden"]

    def __init__(self, column: int, row: int, state: str = "hidden"):
        self.column = column
        self.row = row
        self.state = state

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

    def __str__(self):
        return f"Dot with coordinates on board: column {self.column}, row {self.row}. Current state is: {self.state}."

    def get_coords(self) -> tuple:
        return self.column, self.row

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        if 1 <= value <= 6:
            self._column = value
        else:
            raise BoardOutException("Column value should be between 1 and 6")

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        if 1 <= value <= 6:
            self._row = value
        else:
            raise BoardOutException("Row value should be between 1 and 6")

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):

        def change_icon():
            if self.state == "undamaged":
                self.icon = "■"
            elif self.state == "damaged":
                self.icon = "X"
            elif self.state == "missed":
                self.icon = "T"
            else:
                self.icon = "O"

        if isinstance(value, str) and value in self.STATE_CHOICES:
            self._state = value
            change_icon()
        else:
            raise GameplayException("Incorrect state of dot")


class Ship:
    DIRECTION_CHOICES = ("horizontal", "vertical")

    def __init__(self, length: int, direction: str, start_point: Dot, health: int = None):
        self.length = length
        self.direction = direction
        self.start_point = start_point
        self.health = health

        self.dots_list = []

    def __str__(self):
        return f"Ship with {self.length} part(s), starts at {self.start_point.get_coords()}, currently has " \
               f"{self.health} health. Direction is {self.direction}"

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value: int):
        if isinstance(value, int) and 1 <= value <= 3:
            self._length = value
        else:
            raise IncorrectParametersException("Length should be from 1 to 3")

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value: str):
        if isinstance(value, str) and value in self.DIRECTION_CHOICES:
            self._direction = value
        else:
            raise IncorrectParametersException("Direction should be horizontal or vertical")

    @property
    def start_point(self):
        return self._start_point

    @start_point.setter
    def start_point(self, value: Dot):

        def check_start_point(dot_value):
            """
            Checks if all part of the ship can be placed on the board, prevents BoardOutException for each part of the
            ship
            """
            try:
                for i in range(self.length):
                    if self.direction == "horizontal":
                        Dot(dot_value.column + i, dot_value.row)
                    elif self.direction == "vertical":
                        Dot(dot_value.column, dot_value.row + i)
            except BoardOutException:
                raise BoardOutException("This ship can't be places on the board, change start point or length")

        if isinstance(value, Dot):
            check_start_point(value)
            self._start_point = value
        else:
            raise GameplayException("Start point must be class Dot instance")

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value is None:
            self._health = self.length
        else:
            self._health = value

    def get_dots(self) -> list:
        """ Returns the list of tuples with coordinates of each part of the ship. Tuple has format: (column, row). """

        coords_list = list()

        for i in range(self.length):
            if self.direction == "horizontal":
                coords_list.append((self.start_point.column + i, self.start_point.row))
            elif self.direction == "vertical":
                coords_list.append((self.start_point.column, self.start_point.row + i))

        return coords_list

    def reduce_health(self):
        if self.health > 0:
            self.health -= 1
        else:
            raise GameplayException("Health can't get negative value")


class Board:

    def __init__(self):
        self.board = []
        self.create_board()
        self.ships_list = []
        self.ship_length_list = [3, 2, 2, 1, 1, 1, 1]

    def create_board(self):
        """ Creates board with each dot as Dot class instance """
        _board = [list(range(1, 7))] + [list([i]) + [Dot(j, i) for j in range(1, 7)] for i in range(1, 7)]
        self.board = _board

    def print_board(self, hidden: bool = False):
        """ Prints board, gets hidden param as bool, if true, hides not damaged parts of the ship. """
        if hidden:
            print("\n   | ", end="")
            for i in self.board[0]:
                print(i, end=" | ")
            for i in self.board[1:]:
                print("\n", i[0], end=" | ")
                for j in i[1:]:
                    if j.state == "undamaged":
                        print("O", end=" | ")
                    else:
                        print(j.icon, end=" | ")
            print("\n")
        else:
            print("\n   | ", end="")
            for i in self.board[0]:
                print(i, end=" | ")
            for i in self.board[1:]:
                print("\n", i[0], end=" | ")
                for j in i[1:]:
                    print(j.icon, end=" | ")
            print("\n")

    def add_ship(self, new_ship: Ship):

        if isinstance(new_ship, Ship):

            occupied_dots = set()

            for ship in self.ships_list:
                for dot in ship.get_dots():
                    occupied_dots.add(dot)
                for dot in self.contour(ship):
                    occupied_dots.add(dot)

            for dot in new_ship.get_dots():
                if dot in occupied_dots:
                    raise IncorrectParametersException("You can't place ship here, must be at least 1 empty dot "
                                                       "between ships")

            if new_ship.length in self.ship_length_list:
                self.ship_length_list.remove(new_ship.length)
                self.ships_list.append(new_ship)
                for dot in new_ship.get_dots():
                    dot = self.board[dot[1]][dot[0]]
                    dot.state = "undamaged"
                    new_ship.dots_list.append(dot)
            else:
                raise IncorrectParametersException("You're trying to place more ships, than you can")
        else:
            raise GameplayException("Ship must be class Ship instance")

    @staticmethod
    def contour(ship: Ship) -> list:
        if isinstance(ship, Ship):
            contour_dot_list = set()
            for column, row in ship.get_dots():
                dot_list = set((column + i, row + j) for i in range(-1, 2) for j in range(-1, 2))
                contour_dot_list = contour_dot_list.union(dot_list)
            for coord in ship.get_dots():
                contour_dot_list.remove(coord)
            contour_dot_list = list(contour_dot_list)
            for column, row in contour_dot_list.copy():
                if not (1 <= column <= 6) or not (1 <= row <= 6):
                    contour_dot_list.remove((column, row))
            return contour_dot_list
        else:
            raise GameplayException("Ship must be class Ship instance")

    def shot(self, column: int, row: int) -> bool:
        """Shot function, returns True if shit is successful and False if missed"""
        if isinstance(column, int) and isinstance(row, int):
            if 1 <= column <= 6 and 1 <= row <= 6:
                if self.board[row][column].state == "undamaged":
                    self.board[row][column].state = "damaged"
                    for i in self.ships_list:
                        if (column, row) in i.get_dots():
                            i.reduce_health()
                            if i.health == 0:
                                for column, row in self.contour(i):
                                    self.board[row][column].state = "missed"
                                self.ships_list.remove(i)
                    return True
                elif self.board[row][column].state == "hidden":
                    self.board[row][column].state = "missed"
                    return False
                elif self.board[row][column].state == "damaged" or "missed":
                    raise IncorrectParametersException("You've already shot in this field")
                self.print_board()
            else:
                raise BoardOutException("You're trying to shoot outside the board. Choose the coords between 1 and 6")
        else:
            raise IncorrectParametersException("Column and row both should be integer")


class Player:

    def __init__(self, my_board: Board, enemy_board: Board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self) -> tuple:
        pass

    def move(self, player: str) -> bool:
        """ Function for each player's turn. Returns True if player can make turn one more time """
        try:
            choice: tuple = self.ask()
            shot_result = self.enemy_board.shot(*choice)
            if player == "user":
                print(f"\nYou hit dot with coordinates: column {choice[0]}, row {choice[1]}\n")
                print("Enemy's board:")
                self.enemy_board.print_board(True)
            elif player == "computer":
                print(f"\nComputer hit dot with coordinates: column {choice[0]}, row {choice[1]}\n")
                print("Your board:")
                self.enemy_board.print_board()
            else:
                raise GameplayException("Player can be user or computer")
        except BoardOutException as e:
            if player == "user":
                print(e)
                self.enemy_board.print_board()
            return self.move(player)
        except IncorrectParametersException as e:
            if player == "user":
                print(e)
                self.enemy_board.print_board()
            return self.move(player)
        else:
            if shot_result:
                return True
            else:
                return False


class User(Player):

    def ask(self) -> tuple:
        try:
            choice = tuple(map(int, input("Enter coordinates on enemy board: ").split()))
            if len(choice) != 2:
                raise IncorrectParametersException("Enter 2 coordinates with space between in format: column row")
            elif not (1 <= choice[0] <= 6) or not (1 <= choice[1] <= 6):
                raise BoardOutException("Both coordinates must be between 1 and 6")
        except ValueError:
            print("Enter valid numbers")
            return self.ask()
        except BoardOutException as e:
            print(e)
            return self.ask()
        except IncorrectParametersException as e:
            print(e)
            return self.ask()
        else:
            return choice


class AI(Player):

    def ask(self) -> tuple:
        choice = tuple(random.choices(list(range(1, 7)), k=2))
        return choice


class Game:

    def __init__(self):
        self.board_human = Board()
        self.board_ai = Board()
        self.player_human = User(my_board=self.board_human, enemy_board=self.board_ai)
        self.player_ai = AI(my_board=self.board_ai, enemy_board=self.board_human)

    @staticmethod
    def greet():
        example_ship = Ship(length=3, direction="horizontal", start_point=Dot(3, 2))
        example_board = Board()
        example_board.add_ship(example_ship)
        text1 = "\nWelcome to the Battleship game.\n\nYou're playing with the computer.\nFirst you need to put your " \
                "ships on the board, you can do it automatically or place them yourself. If you want to place them " \
                "by yourself, you need to enter length (amount of ship's part), direction (can be " \
                "\"horizontal\" and \"vertical\") and coordinates of the start point of the ship.\nTo enter " \
                "coordinates you need to enter column and row with space between, like: 4 3 (which means column " \
                "4 row 3).\nYou can have 1 ship with 3 parts, 2 ship with 2 parts and 4 ships with 1 part. Between " \
                "each ship must be space in 1 dot.\nThe direction goes from left to right if horizontal and from top " \
                "to bottom if vertical.\nHere's example of ship with length 3, horizontal direction and start point " \
                "at 3 2:"

        text2 = "After that you and computer take turns, trying to hit opponent's ship. To do that you also need to " \
                "enter coordinates on enemy board in the same way (column and row with space between).\nIf " \
                "your shot is successful, you can shoot one more time until you miss. The one, who sank all of " \
                "the opponent's ships, wins the game.\n\n"

        print(text1)
        example_board.print_board()
        print(text2)

    def random_board(self, player: str):
        """
        Generates random board for player. Can generate board for AI or User. Tries to add ship to board 900 times.
        If attempt is unsuccessful, generates a new board and tries again.
        """

        count = 0
        if player == "user":
            board = self.board_human
        elif player == "computer":
            board = self.board_ai
        else:
            raise GameplayException("Player can be user or computer")

        def inner_func():
            nonlocal count

            count += 1

            if count > 900:
                if player == "user":
                    self.board_human = Board()
                elif player == "computer":
                    self.board_ai = Board()
                else:
                    raise GameplayException("Player can be user or computer")

                self.random_board(player)()

            while board.ship_length_list:
                try:
                    ship_length = board.ship_length_list[0]
                    ship_direction = random.choice(("horizontal", "vertical"))
                    ship_start_point = Dot(random.randint(1, 6), random.randint(1, 6))

                    ship = Ship(length=ship_length, direction=ship_direction, start_point=ship_start_point)
                except BoardOutException:
                    inner_func()
                except IncorrectParametersException:
                    inner_func()
                else:
                    try:
                        board.add_ship(ship)
                    except BoardOutException:
                        inner_func()
                    except IncorrectParametersException:
                        inner_func()

        return inner_func

    def loop(self):
        while self.board_ai.ships_list and self.board_human.ships_list:
            human_move = self.player_human.move("user")
            while human_move:
                human_move = self.player_human.move("user")
                if not self.board_ai.ships_list or not self.board_human.ships_list:
                    return None
            if not self.board_ai.ships_list or not self.board_human.ships_list:
                return None
            ai_move = self.player_ai.move("computer")
            while ai_move:
                ai_move = self.player_ai.move("computer")
                if not self.board_ai.ships_list or not self.board_human.ships_list:
                    return None
            if not self.board_ai.ships_list or not self.board_human.ships_list:
                return None

    def set_ships_by_user(self):
        """Sets ships on the player's field. User choose position for each ship"""

        my_board = self.board_human

        print("\n\nHere is your board to place ship on:")
        my_board.print_board()

        while my_board.ship_length_list:

            def set_length() -> int:
                try:
                    length = int(input("Enter size of the ship: "))
                    if not (1 <= length <= 3):
                        raise ValueError("Enter number from 1 to 3")
                    if length not in my_board.ship_length_list:
                        print("You can't place that ship, choose other length")
                        return set_length()
                except ValueError:
                    print("You've entered wrong number. Enter number from 1 to 3")
                    return set_length()
                else:
                    return length

            def set_direction() -> str:
                try:
                    direction = input("Enter direction of the ship (horizontal or vertical): ")
                    if direction != "horizontal" and direction != "vertical":
                        raise ValueError("Direction isn't vertical or horizontal")
                except ValueError:
                    print("Choose direction between horizontal or vertical")
                    return set_direction()
                else:
                    return direction

            def set_start_point() -> tuple:
                try:
                    start_point = tuple(map(int, input("Enter coordinates for first part of the ship: ").split()))
                    if len(start_point) != 2:
                        raise IncorrectParametersException("Enter 2 coordinates with space between in format: "
                                                           "column row")
                    elif not (1 <= start_point[0] <= 6) or not (1 <= start_point[1] <= 6):
                        raise BoardOutException("Both coordinates must be between 1 and 6")
                except ValueError:
                    print("Enter valid numbers")
                    return set_start_point()
                except IncorrectParametersException as e:
                    print(e)
                    return set_start_point()
                except BoardOutException as e:
                    print(e)
                    return set_start_point()
                else:
                    return start_point

            try:
                ship_length = set_length()
                if ship_length == 1:
                    ship_direction = "horizontal"
                else:
                    ship_direction = set_direction()
                ship_start_point = Dot(*set_start_point())

                ship = Ship(length=ship_length, direction=ship_direction, start_point=ship_start_point)
            except BoardOutException as e:
                print(e)
                self.set_ships_by_user()
            except IncorrectParametersException as e:
                print(e)
                self.set_ships_by_user()
            else:
                try:
                    my_board.add_ship(ship)
                except BoardOutException as e:
                    print(e)
                    self.set_ships_by_user()
                except IncorrectParametersException as e:
                    print(e)
                    self.set_ships_by_user()
                else:
                    my_board.print_board()

    def set_ships(self):

        def generates_random_board():
            try:
                self.random_board("user")()
            except RecursionError:
                self.board_human = Board()
                generates_random_board()
            else:
                print("\nThis you automatically generated board:")
                self.board_human.print_board()

        try:
            choice = int(input("Enter 1 if you want to automatically generate board or 0 if you want to set ships by "
                               "your own: "))
        except ValueError:
            print("Enter 1 or 0")
            self.set_ships()
        else:
            if choice == 1:
                generates_random_board()
            elif choice == 0:
                self.set_ships_by_user()
            else:
                print("Enter 1 or 0")
                self.set_ships()

    def start(self):
        try:
            self.random_board("computer")()
        except RecursionError:
            self.board_ai = Board()
            self.start()
        else:
            Game.greet()
            self.set_ships()
            self.loop()
            if not self.board_ai.ships_list:
                print("You won!")
                return True
            elif not self.board_human.ships_list:
                print("Computer won!")
                return True


Game().start()
