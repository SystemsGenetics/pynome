"""
This contains the main entry point function of this application.
"""
from . import core
from . import crawler
# https://stackoverflow.com/questions/29026709/how-to-get-ftp-files-modify-time-using-python-ftplib
# Use the first one for individual files




def main():
    """
    Starts execution of this application.
    """
    core.assembly.registerCrawler(crawler.Ensembl(),"Ensembl")
    core.assembly.crawl()








if __name__ == "__main__": main()
