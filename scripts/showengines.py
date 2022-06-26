import inspect

from engines import Engines

lines = []
for x, y in Engines.__dict__.items():
    if type(y) == staticmethod and not x.startswith("get"):
        f = getattr(Engines, x)
        sourcelines = inspect.getsourcelines(f)
        lines.append(
            f"[`{x}`](https://github.com/RealCyGuy/chessengines/blob/main/engines.py#L{sourcelines[1]}-{len(sourcelines[0]) + sourcelines[1]}): {f.__doc__}"
        )

print("  \n".join(lines))
