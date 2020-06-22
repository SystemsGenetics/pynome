"""
Contains the Assembly class.
"""
import json
import os
import subprocess
import traceback
from . import abstract
from . import core
from . import exception
from . import settings








class Assembly():
    """
    This is the singleton assembly class. It is responsible for storing a list
    of all available crawler and mirror implementations. It provides method for
    crawling with all implemented crawlers along with syncing all local database
    files using the available mirrors.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes the singleton assembly instance.
        """
        self.__crawlers = {}
        self.__mirrors = {}


    ####################
    # PUBLIC - Methods #
    ####################


    def mirror(
        self
        ,species
        ):
        """
        Iterates through all local database folders, inspecting their metadata
        file and downloading any new data files if new versions are present on
        the remote server. Any downloaded data is properly indexed.

        Parameters
        ----------
        species : string
                  The name of the species that is mirrored, ignoring any other
                  species on the local database. If this string is blank then
                  all species are mirrored.
        """
        for taxId in os.listdir(settings.rootPath):
            path = os.path.join(settings.rootPath,taxId)
            if os.path.isdir(path):
                for assemblyName in os.listdir(path):
                    try:
                        workDir = os.path.join(settings.rootPath,taxId,assemblyName)
                        data = self.__loadMeta_(workDir)
                        if species and data["species"].lower() != species.lower():
                            continue
                        rootName = data["genus"]+"_"+data["species"]
                        if data["intraspecific_name"]:
                            rootName += "_"+data["intraspecific_name"]
                        rootName += "-"+data["assembly_id"]
                        (fasta,gff3) = self.__mirrors[data["mirror_type"]].mirror(
                            workDir
                            ,rootName
                            ,data["mirror_data"]
                        )
                        self.__postProcess_(fasta,gff3,workDir,rootName,data)
                    except:
                        traceback.print_exc()
                        continue


    def crawl(
        self
        ,species
        ):
        """
        Iterates through all registered crawler implementations and crawls their
        remote database to update the local database metadata.

        Parameters
        ----------
        species : string
                  The name of the species that is crawled, ignoring any other
                  species found on the remote server. If this string is blank
                  then all species are crawled.
        """
        for crawler in self.__crawlers.values():
            crawler.crawl(species)
            crawler.assemble()


    def registerCrawler(
        self
        ,crawler
        ):
        """
        Registers a new crawler implementation with the given class instance.

        Parameters
        ----------
        crawler : pynome.abstract.AbstractCrawler
                  The abstract crawler implementation that is registered.
        """
        if not isinstance(crawler,abstract.AbstractCrawler):
            raise exception.RegisterError("Given object is not Crawler instance.")
        if crawler.name() in self.__crawlers.keys():
            raise exception.RegisterError("Crawler '"+name+"' already exists.")
        self.__crawlers[crawler.name()] = crawler


    def registerMirror(
        self
        ,name
        ,mirror
        ):
        """
        Registers a new mirror implementation with the given class instance and
        name.

        Parameters
        ----------
        name : string
               The name of the new abstract mirror implementation. This must be
               unique among all registered mirror implementations.
        mirror : pynome.abstract.AbstractMirror
                 The abstract mirror implementation that is registered.
        """
        if not isinstance(mirror,abstract.AbstractMirror):
            raise exception.RegisterError("Given object is not Mirror instance.")
        if name in self.__mirrors.keys():
            raise exception.RegisterError("Mirror '"+name+"' already exists.")
        self.__mirrors[name] = mirror


    #####################
    # PRIVATE - Methods #
    #####################


    def __loadMeta_(
        self
        ,workDir
        ):
        """
        Getter method.

        Parameters
        ----------
        workDir : string
                  The working directory where the metadata JSON file is located.

        Returns
        -------
        ret0 : dictionary
               The metadata information for the given working directory.
        """
        with open(os.path.join(workDir,"metadata.json"),"r") as ifile:
            return json.loads(ifile.read())


    def __postProcess_(
        self
        ,fasta
        ,gff3
        ,workDir
        ,rootName
        ,meta
        ):
        """
        Detailed description.

        Parameters
        ----------
        fasta : object
                Detailed description.
        gff3 : object
               Detailed description.
        workDir : object
                  Detailed description.
        rootName : object
                   Detailed description.
        meta : object
               Detailed description.
        """
        if fasta or "fasta_processed" not in meta:
            meta["fasta_processed"] = False
        if gff3 or "gff3_processed" not in meta:
            meta["gff3_processed"] = False
        self.__saveMeta_(workDir,meta)
        title = os.path.join(meta["taxonomy"]["id"],os.path.split(workDir)[-1])
        if not meta["fasta_processed"]:
            self.__postProcessFasta_(workDir,rootName,title)
            meta["fasta_processed"] = True
            self.__saveMeta_(workDir,meta)
        if not meta["gff3_processed"]:
            self.__postProcessGff3_(workDir,rootName,title)
            meta["gff3_processed"] = True
            self.__saveMeta_(workDir,meta)


    def __postProcessFasta_(
        self
        ,workDir
        ,rootName
        ,title
        ):
        """
        Detailed description.

        Parameters
        ----------
        workDir : object
                  Detailed description.
        rootName : object
                   Detailed description.
        title : object
                Detailed description.
        """
        core.log.send("Hisat2 Indexing FASTA "+title)
        outBase = os.path.join(workDir,rootName)
        filePath = outBase+".fa"
        cmd = ['hisat2-build','--quiet','-p',str(os.cpu_count()),'-f',filePath,outBase]
        assert(subprocess.run(cmd).returncode==0)


    def __postProcessGff3_(
        self
        ,workDir
        ,rootName
        ,title
        ):
        """
        Detailed description.

        Parameters
        ----------
        workDir : object
                  Detailed description.
        rootName : object
                   Detailed description.
        title : object
                Detailed description.
        """
        core.log.send("Writing GTF from GFF "+title)
        rootPath = os.path.join(workDir,rootName)
        cmd = ['gffread','-T',rootPath+'.gff3','-o',rootPath+'.gtf']
        assert(subprocess.run(cmd).returncode==0)
        with open(rootPath+".Splice_sites",'w') as ofile:
            core.log.send("Writing Spice sites from GFF "+title)
            cmd = ['hisat2_extract_splice_sites.py',rootPath+".gff3"]
            assert(subprocess.run(cmd,stdout=ofile).returncode==0)


    def __saveMeta_(
        self
        ,workDir
        ,meta
        ):
        """
        Detailed description.

        Parameters
        ----------
        workDir : object
                  Detailed description.
        meta : object
               Detailed description.
        """
        with open(os.path.join(workDir,"metadata.json"),"w") as ofile:
            return ofile.write(json.dumps(meta,indent=4) + "\n\n")
