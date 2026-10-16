class Sentence:
    def evaluate(self, model):
        raise NotImplementedError
    def formula(self):
        raise NotImplementedError
    def symbols(self):
        raise NotImplementedError
    
class Symbol(Sentence):
    def __init__(self, name):
        self.name = name
    def evaluate(self, model):
        return model.get(self.name, False)
    def __repr__(self):
        return self.name
    def symbols(self):
        return {self.name}
    
class Not(Sentence):
    def __init__(self, operand):
        self.operand=operand
    def evaluate(self, model):
        return not self.operand.evaluate(model)
    def __repr__(self):
        return f"Not({self.operand})"
    def symbols(self):
        return self.operand.symbols()
    
class And(Sentence):
    def __init__(self, *conjuncts):
        self.conjuncts = conjuncts
    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)
    def __repr__(self):
        return f"({' ∧ '.join(repr(c) for c in self.conjuncts)})"
    def symbols(self):
        result = set()
        for conjunct in self.conjuncts:
            result.update(conjunct.symbols())
        return result

class Or(Sentence):
    def __init__(self, *disjuncts):
        self.disjuncts = disjuncts
    def evaluate(self, model):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)
    def __repr__(self):
        return f"({' ∨ '.join(repr(d) for d in self.disjuncts)})"
    def symbols(self):
        result = set()
        for disjunct in self.disjuncts:
            result.update(disjunct.symbols())
        return result
    
class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent
    def evaluate(self, model):
        return Or(Not(self.antecedent), self.consequent).evaluate(model)
    def __repr__(self):
        return f"({repr(self.antecedent)} => {repr(self.consequent)})"
    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())
    
class Biconditional(Sentence):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, model):
        return And(Implication(self.left, self.right),
                   Implication(self.right, self.left)).evaluate(model)
    def __repr__(self):
        return f"({repr(self.left)} <=> {repr(self.right)})"
    def symbols(self):
        return self.left.symbols().union(self.right.symbols())
    


def model_check(sentence, query):
    symbols = sentence.symbols() | query.symbols()
    return check_all(sentence, query, symbols, {})

def check_all(sentence, query, symbols, model):
    if not symbols:
        if sentence.evaluate(model):
            return query.evaluate(model)
        return True
    
    remaining = symbols.copy()
    p = remaining.pop()
    model_true = model.copy()
    model_true[p] = True
    model_false = model.copy()
    model_false[p] = False
    return (check_all(sentence, query, remaining, model_true) and
            check_all(sentence, query, remaining, model_false))



AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)), 
    Not(And(BKnight, BKnave)),
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    Implication(AKnight, Or(AKnave, AKnight)),
    Implication(AKnave, Not(Or(AKnave, AKnight))),
    Implication(BKnight, Implication(AKnight, BKnave)),
    Implication(BKnave, Implication(AKnave, Not(BKnave))),
    Implication(BKnight, (CKnave)),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

