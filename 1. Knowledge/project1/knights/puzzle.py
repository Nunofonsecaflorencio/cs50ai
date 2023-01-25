from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


gameRules = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)
# Puzzle 0
# A says "I am both a knight and a knave."

# What said
ASaid = And(AKnight, AKnave)

knowledge0 = And(
    # Problem
    gameRules,

    # Who is Knight
    Implication(AKnight, ASaid),
    Implication(AKnave, Not(ASaid))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
ASaid = And(AKnave, BKnave)

knowledge1 = And(
    # Problem
    gameRules,
    # Who is Knight
    Implication(AKnight, ASaid),
    Implication(AKnave, Not(ASaid)),
    # if A is Knight then B is Knave
    Implication(AKnight, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASaid = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BSaid = Not(ASaid)

knowledge2 = And(
    # Problem
    gameRules,
    # Who is Knight
    Implication(AKnight, ASaid),
    Implication(AKnave, Not(ASaid)),
    # if A is Knight then B is Knave
    Implication(AKnight, BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASaid = Or(AKnight, AKnave)
BSaid = And(Implication(AKnave, BKnight), CKnave)
CSaid = AKnight
knowledge3 = And(
    gameRules,

    # A
    Implication(AKnight, ASaid),
    Implication(AKnave, Not(ASaid)),

    # B
    Implication(BKnight, BSaid),
    Implication(BKnave, Not(BSaid)),

    # C
    Implication(CKnight, CSaid),
    Implication(CKnave, Not(CSaid)),
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
