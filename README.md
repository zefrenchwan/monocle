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

## NLP 

This section details the models and frameworks used. 

### What framework / tool do you use for NLP ? 

[Spacy](https://spacy.io/) 

### What are supported languages ?

French. 
To change it, include a new model in `initializations.py`

### Your model is not accurate / I am not happy with the results 

Model is the smallest one, it focuses on speed more than accuracy. 
To use a better model, change `initializations.py`

