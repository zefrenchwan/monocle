from counters import *


class LocalResult:
    """
    Local results are data read from one URL. 
    Global results (results) are reduced results, that is whole site level
    """
    def __init__(self, url: str):
        """
        Constructs a result for an URL
        """
        self.url = url
        self.counter = Counter() 

    
    def add(self, value:str, label:str|None=None, counter=1):
        """
        Given a label ("named entities", "noun chunks"), add one count for an occurence. 
        Note that label is not mandatory. If you count more than once, let us say N times a value, then counter = N
        """
        self.counter.add(value, label, counter)

    def best_values(self, blocks: int= 1, label:str|None=None) -> dict[int,list[str]]:
        """
        Given a local result and a label, some words may appear 10 times, some 6, some 4, rest less than 3.  
        Blocks set to 2 will display values for 10 and 6 (the 2 best) as sorted lists of elements
        """
        return self.counter.best_values(blocks, label)
    
    def keys(self) -> set[str]:
        """
        Label keys
        """
        return set(self.counter.keys())


class GlobalResult:

    def __init__(self):
        self.counter = Counter()

    def add(self, local:LocalResult):
        self.counter = self.counter + local.counter

    def aggregate(self):
        for key in self.counter.keys():
            print(self.counter.best_values(3,key))
            print()
    