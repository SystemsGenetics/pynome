"""
This contains the main entry point function of this application.
"""
import argparse
from . import core
from . import crawler
from . import mirror
from . import settings




def index(
    path
    ):
    """
    Detailed description.

    Parameters
    ----------
    path : object
           Detailed description.
    """
    with open(path,"r") as ifile:
        parts = [x.strip() for x in ifile.read().split("\n") if x]
        assert(len(parts)==2)
        taxId = parts[0]
        assemblyName = parts[1]
        core.assembly.index(taxId,assemblyName)




def listAll():
    """
    Detailed description.
    """
    i = 0
    for (taxId,assemblyName) in core.assembly.listAllWork():
        with open(settings.JOB_NAME%(i,),"w") as ofile:
            ofile.write(taxId+"\n"+assemblyName+"\n")
        i += 1




def main():
    """
    Starts execution of this application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",dest="crawl",action="store_true")
    parser.add_argument("-m",dest="mirror",action="store_true")
    parser.add_argument("-i",dest="index",action="store_true")
    parser.add_argument("-f",dest="indexFile",default=None)
    parser.add_argument("-I",dest="listAll",action="store_true")
    parser.add_argument("-t",dest="species",default="")
    parser.add_argument("-d",dest="rootPath",default=None)
    parser.add_argument("-q",dest="notEcho",action="store_true")
    args = parser.parse_args()
    if args.rootPath:
        settings.rootPath = args.rootPath
    core.log.setEcho(not args.notEcho)
    core.assembly.registerCrawler(crawler.Ensembl())
    core.assembly.registerCrawler(crawler.Ensembl2())
    core.assembly.registerCrawler(crawler.NCBI())
    core.assembly.registerMirror("ftp_gunzip",mirror.FTPGunzip())
    if args.listAll:
        listAll()
    else:
        if not args.crawl and not args.mirror and not args.index:
            core.assembly.crawl(args.species)
            core.assembly.mirror(args.species)
            if args.indexFile is not None:
                index(args.indexFile)
            else:
                core.assembly.indexSpecies(args.species)
        else:
            if args.crawl:
                core.assembly.crawl(args.species)
            if args.mirror:
                core.assembly.mirror(args.species)
            if args.index:
                if args.indexFile is not None:
                    index(args.indexFile)
                else:
                    core.assembly.indexSpecies(args.species)








if __name__ == "__main__": main()
