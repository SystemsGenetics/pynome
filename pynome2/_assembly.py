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
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        workDir = os.path.join(settings.rootPath,taxId,assemblyName)
                        meta = self.__loadMeta_(workDir)
                        if species and meta["species"].lower() != species.lower():
                            continue
                        rootName = meta["genus"]+"_"+meta["species"]
                        if meta["intraspecific_name"]:
                            rootName += "_"+meta["intraspecific_name"]
                        rootName += "-"+meta["assembly_id"]
                        self.__mirrorFasta_(workDir,rootName+".fa",meta)
                        self.__mirrorGff_(workDir,rootName+".gff",meta)


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
        self.__prepareDataDirs_()
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
               The metadata information for the given working directory. If the
               processed keys are not set then they are added and set to false.
        """
        with open(os.path.join(workDir,"metadata.json"),"r") as ifile:
            meta = json.loads(ifile.read())
            if "fasta_processed" not in meta:
                meta["fasta_processed"] = False
            if "gff_processed" not in meta:
                meta["gff_processed"] = False
            return meta


    def __mirrorFasta_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Mirrors the FASTA file of the given assembly, running post processing on
        the local FASTA file if a new one has been downloaded from the remote
        server.

        Parameters
        ----------
        workDir : string
                  The working directory of the assembly.
        path : string
               The full file name of the given assembly's FASTA file located
               within the given working directory.
        meta : dictionary
               The full metadata of the given assembly.
        """
        title = os.path.join(meta["taxonomy"]["id"],os.path.split(workDir)[-1])
        try:
            fasta = self.__mirrors[meta["mirror_type"]].mirrorFasta(
                workDir
                ,path
                ,meta["mirror_data"]
                ,title
            )
            if fasta:
                meta["fasta_processed"] = False
            if not meta["fasta_processed"]:
                filePath = os.path.join(workDir,path)
                core.log.send("Hisat2 Indexing FASTA "+title)
                outBase = os.path.join(
                    workDir
                    ,(subprocess.check_output(["hisat2","--version"])
                        .decode()
                        .split("\n")[0]
                        .replace("/","|")
                        .replace(" ","_")
                    )
                )
                os.makedirs(outBase,exist_ok=True)
                outBase = os.path.join(outBase,path[:-3])
                cmd = ["hisat2-build","--quiet","-p",str(os.cpu_count()),"-f",filePath,outBase]
                assert(subprocess.run(cmd).returncode==0)
                core.log.send("Salmon Indexing FASTA "+title)
                outBase = os.path.join(
                    workDir
                    ,(subprocess.check_output(["salmon","--version"])
                        .decode()
                        .split("\n")[0]
                        .replace("/","|")
                        .replace(" ","_")
                    )
                )
                cmd = [
                    "salmon"
                    ,"index"
                    ,"--index"
                    ,outBase
                    ,"--transcripts"
                    ,filePath
                    ,"--threads"
                    ,str(os.cpu_count())
                ]
                assert(subprocess.run(cmd,capture_output=True).returncode==0)
                core.log.send("Kallisto Indexing FASTA "+title)
                outBase = os.path.join(
                    workDir
                    ,(subprocess.check_output(["kallisto","version"])
                        .decode()
                        .split("\n")[0]
                        .replace("/","|")
                        .replace(" ","_")
                    )
                )
                os.makedirs(outBase,exist_ok=True)
                outBase = os.path.join(outBase,path[:-3]+".idx")
                cmd = ["kallisto","index","--index",outBase,filePath]
                assert(subprocess.run(cmd,capture_output=True).returncode==0)
                meta["fasta_processed"] = True
                self.__saveMeta_(workDir,meta)
        except:
            traceback.print_exc()


    def __mirrorGff_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Mirrors the GFF file of the given assembly, running post processing on
        the local GFF file if a new one has been downloaded from the remote
        server.

        Parameters
        ----------
        workDir : string
                  The working directory of the assembly.
        path : string
               The full file name of the given assembly's GFF file located
               within the given working directory.
        meta : dictionary
               The full metadata of the given assembly.
        """
        title = os.path.join(meta["taxonomy"]["id"],os.path.split(workDir)[-1])
        try:
            gff = self.__mirrors[meta["mirror_type"]].mirrorGff(
                workDir
                ,path
                ,meta["mirror_data"]
                ,title
            )
            if gff:
                meta["gff_processed"] = False
            if not meta["gff_processed"]:
                core.log.send("Writing GTF from GFF "+title)
                filePath = os.path.join(workDir,path)
                tPath = os.path.join(workDir,"temp.gff")
                basePath = filePath[:-4]
                cmd = ["cp",filePath,tPath]
                assert(subprocess.run(cmd).returncode==0)
                cmd = ["gffread","-T",tPath,"-o",basePath+".gtf"]
                assert(subprocess.run(cmd).returncode==0)
                cmd = ["rm",tPath]
                assert(subprocess.run(cmd).returncode==0)
                with open(basePath+".Splice_sites",'w') as ofile:
                    core.log.send("Writing Spice sites from GTF "+title)
                    cmd = ['hisat2_extract_splice_sites.py',basePath+".gtf"]
                    assert(subprocess.run(cmd,stdout=ofile).returncode==0)
                meta["gff_processed"] = True
                self.__saveMeta_(workDir,meta)
        except:
            traceback.print_exc()


    def __prepareDataDirs_(
        self
        ):
        """
        Creates any of the special data directories for all implemented crawlers
        if they do not exist.
        """
        for crawler in self.__crawlers.values():
            d = os.path.join(settings.rootPath,"."+crawler.name())
            os.makedirs(d,exist_ok=True)


    def __saveMeta_(
        self
        ,workDir
        ,meta
        ):
        """
        Saves the given assembly metadata to the given working directory.

        Parameters
        ----------
        workDir : string
                  The working directory where the given assembly metadata is
                  saved as JSON to the special "metadata.json" file.
        meta : dictionary
               The given assembly metadata that is saved to the given working
               directory as JSON.
        """
        with open(os.path.join(workDir,"metadata.json"),"w") as ofile:
            return ofile.write(json.dumps(meta,indent=4) + "\n\n")