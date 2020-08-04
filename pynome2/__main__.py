"""
This contains the main entry point function of this application.
"""
import argparse
from . import core
from . import crawler
from . import mirror
from . import settings




def main():
    """
    Starts execution of this application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",dest="crawl",action="store_true")
    parser.add_argument("-m",dest="mirror",action="store_true")
    parser.add_argument("-t",dest="species",default="")
    parser.add_argument("-d",dest="rootPath",default=None)
    parser.add_argument("-q",dest="notEcho",action="store_true")
    args = parser.parse_args()
    if args.rootPath:
        settings.rootPath = args.rootPath
    core.log.setEcho(not args.notEcho)
    #core.assembly.registerCrawler(crawler.Ensembl())
    core.assembly.registerCrawler(crawler.NCBI())
    core.assembly.registerMirror("ftp_gunzip",mirror.FTPGunzip())
    if not args.crawl and not args.mirror:
        core.assembly.crawl(args.species)
        core.assembly.mirror(args.species)
    else:
        if args.crawl:
            core.assembly.crawl(args.species)
        if args.mirror:
            core.assembly.mirror(args.species)








if __name__ == "__main__": main()
