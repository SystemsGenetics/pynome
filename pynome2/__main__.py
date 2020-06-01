"""
This contains the main entry point function of this application.
"""
import argparse
from . import core
from . import crawler
from . import settings
# https://stackoverflow.com/questions/29026709/how-to-get-ftp-files-modify-time-using-python-ftplib
# Use the first one for individual files




def main():
    """
    Starts execution of this application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",dest="species",default="")
    parser.add_argument("-d",dest="rootPath",default=None)
    parser.add_argument("-q",dest="notEcho",action="store_true")
    args = parser.parse_args()
    if args.rootPath:
        settings.rootPath = args.rootPath
    core.log.setEcho(not args.notEcho)
    core.assembly.registerCrawler(crawler.Ensembl())
    core.assembly.crawl(args.species)








if __name__ == "__main__": main()
