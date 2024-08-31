import spacy.language
import re


class Extractor:

    def __init__(self, nlp: spacy.language.Language):
        self.processor = nlp

    def extract(self, raw:str):
        values = self.clean(raw)
        print("\n".join(values))
        
    def clean(self,raw:str) -> list[str]:
        """
        Clean raw text (spaces, etc)
        """
        lines = [ re.sub(r"\s+"," ", value) for value in raw.split("\n") if len(value) != 0 and re.match(r"\s*\w+\s*",value) ]
        # ugly and slow, but super efficient: loop and clean spaces as much as possible
        result = []
        for line in lines:
            size = len(line)
            line = line.replace(r"\s\s+"," ")
            while len(line) < size:
                line = line.replace(r"\s\s+"," ")
                size = len(line)
            # now, line is clean, you may include here all specific processing
            result.append(line)
        return result