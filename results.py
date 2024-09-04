from counters import *
from datetime import datetime
import json 


class LocalResult:
    """
    Local results are data read from one URL, assumed to be the simplest data unit.  
    Global results (results) are reduced results, that is whole site level
    """
    def __init__(self, url: str, blocks: int = 3):
        """
        Constructs a result for an URL
        """
        self.url = url
        self.counter = Counter() 
        self.blocks = blocks

    
    def add(self, value:str, label:str|None=None, counter=1):
        """
        Given a label ("named entities", "noun chunks"), add one count for an occurence. 
        Note that label is not mandatory. If you count more than once, let us say N times a value, then counter = N
        """
        self.counter.add(value, label, counter)

    def best_values(self, label:str|None=None, blocks: int= -1) -> dict[int,list[str]]:
        """
        Given a local result and a label, some words may appear 10 times, some 6, some 4, rest less than 3.  
        Blocks set to 2 will display values for 10 and 6 (the 2 best) as sorted lists of elements
        """
        size = blocks if blocks > 0 else self.blocks
        return self.counter.best_values(size, label)
    
    def keys(self) -> set[str]:
        """
        Label keys
        """
        return set(self.counter.keys())


class GlobalResult:
    """
    Global result just aggregages data for a full website
    """
    def __init__(self, url):
        """
        Constructs global result for a given website 
        """
        self.url = url
        self.counter = Counter()
        self.blocks = 6

    def add(self, local:LocalResult):
        """
        Add result for a page into the global result
        """
        self.counter = self.counter + local.counter

    def reduce(self) -> dict[str,any]:
        """
        Aggregates all data to a dict to write. 
        Separated method to ease your refactoring
        """
        content = dict()
        content["lang"]= "fr"
        content["url"] = self.url
        content["date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        content["entities"] = dict()
        for label in self.counter.keys():
            content["entities"][label] = dict()
            sumup = self.counter.best_values(self.blocks, label)
            keys = sorted(list(sumup.keys()))
            keys.reverse()
            for key in keys:
                content["entities"][label][key] = sumup[key]
        return content

    def aggregate(self, path):
        """
        Write reduced content into a file 
        """
        content = self.reduce()
        payload = json.dumps(content, indent=4)
        with open(path, "w") as output:
            output.write(payload)