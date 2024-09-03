import sys
from initializations import *
from results import *

if __name__== "__main__":
    # read args, build parameters based on them
    args = sys.argv[1:]
    if len(args) not in [1,2]:
        usage()
        sys.exit(-1)
    url = args[0]
    lang = "fr"
    if len(args) == 2:
        lang = args[1]
    # lang and url are set, build elements
    extractor = build_extractor(lang)
    result = GlobalResult()
    for url, content in build_iterator(url):
        if content is None:
            continue
        print(url)
        element = extractor.extract(content, url)
        for key in element.keys():
            print(key)
            print(element.best_values(2, key))
        print()
        print()
        result.add(element)
    # then, reduce and build your own data
    result.aggregate()