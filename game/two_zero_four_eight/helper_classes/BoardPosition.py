class BoardPosition:
    board = [[]]

    def is_end(self):
        return False

    def __str__(self):
        board_string = ''
        for row in self.board:
            for cell in row:
                board_string += cell + ' '
            board_string += '\n'

        return board_string
