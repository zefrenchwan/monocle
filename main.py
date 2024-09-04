import sys
from initializations import *
from results import *

if __name__== "__main__":
    # read args, build parameters based on them
    args = sys.argv[1:]
    if len(args) != 2:
        usage()
        sys.exit(-1)
    url = args[0]
    path = args[1]
    lang = "fr"
    # for each scraped page, map it to an extracted content
    extractor = build_extractor(lang)
    result = GlobalResult(url)
    for url, content in build_iterator(url):
        if content is None:
            continue
        print(url)
        element = extractor.extract(content, url)
        result.add(element)
    # then, reduce and build your own data
    result.aggregate(path)