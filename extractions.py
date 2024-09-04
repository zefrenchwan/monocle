import spacy.language
import re
from results import LocalResult

class Extractor:

    def __init__(self, nlp: spacy.language.Language):
        self.processor = nlp
        self.counters = dict()
        # Spacy limits text size, especially for NER, so we store the max size
        self.size = nlp.max_length

    def extract(self, raw:str, url: str) -> LocalResult:
        values = self.clean(raw)
        text = ".\n".join(values)
        result = LocalResult(url)
        # then, process document
        processable = text if len(text) < self.size else text[0:self.size]
        doc = self.processor(processable)
        for entity in doc.ents:
            result.add(entity.text_with_ws, entity.label_)
        return result 

        
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
