import sys
from initializations import *


if __name__== "__main__":
    # read args, build parameters based on them
    args = sys.argv[1:]
    if len(args) not in [1,2]:
        usage()
        sys.exit(-1)
    url = args[0]
    lang = "fr"
    if len(args) == 2:
        lang = args[2]
    # lang and url are set, build elements
    extractor = build_extractor(lang)
    for content in build_iterator(url):
        extractor.extract(content)