from random import choice

import chess


class Engines:
    @staticmethod
    def getengines():
        return [x for x, y in Engines.__dict__.items() if type(y) == staticmethod and not x.startswith("get")]
    
    @staticmethod
    def getengine(engine):
        engine = engine.lower()
        if engine.startswith("get"):
            engine = ""
        return getattr(Engines, engine, Engines.random)

    @staticmethod
    def random(board: chess.Board):
        """Plays random moves."""
        return choice(list(board.legal_moves))

    @staticmethod
    def randomcheck(board: chess.Board):
        """Plays random moves, prioritizing checks."""
        check_moves = []
        for move in board.legal_moves:
            if board.gives_check(move):
                check_moves.append(move)
        return choice(list(check_moves if len(check_moves) > 0 else board.legal_moves))

    @staticmethod
    def randomcapture(board: chess.Board):
        """Plays random moves, prioritizing captures."""
        capture_moves = []
        for move in board.legal_moves:
            if board.is_capture(move):
                capture_moves.append(move)
        return choice(list(capture_moves if len(capture_moves) > 0 else board.legal_moves))

    @staticmethod
    def samepiece(board: chess.Board):
        """Tries to move the same piece from the last move, playing a random move."""
        same_moves = []
        if len(board.move_stack) >= 2:
            square = board.move_stack[-2].to_square
            for move in board.legal_moves:
                if move.from_square == square:
                    same_moves.append(move)
        print(same_moves)
        return choice(list(same_moves if len(same_moves) > 0 else board.legal_moves))

    @staticmethod
    def copy(board: chess.Board):
        """Tries to copy the opponents move."""
        if len(board.move_stack) >= 1:
            opponent_move = board.move_stack[-1]
            from_square = chess.square_mirror(opponent_move.from_square)
            to_square = chess.square_mirror(opponent_move.to_square)
            try:
                return board.find_move(from_square, to_square, opponent_move.promotion)
            except ValueError:
                pass
        return choice(list(board.legal_moves))

    @staticmethod
    def minimizeopponentmoves(board: chess.Board):
        """Play the move that minimizes opponents legal moves."""
        lowest = None
        lowest_moves = []
        for move in board.legal_moves:
            board.push(move)
            opponentmoves = len(list(board.legal_moves))
            if lowest is None or opponentmoves < lowest:
                lowest = opponentmoves
                lowest_moves = [move]
            elif opponentmoves == lowest:
                lowest_moves.append(move)
            board.pop()
        return choice(list(lowest_moves if len(lowest_moves) > 0 else board.legal_moves))

    @staticmethod
    def maximizeopponentmoves(board: chess.Board):
        """Play the move that maximizes opponents legal moves."""
        highest = None
        highest_moves = []
        for move in board.legal_moves:
            board.push(move)
            opponentmoves = len(list(board.legal_moves))
            if highest is None or opponentmoves > highest:
                highest = opponentmoves
                highest_moves = [move]
            elif opponentmoves == highest:
                highest_moves.append(move)
            board.pop()
        return choice(list(highest_moves if len(highest_moves) > 0 else board.legal_moves))

    @staticmethod
    def minimizeownmoves(board: chess.Board):
        """Play the move that minimize its own legal moves if it was its turn again."""
        lowest = None
        lowest_moves = []
        for move in board.legal_moves:
            board.push(move)
            board.turn = not board.turn
            opponentmoves = len(list(board.legal_moves))
            if lowest is None or opponentmoves < lowest:
                lowest = opponentmoves
                lowest_moves = [move]
            elif opponentmoves == lowest:
                lowest_moves.append(move)
            board.pop()
        return choice(list(lowest_moves if len(lowest_moves) > 0 else board.legal_moves))

    @staticmethod
    def maximizeownmoves(board: chess.Board):
        """Play the move that maximizes its own legal moves if it was its turn again."""
        highest = None
        highest_moves = []
        for move in board.legal_moves:
            board.push(move)
            board.turn = not board.turn
            opponentmoves = len(list(board.legal_moves))
            if highest is None or opponentmoves > highest:
                highest = opponentmoves
                highest_moves = [move]
            elif opponentmoves == highest:
                highest_moves.append(move)
            board.pop()
        return choice(list(highest_moves if len(highest_moves) > 0 else board.legal_moves))
