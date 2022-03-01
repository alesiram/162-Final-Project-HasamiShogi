# Marisela Vasquez
# Date: 11/18/21
# Description: Hasami Shogi Game

class HasamiShogiGame:
    """Hasami Shogi Game"""
    def __init__(self):
        """Initializes the private data members"""
        self._active_player = "BLACK"
        self._game_state = "UNFINISHED"
        self._num_red_captured = 0
        self._num_black_captured = 0
        # create empty board, then set starting positions
        self._board = [["NONE"] * 9 for i in range(9)]
        self._board[0] = ["RED"] * 9
        self._board[8] = ["BLACK"] * 9

    def print_board(self):
        """Prints the board"""
        print("   1  2  3  4  5  6  7  8  9")
        y_axis = "a"
        for list in self._board:
            print(y_axis + " ", end=" ")
            for player in list:
                player_to_print = "E"
                if player == "RED":
                    player_to_print = "R"
                if player == "BLACK":
                    player_to_print = "B"
                if player == "NONE":
                    player_to_print = "."
                print(player_to_print + " ", end=" ")
            print("\n")
            # bump y_axis to next letter
            y_axis = chr(ord(y_axis) + 1)

    def get_num_captured_pieces(self, player):
        """Returns the number of captured pieces"""
        if player == "BLACK":
            return self._num_black_captured
        if player == "RED":
            return self._num_red_captured

    def capture_pieces(self):
        """Captures pieces"""
        if self._active_player == "BLACK":
            self._num_red_captured = self._num_red_captured + 1
        else:
            self._num_black_captured = self._num_black_captured + 1

    def check_game_over(self):
        """Checks if the game is over"""
        if self._num_red_captured >= 8:
            self._game_state = 'BLACK_WON'
        if self._num_black_captured >= 8:
            self._game_state = 'RED_WON'

    def get_game_state(self):
        """Returns game state"""
        return self._game_state

    def get_active_player(self):
        """Returns active player"""
        return self._active_player

    def switch_active_player(self):
        """Switches active player"""
        if self._active_player == "BLACK":
            self._active_player = "RED"
        else:
            self._active_player = "BLACK"

    def get_enemy_player(self):
        """Gets enemy player"""
        if self._active_player == "BLACK":
            return "RED"
        else:
            return "BLACK"

    def get_square_occupant(self, square):
        """Gets player position"""
        index_y_x = self.convert_move_to_index_values(square)
        player_at_pos = self._board[index_y_x[0]][index_y_x[1]]
        return player_at_pos

    def convert_move_to_index_values(self, move):
        """Returns index position"""
        y_axis = self.convert_char_to_index(move[0])
        x_axis = int(move[1]) - 1
        return (y_axis, x_axis)

    def check_if_axis_move_is_valid(self, start, end):
        """Takes a start and end position
        Returns True if a move vertical or horizontal, False otherwise"""
        start_y = start[0]
        end_y = end[0]
        start_x = start[1]
        end_x = end[1]

        return (start_y == end_y) or (start_x == end_x)

    def convert_char_to_index(self, char):
        """Takes a y-axis char and returns the corresponding index value
        For example: a -> 0, ..., i -> 8"""

        return ord(char) % 97

    def make_move(self, start, end):
        """Makes move, returns True if possible, False if not possible"""
        # Start position must have a piece owned by active player
        if self._active_player != self.get_square_occupant(start):
            return False
        # Move must be on x or y axis only
        if self.check_if_axis_move_is_valid(start, end) == False:
            return False
        # Game must not be won already
        if self._game_state != "UNFINISHED":
            return False
        # End move position must be empty
        if self.get_square_occupant(end) != "NONE":
            return False
        # Start move position must not be empty
        if self.get_square_occupant(start) == "NONE":
            return False

        # Make the move
        start_position = self.convert_move_to_index_values(start)
        end_position = self.convert_move_to_index_values(end)
        self._board[end_position[0]][end_position[1]] = self._active_player
        self._board[start_position[0]][start_position[1]] = "NONE"
        self.capture_x_axis(end_position)
        self.capture_y_axis(end_position)
        self.capture_corner(end_position)
        self.check_game_over()
        self.switch_active_player()
        return True

    def capture_x_axis(self, end_position):
        """Check if there are any players that can be captured on x-axis"""
        # Check if there are other pieces of currently active player on x-axis
        can_capture_left = False
        can_capture_right = False

        left_capture_partner = end_position[1] - 1
        while (can_capture_left == False) and (left_capture_partner >= 0):
            if self._board[end_position[0]][left_capture_partner] == self._active_player:
                if end_position[1] - left_capture_partner == 1:
                    can_capture_left = False
                    break
                else:
                    can_capture_left = True
                    break
            elif self._board[end_position[0]][left_capture_partner] == "NONE":
                # if square is empty then no way we can sandwich pieces to capture
                can_capture_left = False
                break
            else:
                left_capture_partner = left_capture_partner - 1

        right_capture_partner = end_position[1] + 1
        while (can_capture_right == False) and (right_capture_partner <= 8):
            if self._board[end_position[0]][right_capture_partner] == self._active_player:
                if right_capture_partner - end_position[1] == 1:
                    can_capture_right = False
                    break
                else:
                    can_capture_right = True
                    break
            elif self._board[end_position[0]][right_capture_partner] == "NONE":
                # if square is empty then no way we can sandwich pieces to capture
                can_capture_right = False
                break
            else:
                right_capture_partner = right_capture_partner + 1

        if can_capture_right == True:
            for square in range(end_position[1] + 1, right_capture_partner):
                self._board[end_position[0]][square] = "NONE"
                self.capture_pieces()

        if can_capture_left == True:
            for square in range(left_capture_partner + 1, end_position[1]):
                self._board[end_position[0]][square] = "NONE"
                self.capture_pieces()

    def capture_y_axis(self, end_position):
        """Check if there are any players that can be captured on y-axis"""
        # Check if there are other pieces of currently active player on y-axis
        can_capture_up = False
        can_capture_down = False

        up_capture_partner = end_position[0] - 1
        while (can_capture_up == False) and (up_capture_partner >= 0):
            if self._board[up_capture_partner][end_position[1]] == self._active_player:
                if end_position[0] - up_capture_partner == 1:
                    can_capture_up = False
                    break
                else:
                    can_capture_up = True
                    break
            elif self._board[up_capture_partner][end_position[1]] == "NONE":
                # if square is empty then no way we can sandwich pieces to capture
                can_capture_up = False
                break
            else:
                up_capture_partner = up_capture_partner - 1

        down_capture_partner = end_position[0] + 1
        while (can_capture_down == False) and (down_capture_partner <= 8):
            if self._board[down_capture_partner][end_position[1]] == self._active_player:
                if down_capture_partner - end_position[0] == 1:
                    can_capture_down = False
                    break
                else:
                    can_capture_down = True
                    break
            elif self._board[down_capture_partner][end_position[1]] == "NONE":
                # if square is empty then no way we can sandwich pieces to capture
                can_capture_down = False
                break
            else:
                down_capture_partner = down_capture_partner + 1

        if can_capture_down == True:
            for square in range(end_position[0] + 1, down_capture_partner):
                self._board[square][end_position[1]] = "NONE"
                self.capture_pieces()

        if can_capture_up == True:
            for square in range(up_capture_partner + 1, end_position[0]):
                self._board[square][end_position[1]] = "NONE"
                self.capture_pieces()

    def capture_corner(self, end_position):
        """Checks if any corner pieces can be captured"""
        # capture bottom left
        if end_position[0] == 7 or end_position[0] == 8:
            if end_position[1] == 0 or end_position[1] == 1:
                if (self._board[8][1] == self._active_player and
                        self._board[7][0] == self._active_player and
                        self._board[8][0] == self.get_enemy_player()):
                    self._board[8][0] = "NONE"
                    self.capture_pieces()

        # capture bottom right
        if end_position[0] == 7 or end_position[0] == 8:
            if end_position[1] == 7 or end_position[1] == 8:
                if (self._board[8][7] == self._active_player and
                        self._board[7][8] == self._active_player and
                        self._board[8][8] == self.get_enemy_player()):
                    self._board[8][8] = "NONE"
                    self.capture_pieces()

        # capture top left
        if end_position[0] == 0 or end_position[0] == 1:
            if end_position[1] == 0 or end_position[1] == 1:
                if (self._board[0][1] == self._active_player and
                        self._board[1][0] == self._active_player and
                        self._board[0][0] == self.get_enemy_player()):
                    self._board[0][0] = "NONE"
                    self.capture_pieces()

        # capture top right
        if end_position[0] == 0 or end_position[0] == 1:
            if end_position[1] == 7 or end_position[1] == 8:
                if (self._board[0][7] == self._active_player and
                        self._board[1][8] == self._active_player and
                        self._board[0][8] == self.get_enemy_player()):
                    self._board[0][8] = "NONE"
                    self.capture_pieces()
