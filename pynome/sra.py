"""
===========
SRA Helpers
===========

This module will write an sra.txt to each genome. sra.txt will contain a list
of accession numbers that are retrieved from a search using the corresponding
taxonomy id.


Filter criteria:

1)  read length >-= 100bp
2)  # of spots (reads):  15 Million
3)  PAIRED reads only
4)  Species with genome and GFF3 file.
5)  Illumina sequencers.

A problem emerges. Read lengths appear to be stored as strings. A greater than
or equal to implementation does not appear possible.

Sample search string:

((txid4530[Organism:exp]) AND
"biomol rna"[Properties]) AND
(("instrument hiseq x five"[Properties] OR
"instrument hiseq x ten"[Properties] OR
"instrument illumina genome analyzer"[Properties] OR
"instrument illumina genome analyzer ii"[Properties] OR
"instrument illumina genome analyzer iix"[Properties] OR
"instrument illumina hiseq 1000"[Properties] OR
"instrument illumina hiseq 1500"[Properties] OR
"instrument illumina hiseq 2000"[Properties] OR
"instrument illumina hiseq 2500"[Properties] OR
"instrument illumina hiseq 3000"[Properties] OR
"instrument illumina hiseq 4000"[Properties] OR
"instrument illumina miniseq"[Properties] OR
"instrument illumina miseq"[Properties] OR
"instrument illumina nextseq 500"[Properties] OR
"instrument nextseq 500"[Properties] OR
"instrument nextseq 550"[Properties] OR
"platform illumina"[Properties]))
"""

# import os
# import sys
# import json
import urllib
import argparse
import xmltodict


QUERY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&term='


def build_sra_search(tax_id):
    """
    Builds the SRA search string based on an input taxonomy id number.
    :return:
    """
    # sra_search_term_l = list()

    # for tax_id in tax_id_l:
    tax_id_str = "txid{0}[Organism:exp]".format(tax_id)
    properties_str = '"biomol rna"[Properties]'
    platform_str = '"platform illumina"[Properties]'
    search_str = tax_id_str + ' AND ' + properties_str + ' AND ' + platform_str
    # sra_search_term_l.append(search_str)

    # return sra_search_term_l
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
    retr_id_l = response['eSearchResult']['IdList']['Id']
    return retr_id_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('taxonomy_id', metavar='taxonomy-id', nargs='+')
    args = parser.parse_args()  # Parse the arguments

    # For each item passed, run the search
    for id in args.taxonomy_id:
        sra_query = build_sra_search(args.taxonomy_id)
        print(sra_query)
        result = run_sra_search(sra_query)
        print(result)
