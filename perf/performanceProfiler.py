import cProfile, pstats, io
from pstats import SortKey

with open("../simpleJava/simpleJava.py", "r") as f:
    src = f.read()

cProfile.run(src)