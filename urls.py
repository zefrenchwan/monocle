from urllib.parse import urlsplit
import urllib.request
import urllib.response
import re 

from bs4 import BeautifulSoup


class UrlVisitor:
    """
    URL visitor reads an url, gets the text content and tries to find other pages to parse.
    """
    def __init__(self, start:str):
        parts = urlsplit(start)
        self.scheme = parts.scheme 
        self.domain = parts.netloc
        self.base = self.scheme + "://" + self.domain + "/"
        self.start = start 
        self.elements = [start]
        self.pages = set(self.elements)
        self.parser = 'html.parser'
        # source for this regexp: https://www.geeksforgeeks.org/python-check-url-string/
        self.urlreader = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", re.IGNORECASE)
        self.headers = {
            'User-agent': 'Mozilla/5.0' ,    
            'Content-Type': "text/plain;charset=UTF-8"       
        }

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str,str|None]:
        """
        Iterator over page and content. 
        First value is URL, second value is page content, or none for reading failure
        """
        if len(self.elements) == 0:
            raise StopIteration
        # pop first url, read content and find links
        result = None 
        current = self.elements.pop()
        # call may fail, and process should keep going
        content = None
        response = None 
        try:
            request = urllib.request.Request(current, headers=dict(self.headers))
            response = urllib.request.urlopen(request)
            payload = response.read()
            content = BeautifulSoup(payload, self.parser, from_encoding=response.info().get_param('charset'))    
        except:
            self.pages.add(current)
            return current, None 
        finally: 
            if response is not None:
                response.close()
        # extract text and maps it
        result = content.text
        # then, look for the next urls to visit
        self.schedule(content)
        return current, result 

    def accept(self, url:str) -> bool:
        """
        test if an URL should be explored. 
        Add in here all the logic you need to exclude resources
        """
        if url in ["#", "/#"]:
            return False
        split = urlsplit(url)
        if split is None:
            return False
        # not same domain ==> leave
        if not split.netloc.endswith(self.domain):
            return False
        # wordpress, technical content, skip it
        if split.path.startswith("/wp-"):
            return False
        # exclude some content types that are irrelevant
        if not url.endswith("/"):
            resource_type = url[url.rindex(".")+1:]
            return resource_type not in ["css","jpg","jpeg","pdf","xml","json"]
        return True


    def standardize(self, url:str) -> str:
        """
        Given a url, make it standard for parsing. 
        For instance /jeux/ should become "https://mysite.fr/jeux"
        """
        if url.startswith("//"):
            return self.scheme + ":" + url
        if url.startswith("/"):
            return self.base[:-1]+url
        return url

    def schedule(self, content):
        """
        Given a BS4 content, parse it to find links to go through. 
        This is a separate method so that you may add your own heuristics
        """
        matches = []
        # restrict to href to avoid all the js scripts
        for value in re.findall(r"href=\S+[\s>]",str(content)):
            matchings = [matching[0] for matching in self.urlreader.findall(value)]
            if len(matchings) != 0:
                url = matchings[0]
                matches.append(url)
        # deduplicate
        matches = list(set(matches))
        for element in matches:
            element = self.standardize(element)
            if element not in self.pages and self.accept(element):
                self.elements.append(element)
            self.pages.add(element)