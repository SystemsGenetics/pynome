# DO NOT RUN THIS SCRIPT
# THIS IS A VERY HACKY SCRIPT DESIGNED FOR A VERY SPECIFIC TASK
import json
import os
import re
import subprocess
import sys


oldRootPath = sys.argv[1]
rootPath = sys.argv[2]



def findData(workDir):
    fasta = ""
    gff = ""
    gtf = ""
    splice = ""
    hisat = ""
    for p in os.listdir(workDir):
        if p.endswith(".fa"):
            fasta = os.path.join(workDir,p)
        if p.endswith(".gff"):
            gff = os.path.join(workDir,p)
        if p.endswith(".gtf"):
            gtf = os.path.join(workDir,p)
        if p.endswith(".Splice_sites"):
            splice = os.path.join(workDir,p)
        if p == "hisat-2.1.0":
            hisat = os.path.join(workDir,p)
    return (fasta,gff,gtf,splice,hisat)


def loadMeta(workDir):
    with open(os.path.join(workDir,"metadata.json"),"r") as ifile:
        meta = json.loads(ifile.read())
        return meta


def saveMeta(workDir,meta):
    with open(os.path.join(workDir,"metadata.json"),"w") as ofile:
        return ofile.write(json.dumps(meta,indent=4) + "\n\n")


def getRootName(meta):
    ret = meta["genus"]+"_"+meta["species"]
    if meta["intraspecific_name"]:
        ret += "_"+meta["intraspecific_name"]
    ret += "-"+meta["assembly_id"]
    return re.sub("[\s\\\\/]","_",ret)



def copyHiSat(fromDir,toDir,rootName):
    exts = {}
    for p in os.listdir(fromDir):
        if p.endswith(".ht2"):
            exts[p[-5:]] = p
    if exts:
        os.makedirs(toDir,exist_ok=True)
        for key in exts:
            cmd = [
                "cp"
                ,"--preserve=timestamps"
                ,os.path.join(fromDir,exts[key])
                ,os.path.join(toDir,rootName+"."+key)
            ]
            assert(subprocess.run(cmd).returncode==0)



for taxId in os.listdir(oldRootPath):
    if taxId.isdecimal():
        path = os.path.join(oldRootPath,taxId)
        if os.path.isdir(path):
            for assemblyName in os.listdir(path):
                oldWorkDir = os.path.join(path,assemblyName)
                workDir = os.path.join(rootPath,taxId,re.sub("[\s\\\\/]","_",assemblyName))
                if os.path.isdir(workDir):
                    meta = loadMeta(workDir)
                    rootName = getRootName(meta)
                    (fasta,gff,gtf,splice,hisat) = findData(oldWorkDir)
                    if fasta:
                        cmd = [
                            "cp"
                            ,"--preserve=timestamps"
                            ,fasta
                            ,os.path.join(workDir,rootName+".fa")
                        ]
                        assert(subprocess.run(cmd).returncode==0)
                    if gff:
                        cmd = [
                            "cp"
                            ,"--preserve=timestamps"
                            ,gff
                            ,os.path.join(workDir,rootName+".gff")
                        ]
                        assert(subprocess.run(cmd).returncode==0)
                    if gtf:
                        cmd = [
                            "cp"
                            ,"--preserve=timestamps"
                            ,gtf
                            ,os.path.join(workDir,rootName+".gtf")
                        ]
                        assert(subprocess.run(cmd).returncode==0)
                        meta["processed"]["write_gtf"] = True
                        saveMeta(workDir,meta)
                    if splice:
                        cmd = [
                            "cp"
                            ,"--preserve=timestamps"
                            ,splice
                            ,os.path.join(workDir,rootName+".Splice_sites")
                        ]
                        assert(subprocess.run(cmd).returncode==0)
                        meta["processed"]["write_splice_sites"] = True
                        saveMeta(workDir,meta)
                    if hisat:
                        copyHiSat(hisat,os.path.join(workDir,"hisat-2.1.0"),rootName)
                        meta["processed"]["index_hisat"] = True
                        saveMeta(workDir,meta)
