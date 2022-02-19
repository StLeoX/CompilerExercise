# sql backend

from core.cfg import ContextFreeGrammar
from core.typeDef import TypeDefinition
from core.action import Action
from core.goto import Goto
from core.parseTree import ParseTreeActionRegister
from core import scanner
from core import parser

typedef = TypeDefinition.load("typedef")
cfg = ContextFreeGrammar.load(typedef, "sqlCFG")
action, goto = parser.genActionGoto(typedef, cfg)

tokenList = scanner.parse(typedef, input())
pt = parser.parse(tokenList, typedef, cfg, action, goto)
print(pt)
