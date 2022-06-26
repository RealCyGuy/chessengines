import argparse
import sys
import chess

from engines import Engines


def talk(engine):
    board = chess.Board()

    while True:
        msg = input()
        newengine = command(msg, board, engine)
        if newengine:
            engine = newengine


def command(msg: str, board: chess.Board, engine):
    msg = msg.strip()
    tokens = [y for y in msg.split(" ") if y != ""]

    for i, token in enumerate(tokens):
        if token == "quit":
            sys.exit()

        if token == "uci":
            print(f"id name chessengines - {engine.__name__}: {engine.__doc__}")
            print("id author Cyrus Yip")
            printoptions()
            print("uciok")
            return

        if token == "isready":
            print("readyok")
            return

        if token == "position":
            if len(tokens[i:]) < 2:
                return

            if tokens[i + 1] == "startpos":
                board.reset()
                moves_start = 2
            elif tokens[i + 1] == "fen":
                fen = " ".join(tokens[2:8])
                board.set_fen(fen)
                moves_start = 8
            else:
                return

            if len(tokens[i:]) <= moves_start or tokens[i + moves_start] != "moves":
                return

            for move in tokens[(i + moves_start + 1) :]:
                board.push_uci(move)
            return

        if token == "d":
            print(board)
            print(board.fen())
            return

        if token == "go":
            print(f"bestmove {engine(board)}")
            return

        if token == "setoption":
            if len(tokens[i:]) < 5:
                return
            if tokens[i + 1] != "name" and tokens[i + 3] != "value":
                return
            if tokens[i + 2] == "Engine":
                print(f"set to {tokens[i + 4]}")
                return Engines.getengine(tokens[i + 4])
            return


def printoptions():
    print(
        f"option name Engine type combo default Random var {' var '.join([x[0].upper() + x[1:] for x in Engines.getengines()])}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", default="random", help="Choose an engine.")
    args = parser.parse_args()

    engine = Engines.getengine(args.engine)

    talk(engine)