#
# game = HasamiShogiGame()
# game.print_board()
# print("PLAYER TYPE: ", game.get_square_occupant("i3"))
# print("Move 1 Valid? :", game.make_move("i2", "c2"))
# print("Move 2 Valid? :", game.make_move("a3", "c3"))
# print("Move 3 Valid? :", game.make_move("i9", "d9"))
# print("Move 4 Valid? :", game.make_move("a6", "c6"))
# print("Move 5 Valid? :", game.make_move("i4", "d4"))
# print("Move 6 Valid? :", game.make_move("a5", "c5"))
# print("Move 7 Valid? :", game.make_move("i7", "c7"))
# print("Move 8 Valid? :", game.make_move("a9", "b9"))
# game.print_board()
# print("Move 9 Valid? :", game.make_move("d4", "c4"))
# game.print_board()
# print("Move 10 Valid? :", game.make_move("a8", "e8"))
# print("Move 10 Valid? :", game.make_move("c7", "c9"))
# game.print_board()
# print("Move 10 Valid? :", game.make_move("i8", "f8"))
# print("Move 12 Valid? :", game.make_move("a7", "g7"))
# print("Move 10 Valid? :", game.make_move("i8", "f8"))
# print("Move 13 Valid? :", game.make_move("f8", "f9"))
# print("Move 13 Valid? :", game.make_move("g7", "g9"))
# print("Move 13 Valid? :", game.make_move("f8", "f9"))
# print("Move 10 Valid? :", game.make_move("e8", "e9"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 10 Valid? :", game.make_move("c2", "c3"))
# print("Move 10 Valid? :", game.make_move("a2", "i2"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 15 Valid? :", game.make_move("i6", "i9"))
# print("Move 15 Valid? :", game.make_move("a1", "h1"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 15 Valid? :", game.make_move("i5", "a5"))
# print("Move 15 Valid? :", game.make_move("g9", "h9"))
# print("Move 15 Valid? :", game.make_move("a5", "a9"))
# print("Move 15 Valid? :", game.make_move("h1", "h8"))
# print("Move 15 Valid? :", game.make_move("c3", "a3"))
# game.print_board()
# print("Move 15 Valid? :", game.make_move("h8", "i8"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 15 Valid? :", game.make_move("c4", "c8"))
# print("Move 15 Valid? :", game.make_move("e9", "e1"))
# game.print_board()
# print("Move 15 Valid? :", game.make_move("c8", "c7"))
# print("Move 15 Valid? :", game.make_move("i8", "a8"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 15 Valid? :", game.make_move("a3", "a1"))
# print("Move 15 Valid? :", game.make_move("e1", "b1"))
# print("Move 15 Valid? :", game.make_move("c7", "c9"))
# game.print_board()
# print("Move 15 Valid? :", game.make_move("a4", "a2"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("Move 15 Valid? :", game.make_move("i3", "a3"))
# print("Move 15 Valid? :", game.make_move("a8", "a4"))
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# game.print_board()
# print("get_num_captured_pieces BLACK", game.get_num_captured_pieces("BLACK"))
# print("get_num_captured_pieces RED", game.get_num_captured_pieces("RED"))
# print("game.get_active_player()", game.get_active_player())
# print("game.get_square_occupant('a4')", game.get_square_occupant('a4'))
# print("game.get_square_occupant('a7')", game.get_square_occupant('a7'))
# print("game.get_game_state()", game.get_game_state())
# print("Move 15 Valid? :", game.make_move("a4", "a2"))


