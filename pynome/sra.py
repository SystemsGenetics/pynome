"""
===========
SRA Helpers
===========

This module will write an sra.txt to each genome. sra.txt will contain a list
of accession numbers that are retrieved from a search using the corresponding
taxonomy id.


Filter criteria:

Filter criteria:

1)  read length >-= 100bp
2) # of spots (reads): 10 Million
3)  PAIRED reads only
4)  Species with genome and GFF3 file.
5)  Illumina sequencers.
6)  Assay Type: RNA-Seq

https://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

import urllib
import argparse
import xmltodict

ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

QUERY ='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term='

def construct_entrez_search():

    return


def build_sra_search(tax_id):
    """
    Builds the SRA search string based on an input taxonomy id number.
    :return:
    """
    tax_id_str = "{0}[uid]".format(tax_id)
    properties_str = '"biomol rna"[Properties]'
    platform_str = '"platform illumina"[Properties]'
    search_str = tax_id_str + '+AND+' + properties_str + '+AND+' + platform_str
    return search_str


def write_sra_file():
    pass


def run_sra_search(sra_term):
    """Runs the actual query."""
    query = QUERY + sra_term
    print(query)
    with urllib.request.urlopen(query) as response:
        response_xml = response.read()

    response = xmltodict.parse(response_xml)
    retr_id_l = response #['eSearchResult']['IdList']['Id']
    return retr_id_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('taxonomy_id', metavar='taxonomy-id', nargs='+')
    args = parser.parse_args()  # Parse the arguments

    # For each item passed, run the search
    for id in args.taxonomy_id:
        sra_query = build_sra_search(args.taxonomy_id)
        # print(sra_query)
        result = run_sra_search(sra_query)
        # print(result)
