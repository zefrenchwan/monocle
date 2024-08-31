from urllib.parse import urlsplit
import urllib.request

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
        self.index = 0
        self.parser = 'html.parser'
        self.headers = {
            'User-agent': 'Mozilla/5.0'            
        }

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.elements):
            raise StopIteration
        # pop first url, read content and find links
        result = None 
        with self.read(self.elements[self.index]) as response:
            content = BeautifulSoup(response.read(), self.parser, from_encoding=response.info().get_param('charset'))
            result = content.text
            # then, look for the next urls to visit
            links = list(set(content.find_all('a', href=True)))
            for link in links:
                parsed = self.standardize(link.get("href"))
                if parsed is not None and parsed not in self.elements and self.accept(parsed):
                    self.elements.append(parsed)
        self.index = self.index + 1    
        return result 

    def accept(self, url:str) -> bool:
        """
        test if an URL should be explored. 
        Add in here all the logic you need to exclude resources
        """
        split = urlsplit(url)
        # not same domain ==> leave
        if not split.netloc.endswith(self.domain):
            return False
        # wordpress, technical content, skip it
        if split.path.startswith("/wp-"):
            return False
        if not url.endswith("/"):
            resource_type = url[url.rindex(".")+1:]
            return resource_type not in ["css","jpg","jpeg","pdf"]
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

    def read(self, url:str) -> str:                
        """
        Given an URL, read its content. 
        It is not just read, it includes headers to add, etc
        """
        request = urllib.request.Request(url, headers=dict(self.headers))
        return urllib.request.urlopen(request)
