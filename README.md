# monocle

Tool to list what a website is about. 

Name comes from "monocle", a french word. 
It is, basically, a piece of glass to correct one eye vision (just one eye). 
This code is really basic webscraping, it will not provide you a definitive vision of what a website is about. 

## How do I use it ? 

First, *pay attention to your usage*. 
This tool scrapes a website starting at a given page. 
Be sure that the website allows it and that the load is acceptable for that website. 
For instance, wikipedia says it: they provide their full content as a database, no need to webscrap them. 


Then, assume you want to scrap website `https://iamawebsite.fr`. 
Usage would be `pipenv run .\main.py https://iamawebsite.fr` 

## How do I change it ?

Algorithm is a graph walkthrough with no cycle. 
It just starts from the provided URL, explore each page to find outgoing links. 
Then, it picks the next non processed page, it loads the page, etc. 

Interesting parts are:
* data clean to pass from HTML to plain text. Dealt with BS4, just a reponse.text
* picking links. Dealt with a BS4 search for a href. Basic, you may want to change this part
* NLP pipeline. This is the plus-value core. 

### NLP 

This section details the models and frameworks used. 

* NLP library is [Spacy](https://spacy.io/) 
* Supported languages are ... French. To change it, include a new model in `initializations.py`
* Spacy model is the small one, it focuses on speed more than accuracy. To use a better model for your use case, change `initializations.py`

