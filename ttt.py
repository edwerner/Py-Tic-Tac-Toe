#!/usr/bin/env python

import random


class ttt(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ("X wins", "Draw", "O wins")

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def print_board(self):
        for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
            print(element)
        print("-----------------")

    def available_squares(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]
        return False

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def game_over(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True

    def move(self, node, player, alpha, beta):
        if node.game_over():
            if self.winner() == 'X':
                return -1
            elif self.game_over() == True and self.winner() is None:
                return 0
            elif self.winner() == 'O':
                return 1
        for move in node.available_squares():
            node.make_move(move, player)
            val = self.alphabeta(node, get_opponent(player), alpha, beta)
            node.make_move(move, None)

    def alphabeta(self, node, player, alpha, beta):
        if node.game_over():
            if self.winner() == 'X':
                return -1
            elif self.game_over() == True and self.winner() is None:
                return 0
            elif self.winner() == 'O':
                return 1
        for move in node.available_squares():
            node.make_move(move, player)
            val = self.alphabeta(node, get_opponent(player), alpha, beta)
            self.print_board()
            node.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_squares()) == 9:
        return 4
    for move in board.available_squares():
        board.make_move(move, player)
        val = board.alphabeta(board, get_opponent(player), -2, 2)
        board.make_move(move, None)
        print("********* FINAL MOVE *************")
        print("move:", move + 1, "effect:", board.winners[val + 1])
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_opponent(player):
    if player == 'X':
        return 'O'
    return 'X'

if __name__ == "__main__":
    board = ttt()
    board.print_board()

    while not board.game_over():
        player = 'X'
        player_move = int(input("Next Move: ")) - 1
        if not player_move in board.available_squares():
            continue
        board.make_move(player_move, player)
        board.print_board()

        if board.game_over():
            break
        player = get_opponent(player)
        computer_move = determine(board, player)
        board.make_move(computer_move, player)
        board.print_board()
    print("winner is", board.winner())