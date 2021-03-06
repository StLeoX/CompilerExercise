# calc backend

from core.cfg import ContextFreeGrammar
from core.typeDef import TypeDefinition
from core.action import Action
from core.goto import Goto
from core.parseTree import ParseTreeActionRegister
from core import scanner
from core import parser

global d
d = {}

typedef = TypeDefinition.load("typedef")
cfg = ContextFreeGrammar.load(typedef, "CFG4")
# action, goto = Parser.genActionGoto(typedef, cfg)
# action.save('simpleCalc/calc_action')
# goto.save('simpleCalc/calc_goto')
# exit()
ar = ParseTreeActionRegister(cfg)


@ar.production('Statement -> E', 'Statement -> Assignment')
def __stmt(stmt, _):
    print(_.val)


@ar.production('E -> E + T')
def __e0(e, e1, _, t):
    e.val = e1.val + t.val


@ar.production('E -> E - T')
def __e1(e, e1, _, t):
    e.val = e1.val - t.val


@ar.production('E -> T', 'T -> F', 'F -> G')
def __e2(a, b):
    a.val = b.val


@ar.production('T -> T * F')
def __t0(t, t1, _, f):
    t.val = t1.val * f.val


@ar.production('T -> T / F')
def __t1(t, t1, _, f):
    if t1.val % f.val:
        t.val = t1.val / f.val
    else:
        t.val = t1.val // f.val


@ar.production('T -> T % F')
def __t2(t, t1, _, f):
    t.val = t1.val % f.val


@ar.production('F -> F ** G')
def __f0(f, f1, _, g):
    f.val = f1.val ** g.val


@ar.production('G -> ( E )')
def __g0(g, leftPar, e, rightPar):
    g.val = e.val


@ar.production('G -> int_const')
def __g1(g, int_const):
    g.val = int(int_const.getContent())


@ar.production('G -> id')
def __g2(g, id_):
    global d
    g.val = d[id_.getContent()]


@ar.production('Assignment -> id = E')
def __assign(assi, id_, _, E):
    d[id_.getContent()] = E.val
    assi.val = d[id_.getContent()]


if __name__ == '__main__':
    action = Action.load(cfg, "calc_action")
    goto = Goto.load(cfg, "calc_goto")

    while True:
        try:
            inputString = input(">>> ")
            tokenList = scanner.parse(typedef, inputString)
            pt = parser.parse(tokenList, typedef, cfg, action, goto)
            pt.evaluate(ar)

        except EOFError:
            break
