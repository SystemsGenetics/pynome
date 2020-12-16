#!/usr/bin/env python3
"""
This is a custom standalone script module that contains a simple function which
outputs a list of assemblies with an optional first argument limiting it by
genus and species.
"""
import json
import os
import sys




def main():
    """
    Starts execution of this custom module script.
    """
    species = ""
    if len(sys.argv) >= 2:
        species = sys.argv[1]
    for taxId in os.listdir():
        if taxId.isdecimal():
            if os.path.isdir(taxId):
                for assemblyName in os.listdir(taxId):
                    path = os.path.join(taxId,assemblyName)
                    with open(os.path.join(path,"metadata.json"),"r") as ifile:
                        meta = json.loads(ifile.read())
                        fullName = meta["genus"].lower()+" "+meta["species"].lower()
                        if species and not species.lower() in fullName:
                            continue
                        print(
                            meta["genus"]
                            ,meta["species"]
                            ,meta["intraspecific_name"]
                            ,meta["process_type"]
                            ,meta["assembly_id"]
                            ,path
                            ,sep="\t"
                        )








if __name__ == "__main__":
    main()
