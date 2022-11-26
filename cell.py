
class Cell():
    def __init__(self):
        self.isAlive = False
        self.stateHasChanged = False
        self.color = [0, 0, 0]
        self.dna = 0
        # self.dna = []

    def addDna(self, dna: int) -> None:
        self.dna.append(dna)

    def hasDna(self, dna: int) -> bool:
        hasdna = False
        for sDna in self.dna:
            if sDna == dna:
                hasdna = True
        return hasdna

