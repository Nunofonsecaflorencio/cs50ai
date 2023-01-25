import sys

from crossword import *
from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        # for v, ws in self.domains.items():
        #     print(f'{v} -> {ws}')
        self.ac3()
        # print()
        # for v, ws in self.domains.items():
        #     print(f'{v} -> {ws}')
        # print()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in self.domains.items():
            for word in domain.copy():
                # Unary constraint: word length
                if variable.length != len(word):
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        
        if not overlap:
            return False
        
        for x_word in self.domains[x].copy():
            i, j = overlap
            # if there is a overlap with same characters
            if x_word[i] not in [y_word[j] for y_word in self.domains[y]]:
                self.domains[x].remove(x_word) 
                revised = True
        
        return revised           
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # initialize the queue
        queue = arcs if arcs else [
            overlap_vars for overlap_vars in self.crossword.overlaps 
            if self.crossword.overlaps[overlap_vars]
        ]
        # print('\narcs:')
        # for (x, y) in queue:
        #     print(f'{x} [x] {y}')
            
        while queue:
            # Dequeue an arc pair
            X, Y = queue.pop(0)
            # Revise
            if self.revise(X, Y):

                if len(self.domains[X]):
                    return False # No solution
                
                for Z in (self.crossword.neighbors(X) - {Y}):
                    # Enqueue arc (Z, X) to be revised
                    queue.append((Z, X))       
            
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all([assignment.get(variable) for variable in self.crossword.variables])

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable, word in assignment.items():
            # all values are distinct
            if list(assignment.values()).count(word) > 1:
                return False
            # every value is the correct length
            if len(word) != variable.length:
                return False
            # there are no conflicts between neighboring variables
            for neighbor in self.crossword.neighbors(variable):
                if neighbor not in assignment:
                    continue
                i, j = self.crossword.overlaps[variable, neighbor]
                if word[i] != assignment[neighbor][j]:
                    return False
        return True    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Counts the number of values ruled out for neighboring unassigned variables
        # For each word in domain
        ruled_out = dict()
        # Simulate assigning each domain
        for word in self.domains[var]:
            ruled_out[word] = 0
            # check the neighbors
            for neighbor in self.crossword.neighbors(var):
                # neighboring unassigned variables
                if neighbor in assignment:
                    continue
                # count how many words in neighbor domain will be affected (eliminated)
                i, j = self.crossword.overlaps[var, neighbor]
                eliminated_n = sum([word[i] != y_word[j] for y_word in self.domains[neighbor]])
                ruled_out[word] += eliminated_n
        
        return sorted(self.domains[var], key=ruled_out.get)       
            
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get all unassigned_variables
        unassigned_variables = list(self.crossword.variables - assignment.keys())
        # if there is only one, dont need to sort
        if len(unassigned_variables) == 1:
            return unassigned_variables[0]
        
        domain_lengths = {var: len(self.domains[var]) for var in unassigned_variables}
        # sort by minimum remaining value heuristic
        unassigned_variables = sorted(unassigned_variables, key=domain_lengths.get)
        
        # no tie
        if domain_lengths[unassigned_variables[0]] != domain_lengths[unassigned_variables[1]]:
            return unassigned_variables[0]
        
        # sort by degree heuristic
        unassigned_variables = sorted(unassigned_variables, key=lambda var: len(self.crossword.neighbors(var)), reverse=True)
        
        return unassigned_variables[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        domains_backup = deepcopy(self.domains)
        
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            if self.consistent(new_assignment):
                # Make inferences with AC-3
                self.ac3([(Y, var) for Y in self.crossword.neighbors(var)])
                
                result = self.backtrack(new_assignment)
                if result:
                    return result

            # Remove inferences (AC-3)
            self.domains = domains_backup
            
        return None
     
    
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
