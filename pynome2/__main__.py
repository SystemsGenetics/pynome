"""
Detailed description.
"""
from . import core
from .crawler import ensembl
# https://stackoverflow.com/questions/29026709/how-to-get-ftp-files-modify-time-using-python-ftplib
# Use the first one for individual files




def main():
    """
    Detailed description.
    """
    core.Assembly().registerCrawler(ensembl.Ensembl(),"Ensembl")
    core.Assembly().crawl()








if __name__ == "__main__": main()
