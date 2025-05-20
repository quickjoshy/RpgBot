strStat = 0
intStat = 1
endStat = 2
spdStat = 3

class Profile:

    def __init__(self, name, str, int, end, spd, moves, inventory):
        self.name = name
        self.str = str
        self.int = int
        self.spd = spd
        self.end = end
        self.stats = [str,int, end, spd]
        self.moves = moves
        self.inventory = inventory

    def display(self):
        print(f"Name: {self.name}")
        print(f"Speed: {self.spd}")
        print(f"Intelligence: {self.int}")
        print(f"Strength: {self.str}")
        for move in self.moves:
            print(f"Move: {move.name}")