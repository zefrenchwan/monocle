# monocle

Tool to list what a website is about. 

Name comes from "monocle", a french word. 
It is, basically, a piece of glass to correct one eye vision (just one eye). 
This code is really basic webscraping, it will not provide you a definitive vision of what a website is about. 

## TLDR

1. Provide a website and a file path, the tool scraps the website, find named entities and puts it all into a file
2. Internals use a NLP model. Default for french so far, so results are not amazing. Give it a better model if you need
3. Typical use is to find what a website is about (to put ads in it after the 3rd party cookies era, or to automate some searches on someone / something / a company / whatever)
4. Licence is MIT licence, it means basically that you may use it, sell it, whatever. Just mention this licence and this copyright (zefrenchwan, 2024)
5. Use it but do not break others websites by overloading them 


## What does it produce ? 

Given a website, it scraps any pages in that website (not the full web). 
It produces a JSON file, and that file contains:
* lang (fr so far): the lang of the website
* date: end of extraction date
* url: first url (in general, the root of the website) 
* entities: named entities and their types

Let us zoom on entities. 
It means named entities, that is PER (persons), LOC (location), ORG (organizations), or MISC (some stuff that may be an entity, but classification is unclear). 
For each label (PER, LOC, etc), you have: 
* the number of appearences of named entities
* said named entities

For instance 
```
      "LOC": {
            "4": [
                "Rome",
```

means that `Rome` is a named entity that is a location (LOC) and it appeared `4` times in the website. 

## How do I use it ? 

First, *pay attention to your usage*. 
This tool scrapes a website starting at a given page. 
Be sure that the website allows it and that the load is acceptable for that website. 
For instance, wikipedia says it: they provide their full content as a database, no need to webscrap them. 

Second, *this code deals with NLP model itself, no need to install anything else*.
During the first launch, code will not find the right model, so it will download it.  
Reason is that spacy is a "technical detail" somehow, that an end user (you) does not have to bother with. 
It comes with a counterpart: if your website is not in french, you need to change the code to download the correct spacy model. 


Then, assume you want to scrap website `https://iamawebsite.fr` and write result into a `result.json` file. 
Usage would be `pipenv run .\main.py https://iamawebsite.fr result.json` 

## How does it work ?

Algorithm is a map reduce (to find web page content and group stats to a single global result). 
To find pages to explore, it is a graph walkthrough with no cycle. 
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
* Spacy model is the largest one, it focuses on accuracy. To use a better model for your use case, change `initializations.py`


## Some common comments / FAQ

### I am not happy with the results

I used spacy largest model. 
Feel free to change this code or use another better model. 

### Your code may face encoding issues

Website may provide its charset (or not). 
Default is UTF-8, because it is Python default. 
Charset recognition is really painful, costs a lot and provides no benefit for an open source code. 

### I have so many ideas to...

Clone this code, do your stuff, and if you want, share it. 
Code is under MIT licence for that reason. 

### I want to use your code for commercial use

Code is under MIT licence, you may do it. 
Although, there are some better webscraping techniques: 
* to find URL
* to find web page content
* to list named entities

### Any though on some better architecture ?

Sure ! 
* split webscraping and nlp analysis, use apache kafka to sync them (typical producer - consumer)
* save webpages, they may change
* use some reference data to improve named entities recognition 

### Why the MIT licence ? You could be rich and famous and...

Of course...
First of all, because you may use my code with no limit expect LAW and just mentioning me. 
I wanted to share this simple project (less than a week of work) to help anyone that likes webscraping. 

### What changes will you make on this project ? 

Not sure I will. 
Code is sufficient for its purpose: a base for others developers to use. 