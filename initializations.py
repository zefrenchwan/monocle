import spacy 
import spacy.cli
import spacy.language
from typing import Iterable
from urls import UrlVisitor
from extractions import Extractor

def usage():
    """
    Display basic information about the tool
    """
    print("Tool to parse a website and extract named entities")
    print("usage is: main.py website lang")
    print("for instance: pipenv run main.py https://leparisien.fr fr")
    print("lang parameter is optional, default is set to fr")
    print("for instance: pipenv run main.py https://leparisien.fr")


def build_iterator(url:str) -> Iterable[str|None]:
    """
    Given a url, returns a tool to iterate from this url to the visible ones. 
    Result returns the text of each visited page as a string. 
    """
    return UrlVisitor(url) 

def build_extractor(lang:str) -> Extractor:
    """
    Given a language, find matching model and build extractor. 
    Extractor just decorates the model
    """
    model = build_model(lang)
    return Extractor(model)


def build_model(lang:str) -> spacy.language.Language:
    """
    Create nlp model for a given language. 
    Download it if necessary
    """
    models = {"fr":"fr_core_news_sm"}
    nlp = None 
    model = models[lang]
    try:
        nlp = spacy.load(model)
    except OSError:
        spacy.cli.download(model)
    nlp = spacy.load(model)
    return nlp