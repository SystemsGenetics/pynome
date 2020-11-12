"""
Contains the Assembly class.
"""
from . import core
from . import interfaces
from . import exception
import json
import os
import re
from . import settings
import subprocess
import traceback








class Assembly():
    """
    This is the singleton assembly class. It is responsible for storing a list
    of all available crawler and mirror implementations. It provides method for
    crawling with all implemented crawlers along with syncing all local database
    files using the available mirrors.
    """


    def __init__(
        self
        ):
        """
        Initializes the singleton assembly instance.
        """
        self.__crawlers = {}
        self.__mirrors = {}


    def index(
        self
        ,taxId
        ,name
        ):
        """
        Indexes the assembly with the given taxonomy ID and assembly name. If
        the indexes are already up to date for that assembly then nothing is
        done.

        Parameters
        ----------
        taxId : string
                The taxonomy ID of the assembly whose indexes are updated.
        name : string
               The name of the assembly whose indexes are updated.
        """
        workDir = os.path.join(settings.rootPath,taxId,name)
        meta = self.__loadMeta_(workDir)
        rootName = meta["genus"]+"_"+meta["species"]
        if meta["intraspecific_name"]:
            rootName += "_"+meta["intraspecific_name"]
        rootName += "-"+meta["assembly_id"]
        self.__indexFasta_(workDir,rootName+".fa",meta)
        self.__indexGff_(workDir,rootName+".gff",meta)


    def indexSpecies(
        self
        ,species
        ):
        """
        Indexes all assemblies with the given species name. If the indexes are
        already up to date for any matched assembly then it is skipped.

        Parameters
        ----------
        species : string
                  The species name matched with assemblies to index.
        """
        if not species:
            return
        for taxId in os.listdir(settings.rootPath):
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        workDir = os.path.join(settings.rootPath,taxId,assemblyName)
                        meta = self.__loadMeta_(workDir)
                        fullName = meta["genus"].lower()+" "+meta["species"].lower()
                        if not species.lower() in fullName:
                            continue
                        rootName = meta["genus"]+"_"+meta["species"]
                        if meta["intraspecific_name"]:
                            rootName += "_"+meta["intraspecific_name"]
                        rootName += "-"+meta["assembly_id"]
                        self.__indexFasta_(workDir,rootName+".fa",meta)
                        self.__indexGff_(workDir,rootName+".gff",meta)


    def listAllWork(
        self
        ):
        """
        Getter method.

        Returns
        -------
        ret0 : list
               Tuples of taxonomy ID and name of all assemblies whose indexes
               require updating.
        """
        ret = []
        for taxId in os.listdir(settings.rootPath):
            if taxId.isdecimal():
                path = os.path.join(settings.rootPath,taxId)
                if os.path.isdir(path):
                    for assemblyName in os.listdir(path):
                        workDir = os.path.join(settings.rootPath,taxId,assemblyName)
                        meta = self.__loadMeta_(workDir)
                        if (
                            not meta["processed"]["hisat"]
                            or not meta["processed"]["salmon"]
                            or not meta["processed"]["kallisto"]
                            or not meta["processed"]["gff"]
                        ):
                            ret.append((taxId,assemblyName))
        return ret


    def mirror(
        self
        ,species
        ):
        """
        Iterates through all local database folders, inspecting their metadata
        file and downloading any new data files if new versions are present on
        the remote server. Any assembly whose data is updated is marked to
        update its indexes.

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
                        if species:
                            fullName = meta["genus"].lower()+" "+meta["species"].lower()
                            if not species.lower() in fullName:
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
        crawler : class
                  The abstract crawler implementation that is registered.
        """
        if not isinstance(crawler,interfaces.AbstractCrawler):
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
        mirror : class
                 The abstract mirror implementation that is registered.
        """
        if not isinstance(mirror,interfaces.AbstractMirror):
            raise exception.RegisterError("Given object is not Mirror instance.")
        if name in self.__mirrors.keys():
            raise exception.RegisterError("Mirror '"+name+"' already exists.")
        self.__mirrors[name] = mirror


    def __indexFasta_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Indexes the FASTA file of the given assembly, running post processing on
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
        if os.path.isfile(os.path.join(workDir,path)):
            title = os.path.join(meta["taxonomy"]["id"],os.path.split(workDir)[-1])
            if not meta["processed"]["hisat"]:
                try:
                    core.log.send("Hisat2 Indexing FASTA "+title)
                    self.__indexWithHisat_(workDir,path)
                    meta["processed"]["hisat"] = True
                    self.__saveMeta_(workDir,meta)
                except:
                    core.log.send("Hisat2 Indexing FASTA "+title+" FAILURE!")
            if not meta["processed"]["salmon"]:
                try:
                    core.log.send("Salmon Indexing FASTA "+title)
                    self.__indexWithSalmon_(workDir,path)
                    meta["processed"]["salmon"] = True
                    self.__saveMeta_(workDir,meta)
                except:
                    core.log.send("Salmon Indexing FASTA "+title+" FAILURE!")
            if not meta["processed"]["kallisto"]:
                try:
                    core.log.send("Kallisto Indexing FASTA "+title)
                    self.__indexWithKallisto_(workDir,path)
                    meta["processed"]["kallisto"] = True
                    self.__saveMeta_(workDir,meta)
                except:
                    core.log.send("Kallisto Indexing FASTA "+title+" FAILURE!")


    def __indexGff_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Indexes the GFF file of the given assembly, running post processing on
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
        if os.path.isfile(os.path.join(workDir,path)):
            try:
                title = os.path.join(meta["taxonomy"]["id"],os.path.split(workDir)[-1])
                if not meta["processed"]["gff"]:
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
                    meta["processed"]["gff"] = True
                    self.__saveMeta_(workDir,meta)
            except:
                core.log.send("Indexing GFF "+title+" FAILURE!")


    def __indexWithHisat_(
        self
        ,workDir
        ,path
        ):
        """
        Indexes the FASTA file of the given assembly with the hisat2 program.

        Parameters
        ----------
        workDir : string
                  The working directory of the assembly.
        path : string
               The full file name of the given assembly's FASTA file located
               within the given working directory.
        """
        version = subprocess.check_output(["hisat2","--version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        filePath = os.path.join(workDir,path)
        outBase = os.path.join(workDir,"hisat-"+version)
        os.makedirs(outBase,exist_ok=True)
        outBase = os.path.join(outBase,path[:-3])
        cmd = ["hisat2-build","--quiet","-p",str(settings.cpuCount),"-f",filePath,outBase]
        assert(subprocess.run(cmd).returncode==0)


    def __indexWithKallisto_(
        self
        ,workDir
        ,path
        ):
        """
        Indexes the FASTA file of the given assembly with the kallisto program.

        Parameters
        ----------
        workDir : string
                  The working directory of the assembly.
        path : string
               The full file name of the given assembly's FASTA file located
               within the given working directory.
        """
        version = subprocess.check_output(["kallisto","version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        filePath = os.path.join(workDir,path)
        outBase = os.path.join(workDir,"kallisto-"+version)
        os.makedirs(outBase,exist_ok=True)
        outBase = os.path.join(outBase,path[:-3]+".idx")
        cmd = ["kallisto","index","--index",outBase,filePath]
        assert(subprocess.run(cmd,capture_output=True).returncode==0)


    def __indexWithSalmon_(
        self
        ,workDir
        ,path
        ):
        """
        Indexes the FASTA file of the given assembly with the salmon program.

        Parameters
        ----------
        workDir : string
                  The working directory of the assembly.
        path : string
               The full file name of the given assembly's FASTA file located
               within the given working directory.
        """
        version = subprocess.check_output(["salmon","--version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        filePath = os.path.join(workDir,path)
        outBase = os.path.join(workDir,"salmon-"+version)
        cmd = [
            "salmon"
            ,"index"
            ,"--index"
            ,outBase
            ,"--transcripts"
            ,filePath
            ,"--threads"
            ,str(settings.cpuCount)
        ]
        assert(subprocess.run(cmd,capture_output=True).returncode==0)


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
            if "processed" not in meta:
                meta["processed"] = {
                    "hisat": False
                    ,"salmon": False
                    ,"kallisto": False
                    ,"gff": False
                }
            return meta


    def __mirrorFasta_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Mirrors the FASTA file of the given assembly.

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
        fasta = False
        try:
            fasta = self.__mirrors[meta["mirror_type"]].mirrorFasta(
                workDir
                ,path
                ,meta["mirror_data"]
                ,title
            )
        except:
            core.log.send("Mirror FASTA "+title+" FAILURE!")
        if fasta:
            meta["processed"]["hisat"] = False
            meta["processed"]["salmon"] = False
            meta["processed"]["kallisto"] = False
            self.__saveMeta_(workDir,meta)


    def __mirrorGff_(
        self
        ,workDir
        ,path
        ,meta
        ):
        """
        Mirrors the GFF file of the given assembly.

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
        gff = False
        try:
            gff = self.__mirrors[meta["mirror_type"]].mirrorGff(
                workDir
                ,path
                ,meta["mirror_data"]
                ,title
            )
        except:
            core.log.send("Mirror GFF "+title+" FAILURE!")
        if gff:
            meta["processed"]["gff"] = False
            self.__saveMeta_(workDir,meta)


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
