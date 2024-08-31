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
        return [ re.sub(r"\s+"," ", value) for value in raw.split("\n") if len(value) != 0 and re.match(r"\s*\w+\s*",value) ]    
