from urllib.parse import urlsplit
import urllib.request
import urllib.response

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
        self.headers = {
            'User-agent': 'Mozilla/5.0' ,    
            'Content-Type': "text/plain;charset=UTF-8"       
        }

    def __iter__(self):
        return self

    def __next__(self):
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
            return None 
        finally: 
            if response is not None:
                response.close()
        # extract text and maps it
        result = content.text
        # then, look for the next urls to visit
        self.schedule(content)
        # page is now processed
        self.pages.add(current)
        return result 

    def accept(self, url:str) -> bool:
        """
        test if an URL should be explored. 
        Add in here all the logic you need to exclude resources
        """
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

    def schedule(self, content):
        """
        Given a BS4 content, parse it to find links to go through. 
        This is a separate method so that you may add your own heuristics
        """
        for link in content.find_all('a', href=True):
                url = self.standardize(link.get("href"))
                if url not in self.pages and self.accept(url):
                    self.elements.append(url)
