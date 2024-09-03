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
        self.counters = dict()

    
    def add(self, value:str, label:str|None=None, counter=1):
        """
        Given a label ("named entities", "noun chunks"), add one count for an occurence. 
        Note that label is not mandatory. If you count more than once, let us say N times a value, then counter = N
        """
        if label is None:
            label = ""
        elif len(label) == 0:
            raise KeyError()
        counters = self.counters.get(label)
        if counters is None:
            counters = dict()
            self.counters[label] = counters
        previous = counters.get(value)
        if previous is None:
            counters[value] = counter
        else:
            counters[value] = previous + counter
        self.counters[label][value] = counters[value]

    def best_values(self, blocks: int= 1, label:str|None=None) -> dict[int,list[str]]:
        """
        Given a local result and a label, some words may appear 10 times, some 6, some 4, rest less than 3.  
        Blocks set to 2 will display values for 10 and 6 (the 2 best) as sorted lists of elements
        """
        if label is None:
            label = ""
        values = self.counters.get(label)
        if values is None:
            return dict()
        best_choices = set()
        min = -1
        for k,val in values.items():
            if len(best_choices) < blocks:
                if val not in best_choices:
                    best_choices.add(val)
                    min = val
            elif val > min and val not in best_choices:
                best_choices.remove(min)
                best_choices.add(val)
                min = val
        # best choices found, get values
        result = dict()
        for k,v in values.items():
            if v in best_choices:
                if result.get(v) is None:
                    result[v] = set()
                result[v].add(k)
        for k,v in result.items():
            result[k] = sorted(list(v))
        return result 
    
    def keys(self) -> set[str]:
        """
        Label keys
        """
        return set(self.counters.keys())