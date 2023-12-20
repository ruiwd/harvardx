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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        dm = self.domains

        # Remove domain elements with unsatisfactory lengths
        for d in dm:
            for word in dm[d].copy():
                if len(word) != d.length:
                    dm[d].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        dm = self.domains
        ol = self.crossword.overlaps[x,y]
        revised = False

        # Loop through 'x' domain and 'y' domain and if the overlap 
        for i in dm[x].copy():

            # Set as removal candidate until proven otherwise
            rc = True
            for j in dm[y]:
                if i[ol[0]] == j[ol[1]]:
                    rc = False

            if rc:
                dm[x].remove(i)
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
        cw = self.crossword
        dm = self.domains

        # Create queue from arcs
        # Fill queue with all arcs if it's empty
        q = []

        if arcs:
            q = arcs
        else:
            for j in cw.overlaps:
                if cw.overlaps[j]:
                    q.append(j)

        # Revise according to queue, rechecking previous values as revisions are made
        # Return True if acceptable values exist, else False
        while q:
            (x, y) = q.pop()
            
            if self.revise(x, y):
                if not dm[x]:
                    return False
                
                for n in cw.neighbors(x):
                    if n != y:
                        q.append((n, x))

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Every variable filled in
        if len(assignment) == len(self.crossword.variables):
            return True
        
        return False


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        cw = self.crossword
        complete = True

        for v in assignment:
            # Word length check
            if len(assignment[v]) != v.length:
                complete = False
            
            # Valid overlap check
            for n in cw.neighbors(v):
                ol = cw.overlaps[v, n]
                if ol and n in assignment.keys():
                    if assignment[v][ol[0]] != assignment[n][ol[1]]:
                        complete = False

        # Unique word check
        if len(list(assignment.values())) != len(set(assignment.values())):
            complete = False

        return complete


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        dm = self.domains
        cw = self.crossword
        temp = {}

        # For each domain value, count number of overlaps with neighbor domains
        # Temp is a dictionary for each value with count of overlaps
        for val in dm[var]:
            counter = 0
            
            for n in cw.neighbors(var):
                if n not in assignment.keys():
                    for d in dm[n]:
                        if val == d:
                            counter += 1
            
            temp[val] = counter

        # Return temp keys sorted by value
        return list(sorted(temp, key = temp.get))


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        dm = self.domains
        cw = self.crossword

        # List unassigned variables
        uv = {}

        for var in dm:
            if var not in assignment.keys():
               uv[var] = dm[var]

        # Return variable with the minimum domain length and highest degree
        mdl = float('inf')
        for var in uv:
            if len(uv[var]) < mdl:
                mdl = len(uv[var])
        
        for var in uv.copy():
            if len(uv[var]) > mdl:
                uv.pop(var)

        suv = sorted(uv, key = lambda v: len(cw.neighbors(v)), reverse = True)

        return list(suv)[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If complete, return
        if self.assignment_complete(assignment):
            return assignment
        else:
            # Backup assignment and domains in case we need to revert
            ba = deepcopy(assignment)
            bd = deepcopy(self.domains)
            
            # Pick the best variable and value to input
            var = self.select_unassigned_variable(assignment)
            for v in self.order_domain_values(var, assignment):
                assignment[var] = v

                # If consistent, infer options using ac3
                if self.consistent(assignment):
                    arcs = []
                    for n in self.crossword.neighbors(var):
                        arcs.append((n, var))

                    # If inferences OK, continue, otherwise restart from backup
                    if self.ac3(arcs):
                        result = self.backtrack(assignment)
                        if result:
                            return result
                    else:
                        assignment = ba
                        self.domains = bd
                        continue
                else: 
                    assignment = ba
                    self.domains = bd
                    continue


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
